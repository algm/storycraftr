# Using StoryCraftr with AI Coding Agents (Cursor/Copilot/Aider)

StoryCraftr now supports an **AI Agent Mode** that allows you to use it with AI coding assistants like **Cursor**, **GitHub Copilot**, or **Aider** instead of connecting directly to LLM APIs. This mode can automatically call the AI agent's CLI or provide an interactive interface for manual integration.

## Overview

In AI Agent Mode, StoryCraftr can:
1. **Automatically call AI agent CLIs** (cursor, aider, gh-copilot) to get responses
2. **Interactive mode** - display prompts for you to forward to any AI assistant

This workflow allows you to:

- Use your existing AI assistant subscriptions without needing separate API keys
- Leverage the context and capabilities of your AI coding assistant
- Have more control over the generation process
- Work offline or in environments where direct API access is restricted

## Setup

### 1. Initialize Your Project with AI Agent Mode

When creating a new StoryCraftr project, set the provider to `ai-agent` and optionally specify which CLI to use:

**With Cursor CLI:**
```bash
storycraftr init "My Novel" \
  --primary-language "en" \
  --author "Your Name" \
  --genre "science fiction" \
  --llm-provider "ai-agent" \
  --llm-model "ai-agent" \
  --agent-cli "cursor"
```

**With Aider:**
```bash
storycraftr init "My Novel" \
  --primary-language "en" \
  --author "Your Name" \
  --genre "science fiction" \
  --llm-provider "ai-agent" \
  --llm-model "ai-agent" \
  --agent-cli "aider"
```

**With GitHub Copilot CLI:**
```bash
storycraftr init "My Novel" \
  --primary-language "en" \
  --author "Your Name" \
  --genre "science fiction" \
  --llm-provider "ai-agent" \
  --llm-model "ai-agent" \
  --agent-cli "gh-copilot"
```

**Interactive Mode (no CLI):**
```bash
storycraftr init "My Novel" \
  --primary-language "en" \
  --author "Your Name" \
  --genre "science fiction" \
  --llm-provider "ai-agent" \
  --llm-model "ai-agent"
```

### 2. Configure an Existing Project

Edit your `storycraftr.json` file and update the LLM configuration:

**With Cursor CLI:**
```json
{
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "cursor",
  "agent_cli_args": [],
  "temperature": 0.7,
  "request_timeout": 120
}
```

**With Aider:**
```json
{
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "aider",
  "agent_cli_args": ["--no-git", "--yes"],
  "temperature": 0.7,
  "request_timeout": 120
}
```

**Interactive Mode:**
```json
{
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "",
  "agent_cli_args": [],
  "temperature": 0.7,
  "request_timeout": 120
}
```

### 3. Environment Variable Configuration

Alternatively, you can set the AI agent CLI via environment variable:

```bash
export AI_AGENT_CLI="cursor"
# or
export AI_AGENT_CLI="aider"
# or
export AI_AGENT_CLI="gh-copilot"
```

## Usage

### Automatic CLI Integration

When you configure `agent_cli` in your `storycraftr.json`, StoryCraftr will automatically call the AI agent CLI and get responses:

```bash
storycraftr outline general-outline "Write a sci-fi story about AI"
```

**Output (with cursor CLI configured):**
```
Using AI agent: cursor
[Cursor processes the prompt and returns the response]
[Response is automatically integrated into your project]
```

StoryCraftr will:
1. Format the prompt with full context
2. Call the AI agent CLI (e.g., `cursor chat "prompt"`)
3. Capture the response
4. Process it and continue the workflow

### Interactive Workflow (Fallback)

If the CLI call fails or no CLI is configured, StoryCraftr falls back to interactive mode:

1. **StoryCraftr displays a prompt**: The system shows you the complete context
2. **You copy the prompt to your AI agent**: Paste it into Cursor, Copilot Chat, or your preferred AI assistant
3. **Your AI agent generates a response**: Get the response from your AI assistant
4. **You paste the response back**: Copy and paste the AI agent's response into the StoryCraftr prompt
5. **StoryCraftr processes the response**: The system continues with the workflow

## Supported AI Agent CLIs

### Cursor CLI

