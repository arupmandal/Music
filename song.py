import os
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

# logging
bot = Client(
   "Music-Bot",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)
## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@bot.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("ð ðð²ð¹ð¹ð¼ ðð¿ð¼\n\nð ðð¦ ðð®ð¬ð¢ð ðð¨ð°ð§ð¥ð¨ðððð«[ð¶](https://telegra.ph/file/92a1f08c6ca91e0e8c163.mp4)\n\nðºððð ððð ðµððð ðð ððð ðð¨ð§ð  ððð ð¾ððð... ðð¥°ð¤\n\nðððð ð§ðð½ð² ð® ð¦ð¼ð»ð´ ð¡ð®ðºð²\n\nðð . `Believer`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ðð²ðð²ð¹ð¼ð½ð²ð¿', url='https://t.me/tech_arup'),
                    InlineKeyboardButton('ð¦ð¼ðð¿ð°ð²', url='https://github.com/arupmandal/Music')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b>Simplest Wayð</b>\n\n<i>How many times have I said that just giving the name of a song is enough.ð\nDo not expect any other help from með </i>\n\n<b>Eg</b> `Vaathi Coming`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ð¦ð¼ðð¿ð°ð²', url='https://github.com/arupmandal/Music')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("âª<b>Name</b> : â«<i>Music Downloader</i>\nâª<b>Developer</b> : â«[ðð¦ðµð¦ð³ ðð¢ð³ð¬ð¦ð³](https://t.me/tech_arup)\nâª<b>Language</b> : â«<i>Python3</i>\nâª<b>Server</b> : â«[ðð¦ð³ð°ð¬ð¶](https://heroku.com/)\nâª<b>Source Code</b> : â«[ðð­ðªð¤ð¬ ðð¦ð³ð¦](https://github.com/arupmandal/Music)",
    )

@bot.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('ð ð¦ð²ð®ð¿ð°ðµð¶ð»ð´ ððµð² ð¦ð¼ð»ð´...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"MusicDownloadv2bot" 
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('ðð¨ð®ð§ð ðð¨ð­ð¡ð¢ð§ð . ðð«ð² ðð¡ðð§ð ð¢ð§ð  ðð¡ð ðð©ðð¥ð¥ð¢ð§ð  ð ðð¢ð­ð­ð¥ð ð')
            return
    except Exception as e:
        m.edit(
            "â ð¹ðð¢ðð ððð¡âððð. ðð¨ð«ð«ð².\n\nð¯ðð¾ðºðð¾ ð³ðð ð ððºðð ð®ð ð²ð¾ðºðð¼ð ðºð Google.com ð¥ðð ð¢ðððð¾ð¼ð ð²ðð¾ððððð ðð¿ ððð¾ ðð¤ð£ð.\n\nEg.`Believer`"
        )
        print(str(e))
        return
    m.edit("`Uploading Your Song,Please Wait...`[ð§](https://telegra.ph/file/33e209cb838912e8714c9.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'ð§ ð§ð¶ððð¹ð² : [{title[:35]}]({link})\nâ³ ððð¿ð®ðð¶ð¼ð» : `{duration}`\nð ð©ð¶ð²ðð : `{views}`\n\nð® ðð: {message.from_user.mention()}\nð¤ ðð : @MusicDownloadv2bot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('ðððð¡ðð\n\n`Plesase Try Again Later`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
