# GitHub Copilot Instructions for StoryCraftr

## Project Context

StoryCraftr is an AI-powered CLI tool for writing books and research papers. It uses LangChain to support multiple LLM providers and features an interactive chat mode.

## Key Technologies

- **Python 3.10+**: Main language for CLI and agents
- **LangChain**: LLM abstraction layer
- **Click**: CLI framework
- **Rich**: Terminal UI
- **TypeScript**: VS Code extension
- **Poetry**: Python dependency management

## Code Style Preferences

### Python
- Use Black formatting (88 chars)
- Type hints on all public functions
- snake_case naming
- Comprehensive docstrings
- Security scanning with detect-secrets

### TypeScript
- Follow project tsconfig
- camelCase for functions
- PascalCase for classes

## Architecture Patterns

### LLM Provider Pattern
All LLM providers implement `BaseChatModel` from LangChain:
```python
from langchain_core.language_models.chat_models import BaseChatModel

class CustomProvider(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        # Implementation
        pass
```

### Agent Pattern
Agents use LangChain's agent framework with custom prompts:
```python
from storycraftr.agent.agents import create_or_get_assistant

def my_agent(llm, config):
    assistant = create_or_get_assistant(
        llm=llm,
        role="my-role",
        instructions="...",
        book_path=config["book_path"]
    )
    return assistant.invoke({"input": "..."})
```

### Command Pattern
CLI commands follow Click conventions:
```python
@click.command()
@click.argument("arg")
@click.option("--option", default="value")
def my_command(arg, option):
    """Command description."""
    # Implementation
```

## Important Conventions

### Configuration
- Projects store config in `storycraftr.json`
- Supports: `llm_provider`, `llm_model`, `temperature`, etc.
- Provider options: `"openai"`, `"openrouter"`, `"ollama"`, `"ai-agent"`, `"fake"`

### File Structure
- Story chapters: `chapters/chapter_*.md`
- Worldbuilding: `worldbuilding/*.md`
- Outlines: `outlines/*.md`
- Hidden data: `.storycraftr/`

### LLM Providers
1. **OpenAI**: Requires `OPENAI_API_KEY`
2. **OpenRouter**: Requires `OPENROUTER_API_KEY`
3. **Ollama**: Local, no key needed
4. **AI-Agent**: Interactive mode for Cursor/Copilot
5. **Fake**: Testing/offline mode

## AI Agent Mode

The `ai-agent` provider enables StoryCraftr to work with AI coding assistants:

```python
# In factory.py
if provider == "ai-agent":
    return _AIAgentChatModel()

class _AIAgentChatModel(BaseChatModel):
    def _generate(self, messages, ...):
        # Display prompt to user
        # Get response from AI assistant
        # Return as ChatResult
```

Users copy StoryCraftr prompts to Cursor/Copilot and paste responses back.

## Testing Expectations

### Unit Tests
```python
# tests/unit/test_feature.py
def test_feature():
    result = feature_function(input)
    assert result == expected
```

### Integration Tests
```python
# tests/integration/test_workflow.py
def test_full_workflow(tmp_path):
    # Test end-to-end scenarios
```

## Common Patterns to Suggest

### Error Handling
```python
try:
    result = operation()
except SpecificError as e:
    console.print(f"[red]Error: {e}[/red]")
    raise click.ClickException(str(e))
```

### Rich Output
```python
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel("Message", title="Title", border_style="cyan"))
```

### Path Handling
```python
from pathlib import Path

book_path = Path(book_path_str)
config_file = book_path / "storycraftr.json"
```

## Security Guidelines

1. Never hardcode API keys
2. Load credentials from environment or `~/.storycraftr/`
3. Use `detect-secrets` for scanning
4. Validate user input
5. Sanitize file paths

## Documentation Standards

### Docstrings
```python
def function(param: str) -> bool:
    """
    Brief description.

    Args:
        param: Description of param.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param is invalid.
    """
```

### Markdown Files
- Use ATX headers (`#`, `##`, etc.)
- Include code blocks with language tags
- Add examples where helpful
- Link to related docs

## When Suggesting Code

### Prefer
- Existing patterns from codebase
- LangChain built-in features
- Rich library for terminal output
- Type hints
- Descriptive variable names

### Avoid
- Breaking changes to public APIs
- Adding new dependencies unnecessarily
- Complex abstractions for simple tasks
- Hardcoded values
- Global state

## Common Files to Reference

- `storycraftr/llm/factory.py`: LLM provider logic
- `storycraftr/cli.py`: CLI entry point
- `storycraftr/agent/agents.py`: Base agent functionality
- `storycraftr/chat/session.py`: Chat session management
- `docs/ai-agent-mode.md`: AI agent integration docs

## Helpful Commands

```bash
# Development
poetry install
poetry run storycraftr --help
poetry run pytest
poetry run black .
poetry run pre-commit run --all-files

# Extension
npm install
npm run compile
npm run watch

# Usage
storycraftr init "Title" --llm-provider ai-agent
storycraftr chat
storycraftr outline general-outline "Description"
```

## Project Goals

1. Make AI-assisted writing accessible
2. Support multiple LLM providers
3. Keep writers in creative control
4. Enable offline/local AI usage
5. Integrate with developer tools (Cursor, Copilot)

## When Assisting with AI Agent Mode

The AI Agent mode is designed to let users leverage their existing AI assistant subscriptions. When helping with this feature:

1. Ensure prompts are clearly formatted
2. Provide helpful instructions for copy-paste workflow
3. Support both single-line and multi-line input
4. Handle interruptions gracefully
5. Make it easy to switch between providers

## Links

- Repository: https://github.com/raestrada/storycraftr
- Documentation: docs/
- Issues: GitHub Issues
- Extension: https://marketplace.visualstudio.com/items?itemName=StoryCraftr.storycraftr
