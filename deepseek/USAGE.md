# DeepSeek CLI Usage (Current Setup)

## Quick Start

Your DeepSeek is already configured! Just use:

```bash
deepseek-copilot
```

## What's Set Up

1. **API Key**: `sk-dc95d2219b4e44a28534e54355c6b468` (in `~/.zshrc`)
2. **Alias**: `deepseek-copilot` ready to use
3. **Model**: Using `deepseek-chat`
4. **Status**: ✅ **WORKING** (tested and verified)

## Basic Commands

```bash
# Interactive chat
deepseek-copilot

# Single prompt
deepseek-copilot -p "Write Python code for RSI indicator"

# Help with backtesting
deepseek-copilot -p "Optimize my Bitcoin momentum strategy"

# Version check
deepseek-copilot --version
```

## Verify It's Working

Run any command and check output for:
```
Breakdown by AI model:
 deepseek-chat            ... in, ... out, 0 cached
```

## Files in This Directory

- `copilot-deepseek` - Alternative script (optional)
- `how_to_setup_deepseek_cli.md` - Detailed setup guide
- `USAGE.md` - This quick reference

## Troubleshooting

### "Command not found"
```bash
source ~/.zshrc
```

### API errors
1. Check key: `echo $DEEPSEEK_API_KEY`
2. Get new key: https://platform.deepseek.com/api_keys
3. Update `~/.zshrc` with new key

### Switch back to default models
```bash
# Just use regular copilot
copilot
```

## Notes

- DeepSeek won't show in "Select Model" menu (BYOK mode)
- You're billed directly by DeepSeek, not GitHub
- Cost: Very affordable (~$0.14 per 1M tokens)

## Need Help?
- DeepSeek API: https://platform.deepseek.com
- Copilot CLI: `copilot --help`
- Your config: `grep -A2 "DeepSeek" ~/.zshrc`