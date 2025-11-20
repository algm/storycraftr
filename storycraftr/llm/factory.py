from __future__ import annotations

import os
import subprocess
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

console = Console()


_PROVIDER_DEFAULT_ENV = {
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "ollama": None,
    "fake": None,
    "ai-agent": None,
}

_OPENROUTER_DEFAULT_ENDPOINT = "https://openrouter.ai/api/v1"


@dataclass
class LLMSettings:
    """Normalized configuration to construct a chat model."""

    provider: str
    model: str
    endpoint: Optional[str] = None
    api_key_env: Optional[str] = None
    temperature: float = 0.7
    request_timeout: Optional[float] = None
    default_headers: Dict[str, str] = field(default_factory=dict)
    # AI agent CLI settings
    agent_cli_command: Optional[str] = None  # e.g., "cursor", "github-copilot-cli"
    agent_cli_args: Optional[List[str]] = None  # Additional CLI arguments


def _resolve_api_key(provider: str, explicit_env: Optional[str]) -> Optional[str]:
    env_var = explicit_env or _PROVIDER_DEFAULT_ENV.get(provider)
    if not env_var:
        return None
    api_key = os.getenv(env_var)
    if not api_key:
        raise RuntimeError(
            f"Missing environment variable '{env_var}' required for provider '{provider}'."
        )
    return api_key


def build_chat_model(settings: LLMSettings) -> BaseChatModel:
    """
    Build a LangChain chat model according to the supplied settings.

    Raises:
        RuntimeError: if required credentials are missing.
        ValueError: if the provider is unsupported.
    """

    provider = settings.provider.lower()

    if provider in ("openai", "openrouter"):
        api_key = _resolve_api_key(provider, settings.api_key_env)
        base_url = settings.endpoint or (
            _OPENROUTER_DEFAULT_ENDPOINT if provider == "openrouter" else None
        )
        params: Dict[str, object] = {
            "model": settings.model,
            "temperature": settings.temperature,
        }
        if settings.request_timeout:
            params["timeout"] = settings.request_timeout
        if base_url:
            params["base_url"] = base_url

        headers: Dict[str, str] = {}
        headers.update(settings.default_headers or {})
        if provider == "openrouter":
            headers.setdefault(
                "HTTP-Referer",
                os.getenv("STORYCRAFTR_HTTP_REFERER", "https://storycraftr.app"),
            )
            headers.setdefault(
                "X-Title", os.getenv("STORYCRAFTR_APP_NAME", "StoryCraftr CLI")
            )
        if headers:
            params["default_headers"] = headers

        return ChatOpenAI(api_key=api_key, **params)

    if provider == "ollama":
        base_url = settings.endpoint or os.getenv("OLLAMA_BASE_URL")
        params = {
            "model": settings.model,
            "temperature": settings.temperature,
        }
        if base_url:
            params["base_url"] = base_url
        if settings.request_timeout:
            params["timeout"] = settings.request_timeout

        return ChatOllama(**params)

    if provider == "fake":
        return _OfflineChatModel(
            template=(
                "Offline placeholder response for '{prompt}'. "
                "Set llm_provider to openai/openrouter/ollama for real generations."
            )
        )

    if provider == "ai-agent":
        cli_command = settings.agent_cli_command or os.getenv("AI_AGENT_CLI")
        cli_args = settings.agent_cli_args or []
        return _AIAgentChatModel(cli_command=cli_command, cli_args=cli_args)

    raise ValueError(f"Unsupported LLM provider '{settings.provider}'.")


class _OfflineChatModel(BaseChatModel):
    """Minimal offline chat model that returns placeholder responses."""

    template: str = (
        "Offline placeholder response for '{prompt}'. "
        "Set llm_provider to openai/openrouter/ollama for real generations."
    )

    def __init__(self, template: str):
        super().__init__(template=template)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> ChatResult:
        prompt_text = ""
        if messages:
            last_message = messages[-1]
            prompt_text = getattr(last_message, "content", str(last_message))
        content = self.template.format(prompt=prompt_text)
        generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "offline-placeholder"