[Cursor](https://cursor.sh) is an AI-powered code editor with a command-line interface.

**Installation:**
```bash
# Cursor CLI is installed with the Cursor app
# Available after installing Cursor IDE
```

**Configuration:**
```json
{
  "agent_cli": "cursor",
  "agent_cli_args": []
}
```

**How it works:**
StoryCraftr calls: `cursor chat "your prompt here"`

### Aider

[Aider](https://aider.chat) is an AI pair programming tool in your terminal.

**Installation:**
```bash
pip install aider-chat
```

**Configuration:**
```json
{
  "agent_cli": "aider",
  "agent_cli_args": ["--no-git", "--yes"]
}
```

**How it works:**
StoryCraftr calls: `aider --message "your prompt" --yes --no-git`

### GitHub Copilot CLI

[GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli) provides terminal-based Copilot access.

**Installation:**
```bash
# First install GitHub CLI from https://cli.github.com
# Then install the Copilot extension:
gh extension install github/gh-copilot
```

**Configuration:**
```json
{
  "agent_cli": "gh-copilot",
  "agent_cli_args": []
}
```

**How it works:**
StoryCraftr calls: `gh copilot suggest -t shell "your prompt"`

### Generic CLI

You can also use any custom CLI tool:

**Configuration:**
```json
{
  "agent_cli": "/path/to/your/ai-cli",
  "agent_cli_args": ["--custom-arg"]
}
```

### Interactive Mode (No CLI)

If you don't have a CLI or prefer manual control:

**Configuration:**
```json
{
  "agent_cli": "",
  "agent_cli_args": []
}
```

In this mode, StoryCraftr will display prompts in a panel and wait for you to paste responses.

## Example Session

```bash
storycraftr outline general-outline "Write a sci-fi story about AI"
```

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│ StoryCraftr Request to AI Agent                             │
├─────────────────────────────────────────────────────────────┤
│ **System**: You are a creative writing assistant...         │
│                                                             │
│ **User**: Create a general outline for a science fiction   │
│ story about AI...                                           │
└─────────────────────────────────────────────────────────────┘

Please provide the AI agent's response below:
Press ESC then ENTER for multiline mode, or just type and press ENTER

AI Agent Response: _
```

At this point:
1. Copy the entire prompt (System + User messages)
2. Paste into Cursor/Copilot Chat
3. Get the AI's response
4. Copy and paste the response back into the "AI Agent Response:" prompt

## Best Practices

### Working with Cursor

1. **Open Cursor Composer** (Cmd/Ctrl + I)
2. When StoryCraftr shows a prompt, copy the entire context
3. Paste into Cursor Composer and press Enter
4. Copy Cursor's response and paste it back into StoryCraftr

### Working with GitHub Copilot

1. **Open Copilot Chat** in VS Code (Cmd/Ctrl + Shift + I)
2. When StoryCraftr shows a prompt, copy the system and user messages
3. Paste into Copilot Chat
4. Copy Copilot's response and paste it back into StoryCraftr

### Tips for Better Results

- **Include full context**: When copying prompts to your AI agent, include both System and User messages for better context
- **Use multiline mode**: For longer responses, press ESC then ENTER in the StoryCraftr prompt to enable multiline input
- **Save intermediate results**: StoryCraftr automatically saves progress, so you can stop and resume sessions
- **Use chat mode**: The `storycraftr chat` command works great with AI Agent Mode for iterative refinement

## Advanced Configuration

### Customizing the Experience

You can combine AI Agent Mode with other StoryCraftr features:

```bash
# Use AI Agent Mode with chat
storycraftr chat --book-path ./my-novel

# Generate chapters with AI Agent Mode
storycraftr chapters chapter 1

# Iterate on existing content
storycraftr iterate rename-character "Old Name" "New Name"
```

### Switching Between Modes

You can easily switch between AI Agent Mode and direct API mode by editing `storycraftr.json`:

**AI Agent Mode:**
```json
{
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent"
}
```

**OpenAI Mode:**
```json
{
  "llm_provider": "openai",
  "llm_model": "gpt-4"
}
```

**Ollama Mode:**
```json
{
  "llm_provider": "ollama",
  "llm_model": "llama3"
}
```

## Troubleshooting

### Empty Responses

If you press ENTER without providing a response, StoryCraftr will use a default message. You can cancel with Ctrl+C and restart the command.

### Long Prompts

For very long prompts, consider:
- Using a text editor to compose the response
- Breaking down the task into smaller steps
- Using StoryCraftr's chat mode for iterative work

### Copy-Paste Issues

If copy-paste doesn't work well in your terminal:
- Try a different terminal emulator
- Enable multiline mode (ESC + ENTER)
- Check your terminal's paste settings

## Why Use AI Agent Mode?

**Flexibility**: Use the AI assistant you're already paying for
**Control**: Review and modify responses before they're processed
**Privacy**: Keep sensitive content within your AI assistant's context
**Learning**: See exactly what prompts StoryCraftr uses and how AI responds
**Offline Work**: Work in environments without direct internet access to LLM APIs

## Example Workflows

### Creating a Novel with Cursor

```bash
# 1. Initialize with AI Agent Mode
storycraftr init "Space Opera" \
  --primary-language "en" \
  --llm-provider "ai-agent"

# 2. Start chat mode
storycraftr chat

# 3. In chat, use commands and copy prompts to Cursor:
> !worldbuilding technology "Describe faster-than-light travel"
# Copy prompt to Cursor, get response, paste back

> !outline general-outline "Create the main story arc"
# Copy prompt to Cursor, get response, paste back

> !chapters chapter 1
# Copy prompt to Cursor, get response, paste back
```

### Refining Content with Copilot

```bash
# Use iterate commands with Copilot's help
storycraftr iterate improve-character-motivation "Main Character"
# Copy prompt to Copilot Chat, get refined character motivation

storycraftr iterate add-subplot "Secondary plot about..."
# Copy prompt to Copilot Chat, integrate subplot
```

## Next Steps

- Explore the [Getting Started Guide](getting_started.md)
- Learn about [Chat Mode](chat.md)
- Read about [Iteration Commands](iterate.md)
- Check the [Advanced Guide](advanced.md)

Happy writing with your AI agent! 📚✨
