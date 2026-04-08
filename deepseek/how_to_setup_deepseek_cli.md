# How to Setup DeepSeek with GitHub Copilot CLI

This guide shows you how to configure GitHub Copilot CLI to use DeepSeek models instead of the default Claude/GPT models.

## Prerequisites

1. **GitHub Copilot CLI** installed (`npm install -g @githubnext/github-copilot-cli`)
2. **DeepSeek API key** from https://platform.deepseek.com/api_keys

## Quick Setup (One-Time)

Add this to your `~/.zshrc` (or `~/.bashrc`):

```bash
# DeepSeek Copilot CLI Configuration
export DEEPSEEK_API_KEY="sk-your-actual-api-key-here"  # Replace with your key

# DeepSeek Copilot CLI function
deepseek-copilot() {
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        echo "Error: DEEPSEEK_API_KEY is not set"
        echo "Get your API key from: https://platform.deepseek.com/api_keys"
        echo "Then run: export DEEPSEEK_API_KEY=\"sk-your-key\""
        return 1
    fi
    
    COPILOT_PROVIDER_BASE_URL="https://api.deepseek.com/v1" \
    COPILOT_PROVIDER_TYPE="openai" \
    COPILOT_PROVIDER_API_KEY="$DEEPSEEK_API_KEY" \
    COPILOT_MODEL="deepseek-chat" \
    copilot "$@"
}
```

After adding, reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Alternative: Simple Alias

If you prefer a simpler approach, add this instead:

```bash
# Simple alias (requires DEEPSEEK_API_KEY to be set)
alias deepseek-copilot='COPILOT_PROVIDER_BASE_URL="https://api.deepseek.com/v1" COPILOT_PROVIDER_TYPE="openai" COPILOT_PROVIDER_API_KEY="$DEEPSEEK_API_KEY" COPILOT_MODEL="deepseek-chat" copilot'
```

## Usage Examples

### Basic Usage
```bash
# Set your API key (if not in .zshrc)
export DEEPSEEK_API_KEY="sk-your-actual-key"

# Interactive mode
deepseek-copilot

# With a specific prompt
deepseek-copilot -p "Write a Python function to calculate moving average"

# Help with backtesting
deepseek-copilot -p "Help me optimize my Bitcoin momentum strategy"
```

### Advanced Configuration

#### Different DeepSeek Models
```bash
# Use deepseek-reasoner for complex tasks
deepseek-copilot-reasoner() {
    COPILOT_PROVIDER_BASE_URL="https://api.deepseek.com/v1" \
    COPILOT_PROVIDER_TYPE="openai" \
    COPILOT_PROVIDER_API_KEY="$DEEPSEEK_API_KEY" \
    COPILOT_MODEL="deepseek-reasoner" \
    copilot "$@"
}
```

#### Custom Token Limits
```bash
# Higher token limits for longer conversations
deepseek-copilot-long() {
    COPILOT_PROVIDER_BASE_URL="https://api.deepseek.com/v1" \
    COPILOT_PROVIDER_TYPE="openai" \
    COPILOT_PROVIDER_API_KEY="$DEEPSEEK_API_KEY" \
    COPILOT_MODEL="deepseek-chat" \
    COPILOT_PROVIDER_MAX_PROMPT_TOKENS=16384 \
    COPILOT_PROVIDER_MAX_OUTPUT_TOKENS=8192 \
    copilot "$@"
}
```

## Verification

Test that it's working:
```bash
# Check version (should show GitHub Copilot CLI version)
deepseek-copilot --version

# Simple test
deepseek-copilot -p "Say hello"

# Verify model usage (check output for "deepseek-chat" in breakdown)
deepseek-copilot -p "What model are you using?"
```

## Troubleshooting

### "Command not found: deepseek-copilot"
- Make sure you added the function to `~/.zshrc` (or `~/.bashrc`)
- Run `source ~/.zshrc` to reload
- Check spelling: `type deepseek-copilot` should show it's a function

### Authentication Errors
1. Verify your API key at https://platform.deepseek.com/api_keys
2. Check if you have sufficient credits/balance
3. Ensure API key is properly exported: `echo $DEEPSEEK_API_KEY`

### "copilot: command not found"
- Install GitHub Copilot CLI: `npm install -g @githubnext/github-copilot-cli`
- Verify installation: `which copilot`

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEEPSEEK_API_KEY` | Your DeepSeek API key | `sk-dc95d2219b4e44a28534e54355c6b468` |
| `COPILOT_PROVIDER_BASE_URL` | DeepSeek API endpoint | `https://api.deepseek.com/v1` |
| `COPILOT_PROVIDER_TYPE` | API type (OpenAI-compatible) | `openai` |
| `COPILOT_MODEL` | DeepSeek model to use | `deepseek-chat` or `deepseek-reasoner` |
| `COPILOT_PROVIDER_MAX_PROMPT_TOKENS` | Max input tokens | `8192` (default) |
| `COPILOT_PROVIDER_MAX_OUTPUT_TOKENS` | Max output tokens | `4096` (default) |

## Comparison with Default Models

| Aspect | DeepSeek | Claude/GPT (Default) |
|--------|----------|---------------------|
| **Cost** | Very affordable | More expensive |
| **Speed** | Fast responses | Variable |
| **Code Quality** | Excellent for Python | Good |
| **Context Window** | Up to 128K | 200K (Claude) |
| **API Compatibility** | OpenAI-compatible | Native |

## Security Notes

1. **Never commit API keys** to version control
2. Use environment variables or secure credential storage
3. Consider using a `.env` file (add to `.gitignore`):
   ```bash
   # .deepseek.env
   DEEPSEEK_API_KEY="sk-your-key"
   
   # Source it
   source .deepseek.env
   ```

## Removing the Setup

To remove DeepSeek configuration:
1. Remove the function/alias from `~/.zshrc`
2. Remove `DEEPSEEK_API_KEY` export
3. Run `source ~/.zshrc`

## Need Help?

- DeepSeek API Docs: https://platform.deepseek.com/api-docs
- GitHub Copilot CLI Docs: `copilot --help`
- Model availability: Check https://platform.deepseek.com for latest models