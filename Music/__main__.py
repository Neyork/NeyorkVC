import asyncio
import time
import uvloop
import importlib
from pyrogram import Client
from Music.config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID
from Music import BOT_NAME, ASSNAME, app, client
from Music.MusicUtilities.database.functions import clean_restart_stage
from Music.MusicUtilities.database.queue import (get_active_chats, remove_active_chat)
from Music.MusicUtilities.tgcallsrun import run
from pytgcalls import idle
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time

Client(
    ':Music:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Music.Plugins'},
).start()


print(f"[INFO]: بدا البوت AS {BOT_NAME}!")
print(f"[INFO]: بدا الحساب المساعد AS {ASSNAME}!")



async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: إرسال حالة إعادة التشغيل إلى خادم Neyork")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**تم اعاده تشغيل البوت بنجاح.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("حدث خطأ أثناء مسح ديسيبل")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)                                         
        except Exception as e:
            print("حدث خطأ أثناء مسح ديسيبل")
            pass     
    await app.send_message(LOG_GROUP_ID, "تم بدا بوت نيورك للموسيقي بنجاح")
    await client.send_message(LOG_GROUP_ID, "تم بدا الحساب المساعد ل بوت نيورك  بنجاح")
    print("[INFO]: تم تنصيب بوت نيورك علي سورس نيورك بنجاح")
    
   
loop = asyncio.get_event_loop()
loop.run_until_complete(load_start())

run()
idle()
loop.close()

print("[LOG] CLOSING THE YUI MUSIC BOT")
