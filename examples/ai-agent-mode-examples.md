# StoryCraftr AI Agent Mode Examples

This directory contains example configurations and use cases for StoryCraftr's AI Agent Mode.

## Example Configurations

### Example 1: Using Cursor CLI

**storycraftr.json:**
```json
{
  "title": "My Sci-Fi Novel",
  "primary_language": "en",
  "default_author": "John Doe",
  "genre": "science fiction",
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "cursor",
  "agent_cli_args": [],
  "temperature": 0.7,
  "request_timeout": 120
}
```

**Usage:**
```bash
cd my-novel
storycraftr outline general-outline "A dystopian future where AI controls society"
```

StoryCraftr will automatically call Cursor's CLI to generate the outline.

### Example 2: Using Aider

**storycraftr.json:**
```json
{
  "title": "Fantasy Epic",
  "primary_language": "en",
  "default_author": "Jane Smith",
  "genre": "fantasy",
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "aider",
  "agent_cli_args": ["--no-git", "--yes"],
  "temperature": 0.7,
  "request_timeout": 120
}
```

**Usage:**
```bash
cd fantasy-epic
storycraftr worldbuilding magic-system "Describe a magic system based on emotions"
```

Aider will process the request and StoryCraftr will integrate the response.

### Example 3: GitHub Copilot CLI

**storycraftr.json:**
```json
{
  "title": "Mystery Novel",
  "primary_language": "en",
  "default_author": "Detective Writer",
  "genre": "mystery",
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "gh-copilot",
  "agent_cli_args": [],
  "temperature": 0.7,
  "request_timeout": 120
}
```

**Usage:**
```bash
cd mystery-novel
storycraftr chapters chapter 1
```

GitHub Copilot CLI will generate the chapter content.

### Example 4: Interactive Mode (No CLI)

**storycraftr.json:**
```json
{
  "title": "Romance Novel",
  "primary_language": "es",
  "default_author": "Romantic Writer",
  "genre": "romance",
  "llm_provider": "ai-agent",
  "llm_model": "ai-agent",
  "agent_cli": "",
  "agent_cli_args": [],
  "temperature": 0.8,
  "request_timeout": 120
}
```

**Usage:**
```bash
cd romance-novel
storycraftr outline character-summary
```

StoryCraftr will display the prompt in a panel. You copy it to any AI assistant (Cursor, Copilot, ChatGPT, Claude, etc.), get the response, and paste it back.

## Complete Workflow Example

### Setting Up a New Project with Cursor

```bash
# 1. Initialize project with AI agent mode
storycraftr init "Space Opera" \
  --primary-language "en" \
  --author "Sci-Fi Author" \
  --genre "science fiction" \
  --llm-provider "ai-agent" \
  --agent-cli "cursor"

cd "Space Opera"

# 2. Create worldbuilding
storycraftr worldbuilding technology "Faster-than-light travel technology"
storycraftr worldbuilding geography "Three inhabited star systems"

# 3. Create outline
storycraftr outline general-outline "Epic space opera about rebellion"
storycraftr outline character-summary

# 4. Generate chapters
storycraftr chapters chapter 1
storycraftr chapters chapter 2

# 5. Use chat mode for iteration
storycraftr chat
```

In chat mode:
```
> !iterate improve-character-motivation "Main Character"
> !worldbuilding cultures "Describe the three main cultures"
> !outline plot-points
```

## Environment Variables

You can also use environment variables to configure the AI agent:

```bash
# Set the agent CLI globally
export AI_AGENT_CLI="cursor"

# Initialize without specifying --agent-cli
storycraftr init "My Novel" --llm-provider "ai-agent"

# The AI_AGENT_CLI environment variable will be used
```

## Switching Between Modes

You can easily switch between different providers by editing `storycraftr.json`:

**Use Cursor:**
```json
{
  "llm_provider": "ai-agent",
  "agent_cli": "cursor"
}
```

**Use OpenAI directly:**
```json
{
  "llm_provider": "openai",
  "llm_model": "gpt-4"
}
```

**Use Ollama locally:**
```json
{
  "llm_provider": "ollama",
  "llm_model": "llama3"
}
```

## Tips for Best Results

1. **Use specific prompts**: The more detailed your prompt, the better the AI agent's response
2. **Leverage context**: AI agents have access to your entire codebase/project
3. **Iterate**: Use the chat mode to refine and improve content
4. **Combine modes**: Use AI agent mode for generation, then switch to direct API for batch processing
5. **Save often**: StoryCraftr autosaves progress in `.storycraftr/` directory

## Troubleshooting

### CLI Not Found

If you get "CLI not found" error:
- **Cursor**: Install Cursor IDE from https://cursor.sh
- **Aider**: Run `pip install aider-chat`
- **Copilot**: Run `gh extension install github/gh-copilot`

### Timeout Issues

If the CLI times out, increase the timeout in your config:
```json
{
  "request_timeout": 300
}
```

### Interactive Fallback

If the CLI fails, StoryCraftr automatically falls back to interactive mode. You can still use any AI assistant by copy-pasting prompts.

## Next Steps

- Read the [AI Agent Mode Guide](../docs/ai-agent-mode.md)
- Check the [Getting Started Guide](../docs/getting_started.md)
- Explore [Chat Mode](../docs/chat.md)
- Learn about [Iteration Commands](../docs/iterate.md)
