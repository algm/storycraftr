# StoryCraftr AI Agent Integration Architecture

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        StoryCraftr CLI                          │
│                    (storycraftr outline ...)                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ Reads configuration
                            ▼
                  ┌──────────────────────┐
                  │  storycraftr.json    │
                  │  ─────────────────   │
                  │  llm_provider: "ai-agent"   │
                  │  agent_cli: "cursor"        │
                  │  agent_cli_args: []         │
                  └──────────┬───────────┘
                            │
                            │ Builds LLM
                            ▼
              ┌──────────────────────────────┐
              │    LLMSettings Factory       │
              │    (llm_settings_from_config)│
              └──────────┬───────────────────┘
                        │
                        │ Creates
                        ▼
          ┌────────────────────────────────────┐
          │      _AIAgentChatModel             │
          │  ────────────────────────────────  │
          │  - cli_command: "cursor"           │
          │  - cli_args: []                    │
          │  - _generate(messages) →           │
          └────────┬───────────────────────────┘
                  │
                  │ When LLM call needed
                  ▼
    ┌─────────────────────────────────┐
    │   Format prompt from messages   │
    │   (System + User + Assistant)   │
    └─────────┬───────────────────────┘
              │
              │ CLI configured?
              ▼
        ┌─────────┴─────────┐
        │                   │
    YES │               NO  │
        │                   │
        ▼                   ▼
┌───────────────┐   ┌─────────────────┐
│ Call CLI      │   │ Interactive     │
│               │   │ Mode            │
│ cursor chat   │   │                 │
│ aider --msg   │   │ Display prompt  │
│ gh copilot    │   │ Wait for input  │
└───────┬───────┘   └────────┬────────┘
        │                    │
        │ Success?           │
        ▼                    │
    ┌───────┴───────┐        │
    │               │        │
YES │           NO  │        │
    │               │        │
    ▼               ▼        │
┌─────────┐   ┌────────────┐│
│ Return  │   │ Fallback  ││
│ response│   │ to        ││
│         │   │ interactive│←┘
└────┬────┘   └─────┬──────┘
     │              │
     │              │
     └──────┬───────┘
            │
            │ Process response
            ▼
    ┌───────────────────┐
    │  ChatResult       │
    │  with AIMessage   │
    └───────┬───────────┘
            │
            │ Return to
            ▼
   ┌─────────────────────┐
   │  StoryCraftr Agent  │
   │  Continues workflow │
   └─────────────────────┘
```

## Sequence Diagrams

### Automatic Mode (with Cursor CLI)

```
User          StoryCraftr       Factory       AIAgentModel    Cursor CLI
 │                │               │                │              │
 │  storycraftr   │               │                │              │
 │  outline ...   │               │                │              │
 ├───────────────>│               │                │              │
 │                │ Build LLM     │                │              │
 │                ├──────────────>│                │              │
 │                │               │ Create Model   │              │
 │                │               ├───────────────>│              │
 │                │               │                │              │
 │                │ Generate      │                │              │
 │                ├──────────────────────────────->│              │
 │                │               │                │ cursor chat  │
 │                │               │                ├─────────────>│
 │                │               │                │              │
 │                │               │                │<─────────────┤
 │                │               │                │  AI Response │
 │                │               │<───────────────┤              │
 │                │<──────────────────────────────-┤              │
 │                │  Process                       │              │
 │<───────────────┤  Response                      │              │
 │  Result        │               │                │              │
```

### Interactive Mode (Manual)

```
User          StoryCraftr       Factory       AIAgentModel      Terminal
 │                │               │                │                │
 │  storycraftr   │               │                │                │
 │  outline ...   │               │                │                │
 ├───────────────>│               │                │                │
 │                │ Build LLM     │                │                │
 │                ├──────────────>│                │                │
 │                │               │ Create Model   │                │
 │                │               ├───────────────>│                │
 │                │               │                │                │
 │                │ Generate      │                │                │
 │                ├──────────────────────────────->│                │
 │                │               │                │  Display       │
 │                │               │                │  Prompt Panel  │
 │                │               │                ├───────────────>│
 │                │               │                │                │
 │ Copy prompt    │               │                │                │
 │ to AI agent    │               │                │                │
 │ (Cursor/Copilot)              │                │                │
 │ Get response   │               │                │                │
 │                │               │                │<───────────────┤
 │ Paste response │               │                │  User types    │
 │                │               │<───────────────┤  response      │
 │                │<──────────────────────────────-┤                │
 │                │  Process                       │                │
 │<───────────────┤  Response                      │                │
 │  Result        │               │                │                │
```

## Component Details

### _AIAgentChatModel

**Attributes:**
- `cli_command`: str - Name of the CLI to call (cursor, aider, gh-copilot)
- `cli_args`: List[str] - Additional arguments to pass to the CLI

**Methods:**
- `_format_messages_for_prompt(messages)`: Convert LangChain messages to prompt string
- `_call_cursor_cli(prompt)`: Execute cursor CLI and return response
- `_call_aider_cli(prompt)`: Execute aider CLI and return response
- `_call_copilot_cli(prompt)`: Execute gh copilot CLI and return response
- `_fallback_to_interactive(prompt)`: Display prompt and get user input
- `_generate(messages, ...)`: Main entry point, routes to appropriate CLI or interactive

**Error Handling:**
- FileNotFoundError: CLI not installed → Fallback to interactive
- TimeoutExpired: CLI timeout → Fallback to interactive
- subprocess.CalledProcessError: CLI error → Fallback to interactive
- KeyboardInterrupt/EOFError: User cancellation → Return cancelled message

## Configuration Flow

```
CLI Argument           Environment Variable        storycraftr.json
─────────────          ──────────────────          ────────────────
                                                   
--agent-cli cursor  →  AI_AGENT_CLI=cursor    →   "agent_cli": "cursor"
                                                   
                       (Fallback order: CLI arg > JSON > Env var)
```

## Supported CLI Commands

### Cursor
```bash
cursor chat "formatted prompt with system and user messages"
```

### Aider
```bash
aider --message "formatted prompt" --yes --no-git [--custom-args]
```

### GitHub Copilot
```bash
gh copilot suggest -t shell "formatted prompt"
```

### Generic CLI
```bash
<custom-cli> "formatted prompt" [custom-args]
```

## Benefits of This Architecture

1. **Separation of Concerns**: LLM abstraction layer handles provider details
2. **Graceful Degradation**: Automatic fallback to interactive mode
3. **Extensibility**: Easy to add new CLI integrations
4. **User Choice**: Configure via JSON, CLI args, or environment variables
5. **Error Resilience**: Multiple fallback mechanisms
6. **Timeout Protection**: Prevents hanging on CLI failures

## Future Enhancements

- [ ] Support for streaming responses
- [ ] Custom CLI templates for other tools
- [ ] Response caching to avoid redundant calls
- [ ] Parallel CLI calls for batch operations
- [ ] CLI health check before invocation
