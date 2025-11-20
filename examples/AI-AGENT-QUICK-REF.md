# AI Agent Mode Quick Reference

## Quick Start

### Initialize with Cursor
```bash
storycraftr init "My Novel" --llm-provider ai-agent --agent-cli cursor
```

### Initialize with Aider
```bash
storycraftr init "My Novel" --llm-provider ai-agent --agent-cli aider
```

### Initialize with GitHub Copilot
```bash
storycraftr init "My Novel" --llm-provider ai-agent --agent-cli gh-copilot
```

### Initialize Interactive Mode
```bash
storycraftr init "My Novel" --llm-provider ai-agent
```

## Configuration

### Via storycraftr.json
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

### Via Environment Variable
```bash
export AI_AGENT_CLI="cursor"
storycraftr init "My Novel" --llm-provider ai-agent
```

## Supported CLIs

| CLI | Command | Installation |
|-----|---------|--------------|
| **Cursor** | `cursor` | Install Cursor IDE from https://cursor.sh |
| **Aider** | `aider` | `pip install aider-chat` |
| **GitHub Copilot** | `gh-copilot` | `gh extension install github/gh-copilot` |
| **Interactive** | _(none)_ | No installation needed |

## Common Commands

```bash
# Worldbuilding
storycraftr worldbuilding technology "Advanced tech description"
storycraftr worldbuilding magic-system "Magic system rules"

# Outlining
storycraftr outline general-outline "Story concept"
storycraftr outline character-summary

# Chapters
storycraftr chapters chapter 1
storycraftr chapters chapter 2

# Chat Mode
storycraftr chat
```

## In Chat Mode

```
# Iterate commands
!iterate improve-character-motivation "Character Name"
!iterate add-subplot "Subplot description"

# Outline commands
!outline general-outline "Story concept"
!outline plot-points

# Worldbuilding commands
!worldbuilding cultures "Culture description"
!worldbuilding technology "Tech description"

# Chapter commands
!chapters chapter 1
```

## Switching Providers

Edit `storycraftr.json`:

**Use AI Agent (Cursor):**
```json
{"llm_provider": "ai-agent", "agent_cli": "cursor"}
```

**Use OpenAI:**
```json
{"llm_provider": "openai", "llm_model": "gpt-4"}
```

**Use Ollama:**
```json
{"llm_provider": "ollama", "llm_model": "llama3"}
```

## Troubleshooting

### CLI Not Found
```bash
# Install Cursor: Download from https://cursor.sh
# Install Aider: pip install aider-chat
# Install Copilot CLI: 
#   1. First install GitHub CLI: https://cli.github.com
#   2. Then install extension: gh extension install github/gh-copilot
```

### Timeout
Increase timeout in `storycraftr.json`:
```json
{"request_timeout": 300}
```

### CLI Args
Customize CLI behavior:
```json
{
  "agent_cli": "aider",
  "agent_cli_args": ["--no-git", "--yes", "--model", "gpt-4"]
}
```

## How It Works

1. **With CLI**: StoryCraftr → CLI → AI → Response → StoryCraftr
2. **Interactive**: StoryCraftr → Display → You → AI → You → StoryCraftr

## Benefits

✅ Use existing AI subscriptions  
✅ No separate API keys needed  
✅ Automatic or manual modes  
✅ Full control over generation  
✅ Works with any AI assistant  

## Links

- [Full Documentation](../docs/ai-agent-mode.md)
- [Examples](ai-agent-mode-examples.md)
- [Getting Started](../docs/getting_started.md)
- [Chat Mode](../docs/chat.md)
