# bot.py
"""
ULTRA Simple Test Bot - With Health Check for Web Service
"""
from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv
import logging
from aiohttp import web
import asyncio

# Load env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

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
    in_memory=True
)

# Catch-all handler
@app.on_message()
async def catch_all(client: Client, message: Message):
    """Respond to EVERYTHING."""
    logger.info(f"🔥🔥🔥 GOT MESSAGE: {message.text}")
    print(f"🔥🔥🔥 GOT MESSAGE: {message.text}")
    
    # الرد
    await message.reply_text(
        f"✅ **I'm working!**\n\n"
        f"I received: `{message.text}`"
    )

# Health check server
async def health_handler(request):
    """Health endpoint for Render."""
    return web.Response(text="Bot is running! 🤖✅", status=200)

async def start_server():
    """Start health check server."""
    health_app = web.Application()
    health_app.router.add_get('/', health_handler)
    health_app.router.add_get('/health', health_handler)
    
    port = int(os.getenv('PORT', '8080'))
    runner = web.AppRunner(health_app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"✓ Health server started on port {port}")

# Main function
async def main():
    """Start bot and health server."""
    logger.info("🚀 Starting ultra simple bot...")
    
    # Start bot and server concurrently
    await asyncio.gather(
        start_server(),
        app.start()
    )
    
    logger.info("✓ Bot started!")
    
    # Keep running
    await asyncio.Event().wait()


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped")