class _AIAgentChatModel(BaseChatModel):
    """
    Chat model that integrates with AI coding assistant CLIs.
    
    Supports:
    - cursor-cli: Cursor AI command-line interface
    - github-copilot-cli: GitHub Copilot CLI
    - aider: Aider AI pair programming tool
    - Interactive mode: Manual copy-paste for any AI assistant
    
    This allows StoryCraftr to work with AI coding assistants by either:
    1. Calling their CLI directly (automated)
    2. Prompting the user interactively (manual)
    """

    cli_command: Optional[str] = None
    cli_args: List[str] = []

    def __init__(self, cli_command: Optional[str] = None, cli_args: Optional[List[str]] = None):
        super().__init__(cli_command=cli_command, cli_args=cli_args or [])

    def _format_messages_for_prompt(self, messages: List[BaseMessage]) -> str:
        """Format messages into a single prompt string."""
        parts = []
        for msg in messages:
            content = getattr(msg, "content", str(msg))
            if isinstance(msg, SystemMessage):
                parts.append(f"System: {content}")
            elif isinstance(msg, HumanMessage):
                parts.append(f"User: {content}")
            elif isinstance(msg, AIMessage):
                parts.append(f"Assistant: {content}")
            else:
                parts.append(f"{msg.__class__.__name__}: {content}")
        return "\n\n".join(parts)

    def _call_cursor_cli(self, prompt: str) -> str:
        """Call cursor CLI to get AI response."""
        try:
            # Cursor CLI command format: cursor chat "prompt"
            cmd = ["cursor", "chat", prompt]
            if self.cli_args:
                cmd.extend(self.cli_args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                error_msg = result.stderr.strip() or "Unknown error"
                console.print(f"[red]Cursor CLI error: {error_msg}[/red]")
                return self._fallback_to_interactive(prompt)
                
        except FileNotFoundError:
            console.print("[yellow]Cursor CLI not found. Install from https://cursor.sh[/yellow]")
            return self._fallback_to_interactive(prompt)
        except subprocess.TimeoutExpired:
            console.print("[red]Cursor CLI timeout[/red]")
            return self._fallback_to_interactive(prompt)
        except Exception as e:
            console.print(f"[red]Error calling Cursor CLI: {e}[/red]")
            return self._fallback_to_interactive(prompt)

    def _call_copilot_cli(self, prompt: str) -> str:
        """Call GitHub Copilot CLI to get AI response."""
        try:
            # GitHub Copilot CLI might use: gh copilot suggest or similar
            # Try multiple possible command formats
            commands_to_try = [
                ["gh", "copilot", "suggest", "-t", "shell", prompt],
                ["github-copilot-cli", prompt],
            ]
            
            for cmd in commands_to_try:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if result.returncode == 0:
                        return result.stdout.strip()
                except FileNotFoundError:
                    continue
            
            console.print("[yellow]GitHub Copilot CLI not found. Install with: gh extension install github/gh-copilot[/yellow]")
            return self._fallback_to_interactive(prompt)
                
        except subprocess.TimeoutExpired:
            console.print("[red]Copilot CLI timeout[/red]")
            return self._fallback_to_interactive(prompt)
        except Exception as e:
            console.print(f"[red]Error calling Copilot CLI: {e}[/red]")
            return self._fallback_to_interactive(prompt)

    def _call_aider_cli(self, prompt: str) -> str:
        """Call Aider CLI to get AI response."""
        try:
            # Aider command format: aider --message "prompt" --yes
            cmd = ["aider", "--message", prompt, "--yes", "--no-git"]
            if self.cli_args:
                cmd.extend(self.cli_args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                error_msg = result.stderr.strip() or "Unknown error"
                console.print(f"[red]Aider CLI error: {error_msg}[/red]")
                return self._fallback_to_interactive(prompt)
                
        except FileNotFoundError:
            console.print("[yellow]Aider CLI not found. Install with: pip install aider-chat[/yellow]")
            return self._fallback_to_interactive(prompt)
        except subprocess.TimeoutExpired:
            console.print("[red]Aider CLI timeout[/red]")
            return self._fallback_to_interactive(prompt)
        except Exception as e:
            console.print(f"[red]Error calling Aider CLI: {e}[/red]")
            return self._fallback_to_interactive(prompt)

    def _fallback_to_interactive(self, prompt: str) -> str:
        """Fallback to interactive mode when CLI fails."""
        console.print("\n")
        console.print(Panel(
            prompt,
            title="[bold cyan]StoryCraftr Request to AI Agent[/bold cyan]",
            border_style="cyan",
            expand=False
        ))
        console.print("\n[yellow]Please provide the AI agent's response below:[/yellow]")
        console.print("[dim]Press ESC then ENTER for multiline mode, or just type and press ENTER[/dim]\n")
        
        try:
            response = prompt(
                HTML("<ansicyan>AI Agent Response:</ansicyan> "),
                multiline=False
            )
            
            if not response.strip():
                console.print("[yellow]Entering multiline mode. Press ESC then ENTER when done.[/yellow]")
                response = prompt(
                    HTML("<ansicyan>AI Agent Response (multiline):</ansicyan> "),
                    multiline=True
                )
            
            content = response.strip()
            if not content:
                content = "I cannot provide a response at this time."
            return content
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Operation cancelled.[/red]")
            return "Operation cancelled by user."

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> ChatResult:
        """Generate a response using AI agent CLI or interactive mode."""
        
        # Format messages into a prompt
        prompt_text = self._format_messages_for_prompt(messages)
        
        # Determine which CLI to use
        cli = self.cli_command or os.getenv("AI_AGENT_CLI", "").lower()
        
        console.print(f"\n[dim]Using AI agent: {cli or 'interactive mode'}[/dim]")
        
        # Call appropriate CLI or fallback to interactive
        if cli in ("cursor", "cursor-cli"):
            content = self._call_cursor_cli(prompt_text)
        elif cli in ("copilot", "github-copilot-cli", "gh-copilot"):
            content = self._call_copilot_cli(prompt_text)
        elif cli in ("aider", "aider-chat"):
            content = self._call_aider_cli(prompt_text)
        elif cli:
            # Generic CLI call
            console.print(f"[yellow]Unknown CLI '{cli}', trying generic call...[/yellow]")
            try:
                result = subprocess.run(
                    [cli, prompt_text] + self.cli_args,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    content = result.stdout.strip()
                else:
                    content = self._fallback_to_interactive(prompt_text)
            except Exception as e:
                console.print(f"[red]Error calling {cli}: {e}[/red]")
                content = self._fallback_to_interactive(prompt_text)
        else:
            # No CLI specified, use interactive mode
            content = self._fallback_to_interactive(prompt_text)
        
        generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "ai-agent"
