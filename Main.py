import os
from pyrogram import Client, filters
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

# Config
API_ID = os.getenv("37035754")
API_HASH = os.getenv("2dedce4e90d79c47de25aa62b175e095")
BOT_TOKEN = os.getenv("8587508036:AAFuYPOGQiyrWgrEwLa3l6BTpaBLTJ2QSCM")

app = FastAPI()
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video | filters.document)
async def gen_link(client, message):
    # Railway URL + Message ID का लिंक बनाना
    stream_link = f"https://your-railway-url.app{message.id}"
    await message.reply_text(f"🎥 **Stream Link:** {stream_link}\n\n📥 **Direct Download:** {stream_link}?download=true")

# Streaming Endpoint
@app.get("/stream/{message_id}")
async def stream_video(message_id: int, download: bool = False):
    msg = await bot.get_messages(chat_id="3410745884", message_ids=message_id)
    
    async def generate_chunks():
        async for chunk in bot.stream_media(msg):
            yield chunk

    headers = {}
    if download:
        headers["Content-Disposition"] = f"attachment; filename=video.mp4"
    
    return StreamingResponse(generate_chunks(), media_type="video/mp4", headers=headers)
