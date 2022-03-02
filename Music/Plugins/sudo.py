from Music import app, OWNER
import os
import subprocess
import shutil
import re
import sys
import traceback
from Music.MusicUtilities.database.sudo import (
    get_sudoers,
    get_sudoers,
    remove_sudo,
    add_sudo,
)
from pyrogram import filters, Client
from pyrogram.types import Message

@app.on_message(filters.command("addmsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ الرد على رسالة المستخدم أو العطاء username/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user 
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("✅ حصل مستخدم معروف.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(f"✅ Added **{user.mention}** as a مستخدم مميز عن المطور نيورك عم العالم")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await edit_or_reply(message, text="في حاجه غلط ارجع للسجلات او اللوجز ✖️")  
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("✅ حصل مستخدم معروف.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"✅ Added **{mention}** as a مستخدم مميز عن المطور نيورك عم العالم")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await edit_or_reply(message, text="في حاجه غلط ارجع للسجلات او اللوجز ✖️")  
    return    
          
              
@app.on_message(filters.command("delmsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ الرد على رسالة المستخدم أو العطاء username/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user      
        if user.id not in await get_sudoers():
            return await message.reply_text(f"ليس جزء من المستخدمين المميزين ✖️ ")        
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"✅ مسحت **{user.mention}** من المستخدمين المميزين عند المعلم نيورك.")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await message.reply_text(f"في حاجه غلط يا زميلي ✖️.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"ليس جزء من المستخدمين المميزين ✖️")        
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"✅ مسحت {user.mention} من المستخدمين المميزين عند المعلم نيورك.")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await message.reply_text(f"في حاجه غلط يا زميلي ✖️.")
                
                          
@app.on_message(filters.command("msudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**__Sudo Users List of Neyork:-__**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:                     
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue                     
        text += f"➤ {user}\n"
    if not text:
        await message.reply_text("مفيش مستخدمين مميزين يبا 🙂")  
    else:
        await message.reply_text(text) 
