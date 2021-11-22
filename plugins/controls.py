from utils import LOGGER
from pyrogram.types import Message
from config import Config
from pyrogram import (
    Client, 
    filters
)
from utils import (
    clear_db_playlist, 
    get_playlist_str, 
    is_admin, 
    mute, 
    restart_playout, 
    settings_panel, 
    skip, 
    pause, 
    resume, 
    unmute, 
    volume, 
    get_buttons, 
    is_admin, 
    seek_file, 
    delete_messages,
    chat_filter,
    volume_buttons
)

admin_filter=filters.create(is_admin)   

@Client.on_message(filters.command(["playlist", f"playlist@{Config.BOT_USERNAME}"]) & chat_filter)
async def player(client, message):
    if not Config.CALL_STATUS:
        await message.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([message])
        return
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            disable_web_page_preview=True,
            reply_markup=await get_buttons(),
        )
    else:
        if Config.msg.get('player') is not None:
            await Config.msg['player'].delete()
        Config.msg['player'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
            reply_markup=await get_buttons(),
        )
    await delete_messages([message])

@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def skip_track(_, m: Message):
    msg=await m.reply('trying to skip from queue..')
    if not Config.CALL_STATUS:
        await msg.edit(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.playlist:
        await msg.edit("Playlist is Empty.")
        await delete_messages([m, msg])
        return
    if len(m.command) == 1:
        await skip()
    else:
        #https://github.com/callsmusic/tgvc-userbot/blob/dev/plugins/vc/player.py#L268-L288
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    await msg.edit(f"🗑️ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴘʟᴀʏʟɪꜱᴛ - {i}. **{Config.playlist[i][1]}**")
                    await clear_db_playlist(song=Config.playlist[i])
                    Config.playlist.pop(i)
                    await delete_messages([m, msg])
                else:
                    await msg.edit(f"🙅‍♂️ ʜᴇʏ!! ʏᴏᴜ ᴄᴀɴ'ᴛ ꜱᴋɪᴘ ꜰɪʀꜱᴛ 2 ꜱᴏɴɢꜱ - {i}")
                    await delete_messages([m, msg])
        except (ValueError, TypeError):
            await msg.edit("⚠️ ɪɴᴠᴀʟɪᴅ ꜰᴇᴇᴅ")
            await delete_messages([m, msg])
    pl=await get_playlist_str()
    if m.chat.type == "private":
        await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        if Config.msg.get('player'):
            await Config.msg['player'].delete()
        Config.msg['player'] = await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        await delete_messages([m])

@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def pause_playing(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if Config.PAUSE:
        k = await m.reply("🤞 ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜꜱᴇᴅ")
        await delete_messages([m, k])
        return
    k = await m.reply("📺 ᴠɪᴅᴇᴏᴄᴀʟʟ ᴘᴀᴜꜱᴇᴅ")
    await pause()
    await delete_messages([m, k])
    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def resume_playing(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.PAUSE:
        k = await m.reply("✌️ ɴᴏᴛʜɪɴɢ ᴘᴀᴜꜱᴇᴅ ᴛᴏ ʀᴇꜱᴜᴍᴇ")
        await delete_messages([m, k])
        return
    k = await m.reply("📺 ᴠɪᴅᴇᴏᴄᴀʟʟ ʀᴇꜱᴜᴍᴇ")
    await resume()
    await delete_messages([m, k])
    


@Client.on_message(filters.command(['volume', f"volume@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if len(m.command) < 2:
        await m.reply_text('🎛️ ꜱᴡɪᴛᴄʜ ᴠᴏʟᴜᴍᴇ ᴏꜰ ʏᴏᴜʀ ᴘʟᴀʏᴇʀ', reply_markup=await volume_buttons())
        await delete_messages([m])
        return
    if not 1 < int(m.command[1]) < 200:
        await m.reply_text(f"🪃 ꜱᴇᴛ ʙᴇᴛᴡᴇᴇɴ 1-200 ᴠᴏʟᴜᴍᴇ", reply_markup=await volume_buttons())
    else:
        await volume(int(m.command[1]))
        await m.reply_text(f"🎚️ ᴠᴏʟᴜᴍᴇ ꜱᴇᴛ ᴛᴏ {m.command[1]}", reply_markup=await volume_buttons())
    await delete_messages([m])

    


@Client.on_message(filters.command(['vcmute', f"vcmute@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_mute(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if Config.MUTED:
        k = await m.reply_text("🔇 ᴍᴜᴛᴇᴅ ᴀʟʀᴇᴀᴅʏ")
        await delete_messages([m, k])
        return
    k=await mute()
    if k:
        k = await m.reply_text(f"🔇 ᴍᴜᴛᴇ ᴅᴏɴᴇ")
        await delete_messages([m, k])
    else:
        k = await m.reply_text("🔇 ᴍᴜᴛᴇᴅ ᴀʟʀᴇᴀᴅʏ")
        await delete_messages([m, k])
    
@Client.on_message(filters.command(['vcunmute', f"vcunmute@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_unmute(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.MUTED:
        k = await m.reply("🔊 ᴜɴᴍᴜᴛᴇ ꜱᴛʀᴇᴀᴍ")
        await delete_messages([m, k])
        return
    k=await unmute()
    if k:
        k = await m.reply_text(f"🔊 ᴜɴᴍᴜᴛᴇᴅ ᴅᴏɴᴇ")
        await delete_messages([m, k])
        return
    else:
        k=await m.reply_text("🔊 ᴜɴᴍᴜᴛᴇᴅ ᴀʟʀᴇᴀᴅʏ")    
        await delete_messages([m, k])


@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def replay_playout(client, m: Message):
    msg = await m.reply('💿 ᴄʜᴇᴄᴋɪɴɢ ᴘʟᴀʏᴇʀ')
    if not Config.CALL_STATUS:
        await msg.edit(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    await msg.edit(f"▶️ ᴘʟᴀʏ ꜰʀᴏᴍ ᴛʜᴇ ꜱᴛᴀʀᴛ")
    await restart_playout()
    await delete_messages([m, msg])


@Client.on_message(filters.command(["player", f"player@{Config.BOT_USERNAME}"]) & chat_filter)
async def show_player(client, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        title="<b>🎏 ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍ ɪꜱ ᴏɴ !!</b>"
    else:
        if Config.playlist:
            title=f"<b>{Config.playlist[0][1]}</b>\n"
        elif Config.STREAM_LINK:
            title=f"<b>🎏 ꜱᴛʀᴇᴀᴍ ᴜʀʟ [ᴄʟɪᴄᴋ ʜᴇʀᴇ!!]({data['file']})</b>"
        else:
            title=f"<b>🎏 ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴜᴘ [ᴄʟɪᴄᴋ ʜᴇʀᴇ!!]({Config.STREAM_URL})</b>"
    if m.chat.type == "private":
        await m.reply_text(
            title,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('player') is not None:
            await Config.msg['player'].delete()
        Config.msg['player'] = await m.reply_text(
            title,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])


@Client.on_message(filters.command(["seek", f"seek@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def seek_playout(client, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "🪄 ᴛᴀᴘᴇ ɪꜱ ʟɪᴠᴇ!! ᴘʟᴀʏ ᴡɪᴛʜ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    data=Config.DATA.get('FILE_DATA')
    k=await m.reply("🪀 ᴛʀʏɪɴɢ ᴛᴏ ꜱᴇᴇᴋ...")
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        await k.edit("🪀 ʜᴇʏ!! ᴛʜɪꜱ ꜱᴛʀᴇᴀᴍ ᴄᴀɴ'ᴛ ʙᴇ ꜱᴇᴇᴋ...")
        await delete_messages([m, k])
        return
    if ' ' in m.text:
        i, time = m.text.split(" ")
        try:
            time=int(time)
        except:
            await k.edit('📵 ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ꜱᴛᴀᴛᴇᴅ')
            await delete_messages([m, k])
            return
        nyav, string=await seek_file(time)
        if nyav == False:
            await k.edit(string)
            await delete_messages([m, k])
            return
        if not data.get('dur', 0)\
            or data.get('dur') == 0:
            title="<b>🎏 ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍ ɪꜱ ᴏɴ !!</b>"
        else:
            if Config.playlist:
                title=f"<b>{Config.playlist[0][1]}</b>\n"
            elif Config.STREAM_LINK:
                title=f"<b>🎏 ꜱᴛʀᴇᴀᴍ ᴜʀʟ [ᴄʟɪᴄᴋ ʜᴇʀᴇ!!]({data['file']})</b>"
            else:
                title=f"<b>🎏 ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴜᴘ [ᴄʟɪᴄᴋ ʜᴇʀᴇ!!]({Config.STREAM_URL})</b>"
        if Config.msg.get('player'):
            await Config.msg['player'].delete()  
        Config.msg['player'] = await k.edit(f"🎧 {title}", reply_markup=await get_buttons(), disable_web_page_preview=True)
        await delete_messages([m])
    else:
        await k.edit('📵 ɴᴏ ᴛɪᴍᴇ ꜱᴛᴀᴛᴇᴅ')
        await delete_messages([m, k])


@Client.on_message(filters.command(["settings", f"settings@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def settings(client, m: Message):
    await m.reply(f"📼 ᴄᴏɴꜰɪɢᴜʀᴇ - ᴘʟᴀʏᴇʀ ꜱᴇᴛᴛɪɴɢꜱ", reply_markup=await settings_panel(), disable_web_page_preview=True)
    await delete_messages([m])
