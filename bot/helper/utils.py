import os
from bot import data, download_dir, app
import time
import asyncio
from bot.helper.devtools import progress_for_pyrogram, humanbytes , TimeFormatter
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from .function import upload_handle
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height 

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])

async def add_task(message: Message):
    try: 
      d_start = time.time() 
      msg = await message.reply_text(" 🎧**Downloading Video** 🎧", quote=True)
      filepath = await app.download_media(
        message=message,  
        file_name=download_dir,
        progress=progress_for_pyrogram,
        progress_args=(
          app,
          "**🎲  Trying To Downloading 🎲 **",
          msg,
          d_start
        )
      )
      chatid = message.chat.id
      reply_id = message.id
      og = await encode(filepath, msg)
      if og:
        await msg.edit("** 🚀Starting To Upload**")
        thumb = await get_thumbnail(og)
        width, height = await get_width_height(filepath)
        duration2 = await get_duration(og)
        await msg.edit("**🚀 Uploading Video 🚀**")
        u_start = time.time()
        await upload_handle(app, message, og, thumb, reply_id, msg, u_start, width, height, duration2)
        await msg.delete()
        os.remove(thumb)
        os.remove(og)
      else:
        await msg.edit("**Error Contact @Yuvi1poke_lover**")
        os.remove(og)
    except MessageNotModified:
      pass
    except Exception as e:
      await msg.edit(f"```{e}```")
    await on_task_complete()
    os.remove(filepath)
