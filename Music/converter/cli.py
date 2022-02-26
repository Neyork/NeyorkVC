from Music.config import API_HASH, API_ID, BOT_TOKEN, SESSION_NAME
from pyrogram import Client

app = Client(
    "MusicMusicBot",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
)

if not LOG_SESSION:
    LOG_CLIENT = None
else:
    LOG_CLIENT = Client(LOG_SESSION, API_ID, API_HASH)
