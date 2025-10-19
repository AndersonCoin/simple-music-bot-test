# bot.py
"""Simple test bot with health check"""
from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv
import logging
from threading import Thread  # ✅ إضافة
from aiohttp import web  # ✅ إضافة
import asyncio  # ✅ إضافة

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not API_ID or not API_HASH or not BOT_TOKEN:
    logger.error("❌ Missing configuration!")
    exit(1)

# Create bot
app = Client(
    name="SimpleTestBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

logger.info("=" * 50)
logger.info("Simple Test Bot")
logger.info("=" * 50)


# ✅ Health check server (NEW!)
async def health_handler(request):
    """Health endpoint for Render."""
    return web.Response(text="Bot is running! 🤖✅", status=200)

def start_health_server():
    """Start health check server in background."""
    async def run_server():
        health_app = web.Application()
        health_app.router.add_get('/', health_handler)
        health_app.router.add_get('/health', health_handler)
        
        port = int(os.getenv('PORT', '8080'))
        runner = web.AppRunner(health_app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        
        logger.info(f"✓ Health server started on port {port}")
        
        # Keep server running
        while True:
            await asyncio.sleep(3600)
    
    # Run in separate thread
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_server())
    
    thread = Thread(target=run_in_thread, daemon=True)
    thread.start()


# Handler 1: Start command
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command."""
    logger.info(f"✅ /start from {message.from_user.id}")
    
    await message.reply_text(
        "👋 **Hello! I'm working!**\n\n"
        "✅ Bot is receiving messages!\n"
        "✅ Pyrogram is working!\n"
        "✅ Render deployment successful!\n\n"
        "Try these commands:\n"
        "• /ping - Test response\n"
        "• /info - Your info\n"
        "• Send me any text!"
    )


# Handler 2: Ping command
@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Handle /ping command."""
    logger.info(f"🏓 /ping from {message.from_user.id}")
    await message.reply_text("🏓 **Pong!** Bot is alive!")


# Handler 3: Info command
@app.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    """Handle /info command."""
    logger.info(f"ℹ️ /info from {message.from_user.id}")
    
    user = message.from_user
    chat = message.chat
    
    info_text = (
        f"ℹ️ **Your Information:**\n\n"
        f"**User ID:** `{user.id}`\n"
        f"**Username:** @{user.username or 'None'}\n"
        f"**First Name:** {user.first_name}\n"
        f"**Chat Type:** {chat.type}\n"
        f"**Chat ID:** `{chat.id}`"
    )
    
    await message.reply_text(info_text)


# Handler 4: Echo any text
@app.on_message(filters.text & filters.private)
async def echo_text(client: Client, message: Message):
    """Echo any text message."""
    logger.info(f"💬 Text from {message.from_user.id}: {message.text[:50]}")
    
    await message.reply_text(
        f"✅ **I received your message!**\n\n"
        f"You said: _{message.text}_\n\n"
        f"This proves the bot is working perfectly! 🎉"
    )


# Handler 5: Catch everything (for debugging)
@app.on_message(filters.all)
async def debug_handler(client: Client, message: Message):
    """Log all messages for debugging."""
    user_id = message.from_user.id if message.from_user else "Unknown"
    chat_type = message.chat.type
    text = message.text if message.text else "[media/other]"
    
    logger.info(f"📨 Message: user={user_id}, chat={chat_type}, text={text[:30]}")


# Main
if __name__ == "__main__":
    logger.info("🚀 Starting bot...")
    logger.info(f"📱 API_ID: {API_ID}")
    logger.info(f"🔑 BOT_TOKEN: {BOT_TOKEN[:20]}...")
    
    # ✅ Start health server (NEW!)
    start_health_server()
    
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
