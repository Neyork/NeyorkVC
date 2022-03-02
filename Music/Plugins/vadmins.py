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
            "انت مشرف محدش يعرفك! \ n \ n »دي من حق المعلم المشرف الجامد فنفسه كده."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    await query.edit_message_text(
        f"⚙️ إعدادات من {query.message.chat.title} \ n \ n II: وقف التشغيل شويه \ n ▷: كمل التشغيل \ n🔇: كتم صوت المساعد صحبي \ n🔊: كتم صوت المساعد صحبي \ n▢: وقف ام التشغيل خالص وريحنا",
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
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
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
            await m.reply("مفيش حاجه شغاله ✖️")
        elif op == 1:
            await m.reply(
                "✅ __Antrian__ **فارغ.**\n\n**• نزل المساعد من الكول خلصه يبا**"
            )
        elif op == 2:
            await m.reply(
                "🗑️ **بنضفلك قايمه الانتظار اهو احلا مسا عليك**\n\n**• نزل المساعد زميلي من الكول يبا**"
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
        OP = "🗑 **مسحتلك الاغنيه من القايمه يبا خلصه تؤمور بحاجه تاني؟:**"
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


@app.on_message(command(["vend"]) & filters.group)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✔️ **ادينا وقفنا تشغيل لما نشوف اخرتها.**")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ **مفيش يبا حاجه شغاله**")


@app.on_message(command(["vpause"]) & filters.group)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "II **وقفنا ام الفيديو اهو.**\n\n• ** عشان تشغل تاني ، استخدم الأوامر يبا** » /vresume"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ **مفيش يبا حاجه شغاله**")


@app.on_message(command(["vresume"]) & filters.group)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▷ **كمل الي كنت مشغله.**\n\n• **عشان توقف الفيديو شويه ، استخدم الأمر دا يبا** » /vpause"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ **مفيش يبا حاجه شغاله**")


@app.on_message(command(["vmute"]) & filters.group)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **كتمت صوت المساعد زميلي.**\n\n• **لو عاوز تخليه يغني تاني ، دوس علي  الأمر دا**\n» /vunmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ **مفيش يبا حاجه شغاله**")


@app.on_message(command(["vunmute"]) & filters.group)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **المساعد رجع يتكلم تاني خلصانه.**\n\n• **لو عاوز توقف صوته تاني ، استخدم الامر دا **\n» /vmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ **مفيش يبا حاجه شغاله**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "طيب **انت ادمن محدش يعرفك اصلا** !\n\n» عشان توصل للحساب دا من حق الادمن عم الجروب."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text("II وقفت التشغيل شويه", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("✖️ مفيش حاجه شغاله يبني", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "طيب **انت ادمن محدش يعرفك اصلا** !\n\n» عشان توصل للحساب دا من حق الادمن عم الجروب."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▷ شغلنا من تاني", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("✖️ مفيش حاجه شغاله يبني", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "طيب **انت ادمن محدش يعرفك اصلا** !\n\n» عشان توصل للحساب دا من حق الادمن عم الجروب."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text(
                "✅ **خلص التشغيل يبا**", reply_markup=bcl
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("✖️ مفيش حاجه شغاله يبني", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "طيب **انت ادمن محدش يعرفك اصلا** !\n\n» عشان توصل للحساب دا من حق الادمن عم الجروب."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 وقفتلك المساعد زميلي خلاص", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"***Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("✖️ مفيش حاجه شغاله يبني", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "طيب **انت ادمن محدش يعرفك اصلا** !\n\n» عشان توصل للحساب دا من حق الادمن عم الجروب."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "🦾 المشرف الي عنده صلاحيه اداره الكول هوا الي يدوس ع الزار متتعبونيش معاكم بق فل!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 بدا المساعد زميلي من تاني خلصانه", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("✖️ مفيش حاجه شغاله يبني", show_alert=True)


@app.on_message(command(["volume", "vol"]))
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(f"✅ **ظبطلك الصوت يبا علي** `{range}`%")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("✖️ مفيش حاجه شغاله يبني")
