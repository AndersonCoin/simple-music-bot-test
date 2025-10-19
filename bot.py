# bot.py
"""
ULTRA Simple Test Bot - 30 lines of code!
This will definitely work.
"""
from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Config
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create bot
app = Client(
    name="UltraSimpleBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True  # ✅ لا يكتب ملفات session
)

# Catch-all handler
@app.on_message()
async def catch_all(client: Client, message: Message):
    """Respond to EVERYTHING."""
    print(f"🔥🔥🔥 GOT MESSAGE: {message.text}")
    
    # الرد
    await message.reply_text(
        f"✅ **I'm working!**\n\n"
        f"I received: `{message.text}`"
    )

# Run bot
print("🚀 Starting ultra simple bot...")
app.run()
