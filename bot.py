# bot.py
"""
Simple Music Bot - Phase 1: PyTgCalls + User Client
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
import os
from dotenv import load_dotenv
import logging
from threading import Thread
from aiohttp import web
import asyncio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Validate config
if not all([API_ID, API_HASH, BOT_TOKEN, SESSION_STRING]):
    logger.error("❌ Missing configuration! Check environment variables")
    logger.error(f"API_ID: {'✓' if API_ID else '✗'}")
    logger.error(f"API_HASH: {'✓' if API_HASH else '✗'}")
    logger.error(f"BOT_TOKEN: {'✓' if BOT_TOKEN else '✗'}")
    logger.error(f"SESSION_STRING: {'✓' if SESSION_STRING else '✗'}")
    exit(1)

logger.info("=" * 60)
logger.info("Simple Music Bot - Phase 1")
logger.info("=" * 60)

# Create bot client
bot_app = Client(
    name="MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Create user client (assistant)
user_app = Client(
    name="UserBot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Create PyTgCalls instance
pytgcalls = PyTgCalls(user_app)


# Health check server
async def health_handler(request):
    """Health endpoint for Render."""
    return web.Response(text="Music Bot is running! 🎵✅", status=200)

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
        
        while True:
            await asyncio.sleep(3600)
    
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_server())
    
    thread = Thread(target=run_in_thread, daemon=True)
    thread.start()


# ============================================================
# HANDLERS
# ============================================================

@bot_app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command."""
    logger.info(f"✅ /start from {message.from_user.id}")
    
    await message.reply_text(
        "🎵 **Music Bot - Phase 1**\n\n"
        "✅ Bot client: Running\n"
        "✅ User client: Running\n"
        "✅ PyTgCalls: Running\n\n"
        "**Available Commands:**\n"
        "• `/start` - Show this message\n"
        "• `/ping` - Test bot\n"
        "• `/status` - Check clients status\n"
        "• `/assistant` - Show assistant info\n\n"
        "🔜 Coming soon: /play command!"
    )


@bot_app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Handle /ping command."""
    logger.info(f"🏓 /ping from {message.from_user.id}")
    await message.reply_text("🏓 **Pong!** All systems operational!")


@bot_app.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """Check all clients status."""
    logger.info(f"📊 /status from {message.from_user.id}")
    
    status_text = "📊 **System Status:**\n\n"
    
    # Bot client
    try:
        bot_me = await bot_app.get_me()
        status_text += f"✅ **Bot:** @{bot_me.username} (ID: {bot_me.id})\n"
    except Exception as e:
        status_text += f"❌ **Bot:** Error - {e}\n"
    
    # User client
    try:
        user_me = await user_app.get_me()
        status_text += f"✅ **Assistant:** @{user_me.username} (ID: {user_me.id})\n"
    except Exception as e:
        status_text += f"❌ **Assistant:** Error - {e}\n"
    
    # PyTgCalls
    try:
        status_text += f"✅ **PyTgCalls:** Active\n"
    except Exception as e:
        status_text += f"❌ **PyTgCalls:** Error - {e}\n"
    
    status_text += f"\n🎵 **Ready for voice chat streaming!**"
    
    await message.reply_text(status_text)


@bot_app.on_message(filters.command("assistant"))
async def assistant_command(client: Client, message: Message):
    """Show assistant info."""
    logger.info(f"ℹ️ /assistant from {message.from_user.id}")
    
    try:
        user_me = await user_app.get_me()
        
        info_text = (
            f"🤖 **Assistant Information:**\n\n"
            f"**Username:** @{user_me.username}\n"
            f"**ID:** `{user_me.id}`\n"
            f"**First Name:** {user_me.first_name}\n"
            f"**Status:** ✅ Online\n\n"
            f"ℹ️ This account joins voice chats to play music."
        )
        
        await message.reply_text(info_text)
    except Exception as e:
        await message.reply_text(f"❌ Error getting assistant info: {e}")


@bot_app.on_message(filters.all)
async def debug_handler(client: Client, message: Message):
    """Log all messages."""
    user_id = message.from_user.id if message.from_user else "Unknown"
    text = message.text if message.text else "[media]"
    logger.info(f"📨 Message from {user_id}: {text[:30]}")


# ============================================================
# MAIN
# ============================================================

async def main():
    """Main function to start all clients."""
    logger.info("🚀 Starting Music Bot...")
    logger.info(f"📱 API_ID: {API_ID}")
    logger.info(f"🔑 BOT_TOKEN: {BOT_TOKEN[:20]}...")
    logger.info(f"🔐 SESSION_STRING: {SESSION_STRING[:30]}...")
    
    try:
        # Start health server
        start_health_server()
        
        # Start bot client
        await bot_app.start()
        bot_me = await bot_app.get_me()
        logger.info(f"✅ Bot started: @{bot_me.username}")
        
        # Start user client
        await user_app.start()
        user_me = await user_app.get_me()
        logger.info(f"✅ Assistant started: @{user_me.username}")
        
        # Start PyTgCalls
        await pytgcalls.start()
        logger.info(f"✅ PyTgCalls started")
        
        logger.info("=" * 60)
        logger.info("🎵 Music Bot Phase 1 - Ready!")
        logger.info("=" * 60)
        
        # Keep running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
    finally:
        # Cleanup
        try:
            await pytgcalls.stop()
            await user_app.stop()
            await bot_app.stop()
            logger.info("👋 Stopped gracefully")
        except:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Stopped by user")
