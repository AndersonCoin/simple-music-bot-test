# 🤖 Simple Test Bot

Ultra simple Telegram bot to test if everything works!

## 🎯 Purpose

- ✅ Test Render deployment
- ✅ Verify API credentials
- ✅ Confirm bot receives messages
- ✅ Debug basic functionality

## 🚀 Quick Start

### 1. Get Credentials

#### API_ID & API_HASH:
1. Go to https://my.telegram.org
2. Login with your phone number
3. Go to "API development tools"
4. Create an app
5. Copy `api_id` and `api_hash`

#### BOT_TOKEN:
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Follow instructions
4. Copy the token

### 2. Local Testing

```bash
# Clone
git clone https://github.com/YourUsername/simple-test-bot
cd simple-test-bot

# Create .env
cp .env.example .env
# Edit .env with your credentials

# Install
pip install -r requirements.txt

# Run
python bot.py
