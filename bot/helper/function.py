import pyrogram
import time
import asyncio
from html_telegraph_poster import TelegraphPoster
from bot.helper.devtools import progress_for_pyrogram
import time
import subprocess
from subprocess import Popen
from bot import app, sudo_users, ffmpeg, LOG_CHANNEL, download_dir

modes = []
modes.append('video')

async def change_ffmpeg(app, message):
  try:
    changeffmpeg = message.text.split(" ", maxsplit=1)[1]
    ffmpeg.insert(0,changeffmpeg)
    await message.reply_text(f"**Successfully Changed The FFMPEG-CODE To**\n```{changeffmpeg}```")
  except Exception as e:
    await message.reply_text(f"Error ```{e}```")

async def movie_mode(app, message):
  try:
    movie_mode = "-i 'https://te.legra.ph/file/e9408e71281cdcb017874.png' -map 0 -filter_complex 'overlay =main_w-(overlay_w+10):main_h-(overlay_h+10)'  -c:v libx265 -crf 27 -c:s copy -s 854x480 -preset medium -pix_fmt yuv420p10 -metadata title='Visit For More Movies [t.me/AniXpo]'  -metadata:s:v title='Visit Website[Anixpo] t.me/AniXpo] - 480p - HEVC - 8bit'  -metadata:s:a title='[Visit t.me/AniXpo] - Opus - 60 kbps' -metadata:s:s title='[AniXpo Substations Alpha]' -c:a libopus -ab 60k"
    ffmpeg.insert(0,movie_mode)
    await message.reply_text(f"**Successfully Enabled MOVIE 🎥 MODE 📳**")
  except Exception as e:
    await message.reply_text(f"Error ```{e}```")

async def anime_mode(app, message):
    try:
      anime_code = "-i 'https://te.legra.ph/file/e9408e71281cdcb017874.png' -map 0 -filter_complex 'overlay =main_w-(overlay_w+10):main_h-(overlay_h+10)'  -c:v libx265 -crf 30 -c:s copy -s 854x480 -preset slow -metadata title='Visit For More Movies [t.me/AniXpo]'  -metadata:s:v title='Visit Website[Anixpo] t.me/AniXpo] - 480p - HEVC - 8bit'  -metadata:s:a title='[Visit t.me/AniXpo] - Opus - 60 kbps' -metadata:s:s title='[AniXpo Substations Alpha]' -c:a libopus -ab 60k"
      ffmpeg.insert(0,anime_code)
      await message.reply_text("**Enabled Anime Mode**")
    except Exception as e:
      await message.reply_text(f"**Error** ```{e}```")
  
async def get_ffmpeg(app, message):
  await message.reply_text(f"**The Set Code Is**\n```{ffmpeg[0]}```")

def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def upload_mode(app, message):
 mode = message.text.split(" ", maxsplit=1)[1]
 if mode == "document":
   await message.reply_text("Change To Document Upload Mode")
   modes.insert(0, 'document')
 elif mode == "video":
   await message.reply_text("Set To Video Mode")
   modes.insert(0, 'video')
 else:
   await message.reply_text("Undefined Upload Mode Ise ```document``` Or ```video```")

async def info(file, app):
    process = subprocess.Popen(
        ["mediainfo", file, "--Output=HTML"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = process.communicate()
    out = stdout.decode()
    abc = await app.get_me()
    name = abc.first_name
    username = abc.username
    client = TelegraphPoster(use_api=True)
    client.create_api_token("Mediainfo")
    page = client.post(
        title="Mediainfo",
        author=name,
        author_url=f"https://t.me/{username}",
        text=out,
    )
    return page["url"]

async def upload_handle(app, message, og, thumb, reply_id, msg, u_start, width, height, duration2):
  if modes[0] == "video":
    u_start = time.time()
    await app.send_video(
      video=og,
      chat_id=message.chat.id, 
      supports_streaming=True,
      file_name=og, 
      thumb=thumb, 
      duration=duration2, 
      width=width, 
      height=height, 
      caption=og, 
      reply_to_message_id=reply_id,
      progress=progress_for_pyrogram,
      progress_args=(
        app,
        "**⬆️ Trying To Upload ⬆️**",
        msg,
        u_start
      )
  )
    await app.send_video(
      video=og,
      chat_id=LOG_CHANNEL, 
      supports_streaming=True,
      file_name=og, 
      thumb=thumb, 
      duration=duration2, 
      width=width, 
      height=height, 
      caption=og
    )  
  elif modes[0] == 'document':
   await app.send_document(
     document=og,
     chat_id=message.chat.id, 
     force_document=True,
     file_name=og, 
     thumb=thumb,  
     caption=og, 
     reply_to_message_id=reply_id,
     progress=progress_for_pyrogram,
     progress_args=(
       app,
       "**⬆️ Trying To Upload ⬆️**",
       msg,
       u_start
     )
  ) 
   await app.send_document(
     document=og,
     chat_id=LOG_CHANNEL, 
     force_document=True,
     file_name=og, 
     thumb=thumb,  
     caption=og
   )

async def mediainfo(app, message):
  if message.reply_to_message:
   video = message.reply_to_message.id
   msg = await app.send_message(chat_id=message.chat.id, reply_to_message_id=message.reply_to_message.id, text="**Downloading The File**", disable_web_page_preview=True)
   d_start = time.time()
   filepath = await app.download_media(
        message=message.reply_to_message,  
        file_name=download_dir,
        progress=progress_for_pyrogram,
        progress_args=(
          app,
          "**📥 Trying To Downloading 📥**",
          msg,
          d_start
        )
      )
   await msg.edit("**Getting Mediainfo**")
   mediainfo = await info(filepath, app)
   await msg.edit(f"[Mediainfo]({mediainfo})")
  else:
   await app.send_message(message.chat.id, "**😐 Reply To A File Bruhh**")
