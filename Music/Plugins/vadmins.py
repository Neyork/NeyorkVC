from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Music import app
from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py

from Music.MusicUtilities.helpers.decorators import authorized_users_only
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.tgcallsrun.queues import QUEUE, clear_queue
from Music.MusicUtilities.tgcallsrun.video import skip_current_song, skip_item


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup([[InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")]])


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنت مسؤول مجهول! \ n \ n »رجوع إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن إدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    await query.edit_message_text(
        f"⚙️ إعدادات من {query.message.chat.title} \ n \ n II: إيقاف البث مؤقتًا \ n ▷: استئناف البث \ n🔇: مساعد كتم الصوت \ n🔊: مساعد كتم الصوت \ n▢: إيقاف البث",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▢", callback_data="cbstop"),
                    InlineKeyboardButton("II", callback_data="cbpause"),
                    InlineKeyboardButton("▷", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("🔇", callback_data="cbmute"),
                    InlineKeyboardButton("🔊", callback_data="cbunmute"),
                ],
                [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    await query.message.delete()


@app.on_message(command(["vskip"]) & filters.group)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="cbmenu"),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ لا شيء يلعب")
        elif op == 1:
            await m.reply(
                "✅ __Antrian__ **فارغ.**\n\n**• غادر المساعد الدردشة الصوتية**"
            )
        elif op == 2:
            await m.reply(
                "🗑️ **تنظيف قائمة الانتظار**\n\n**• غادر المساعد الدردشة الصوتية**"
            )
        else:
            await m.reply(
                f"""
⏭️ **تحريف {op[2]} التالي**
🏷 **اسم:** [{op[0]}]({op[1]})
🎧 **عند الطلب:** {m.from_user.mention()}
""",
                disable_web_page_preview=True,
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **تمت إزالة الأغنية من قائمة الانتظار:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@app.on_message(command(["vstop"]) & filters.group)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ **انتهى الدفق.**")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")


@app.on_message(command(["vpause"]) & filters.group)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "II **توقف الفيديو مؤقتًا.**\n\n• **لاستئناف الفيديو ، استخدم الأوامر** » /vresume"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")


@app.on_message(command(["vresume"]) & filters.group)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▷ **تابع الفيديو.**\n\n• **لإيقاف مقطع فيديو مؤقتًا ، استخدم الأمر** » /vpause"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")


@app.on_message(command(["vmute"]) & filters.group)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **تم كتم صوت المساعد.**\n\n• **لتنشيط صوت المساعد ، استخدم الأمر**\n» /vunmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")


@app.on_message(command(["vunmute"]) & filters.group)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **تم تنشيط المساعد.**\n\n• **لتعطيل روبوتات المستخدم ، استخدم الأوامر**\n» /vmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنتم **Admin Anonim** !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text("II تم إيقاف البث مؤقتًا", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لا شيء يتدفق", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنتم **مشرف مجهول** !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▷ تم استئناف البث", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لا شيء يتدفق", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنتم **مشرف مجهول** !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text(
                "✅ **انتهى الدفق**", reply_markup=bcl
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لا شيء يتدفق", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنتم **مشرف مجهول** !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 تم إيقاف المساعد بنجاح", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"***Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لا شيء يتدفق", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "أنتم **مشرف مجهول** !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 يمكن للمسؤولين الذين لديهم إذن بإدارة الدردشة الصوتية فقط النقر فوق هذا الزر!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 بدا المساعد بنجاح", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لا شيء يتدفق", show_alert=True)


@app.on_message(command(["volume", "vol"]))
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(f"✅ **تم ضبط الحجم على** `{range}`%")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ليس في الدفق**")
