import asyncio
import yt_dlp
import psutil

from Music.config import SUPPORT_GROUP, UPDATES_CHANNEL
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from youtubesearchpython import VideosSearch
from Music.MusicUtilities.database.assistant import (_get_assistant, get_as_names, get_assistant,
                        save_assistant)
from Music.MusicUtilities.database.auth import (_get_authusers, add_nonadmin_chat, delete_authuser,
                   get_authuser, get_authuser_count, get_authuser_names,
                   is_nonadmin_chat, remove_nonadmin_chat, save_authuser)
from Music.MusicUtilities.database.blacklistchat import blacklist_chat, blacklisted_chats, whitelist_chat
from Music.MusicUtilities.helpers.inline import personal_markup, setting_markup
from Music.MusicUtilities.helpers.inline import (custommarkup, dashmarkup, setting_markup,
                          start_pannel, usermarkup, volmarkup)
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.tgcallsrun.music import pytgcalls
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/NeyorkSupport"),
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/NeyorkUpdate"),
        ],
        [
            InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅ​", url="https://telegra.ph/Neyork-02-02"),
        ],
        [
            InlineKeyboardButton("Neyork", url="https://t.me/lIPyl"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} Merupakan salah satu dari bot telegram yang bisa memutar musik di grup**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ ᴀᴅᴅ ᴍᴇ ʏᴏᴜʀ ᴛᴏ ɢʀᴏᴜᴘ​ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text="✨ sᴜᴘᴘᴏʀᴛ​", url="https://t.me/NeyorkSupport"),
            InlineKeyboardButton("✨ ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/NeyorkUpdate"),
        ],
        [
            InlineKeyboardButton("📚 ᴄᴏᴍᴍᴀɴᴅ ​📚", url="https://telegra.ph/Neyork-02-02"),
        ],
        [
            InlineKeyboardButton("Neyork", url="https://t.me/lIPyl"),
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"💡 ملكي [{member.mention}] انضم للتو إلى هذه المجموعة."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"💡 المسؤول عن البوت [{member.mention}] انضم للتو إلى هذه المجموعة."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 ** مرحبًا ، من الجيد أن تكون قادرًا على الانضمام إلى هذه المجموعة**
💡 **لا تنس أن تجعلني مشرفًا في هذه المجموعة**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


#@Client.on_message(
#    filters.group
#    & filters.command(
#        ["mstart", "mhelp", f"mstart@{BOT_USERNAME}", f"mhelp@{BOT_USERNAME}"]
#    )
#)
#async def start(_, message: Message):
#    chat_id = message.chat.id
#    out = start_pannel()
#    await message.reply_text(
#        f"""
#Terima kasih telah memasukkan saya di {message.chat.title}.
#Musik itu hidup.
#Untuk bantuan silahkan klik tombol dibawah.
#""",
#       reply_markup=InlineKeyboardMarkup(out[1]),
#        disable_web_page_preview=True
#    )
#    return


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "**__Sudo Users List of Bot:-__**\n\n"
            j = 0
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                except Exception:
                    continue
                text += f"➤ {user}\n"
                j += 1
            if j == 0:
                await message.reply_text("No Sudo Users")
            else:
                await message.reply_text(text)
        if name[0] == "i":
            m = await message.reply_text("🔎 إحضار المعلومات!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍 __**معلومات مسار الفيديو**__
❇️ **لقب:** {title}
⏳ **مده التشغيل:** {duration} Mins
👀 **المشاهدات:** `{views}`
⏰ **وقت النشر:** {published}
🎥 **اسم القناه:** {channel}
📎 **رابط القناه:** [Visit From Here]({channellink})
🔗 **رابط الفيديو:** [Link]({link})
⚡️ __تم البحث بواسطه {BOT_NAME}t__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Watch Youtube Video", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="• Cʟᴏsᴇ •", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )

@app.on_message(filters.command("setting") & filters.group)
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup()
    await asyncio.gather(
        message.delete(),
        message.reply_text(f"{text}\n\n**Group:** {message.chat.title}\n**Group ID:** {message.chat.id}\n**Volume Level:** {volume}%", reply_markup=InlineKeyboardMarkup(buttons)),
    )

@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("Going Back ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"شكرا لإضافتي {CallbackQuery.message.chat.title}.\n{BOT_NAME} Telah online.\n\nإذا كنت بحاجة إلى مساعدة أو كانت هناك مشكلة في الروبوت ، فيرجى الانضمام إلى مجموعتنا أو قناتنا.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )

@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Settings ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(filters.regex("EVE"))
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Changes Saved")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nيقوم المسؤولون بوضع الأوامر إلى **Everyone**\n\nالآن يمكن لأي شخص موجود في هذه المجموعة تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها.\n\nالتغييرات التي تم إجراؤها بواسطة @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "تم بالفعل تعيين وضع الأوامر على الجميع", show_alert=True
        )

@app.on_callback_query(filters.regex("AMS"))
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "تم بالفعل تعيين وضع الأوامر على ADMINS فقط", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nاضبط وضع الأوامر على **Admins**\n\nالآن يمكن للمشرفين الموجودين في هذه المجموعة فقط تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها.\n\nالتغييرات التي تم إجراؤها بواسطة @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("بالفعل في أفضل جودة", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("إعدادات البوت ...")
        text, buttons = volmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("إعدادات البوت ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n\nCurrently Who Can Use {BOT_NAME}:- **{current}**\n\n**⁉️ What is This?**\n\n**👥 Everyone :-**Anyone can use {BOT_NAME}'s commands(skip, pause, resume etc) present in this group.\n\n**🙍 Admin Only :-**  Only the admins and authorized users can use all commands of {BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        text, buttons = dashmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n\nCheck {BOT_NAME}'s System Stats In the DashBoard Here! More Functions adding very soon! Keep on Checking Support Channel.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = custommarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nلا يوجد مستخدمون مصرح لهم Found\n\nيمكنك السماح لأي شخص غير مسؤول باستخدام أوامر المسؤول الخاصة بي عن طريق /auth وحذف باستخدام /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "إحضار المستخدمين المصرح لهم ... الرجاء الانتظار"
            )
            msg = f"**قائمة المستخدمين المعتمدين[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"وقت تشغيل بوت: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's استخدام وحدة المعالجة المركزية: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's استخدام الذاكرة: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"إستخدام القرص: {diske}%", show_alert=True
        )
