# Minimal AI Agents

You don't need an agentic framework to start building agents.

## Agents

| Agent | What it does | Run |
|-------|--------------|-----|
| `agent_web.py` | Fetch & summarize any URL | `python agent_web.py` |
| `agent_shell.py` | Run shell commands (with approval) | `python agent_shell.py` |
| `agent_stock.py` | Get stock prices | `python agent_stock.py` |
| `agent_github.py` | Search GitHub code | `python agent_github.py` |

Each agent is ~25 lines. Same pattern, different tools.

## The Pattern

```python
while True:
    response = llm.call(messages, tools)
    if response.done: break
    result = execute(response.tool_call)
    messages.append(result)
```

## Setup

```bash
pip install boto3 requests beautifulsoup4
```

Requires AWS credentials with Bedrock access.

## Also

`mini.py` - Chatbot with Confluence access (requires Chainlit + Atlassian SDK)
