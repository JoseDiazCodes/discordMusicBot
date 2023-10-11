# Discord Music Bot

A simple Discord bot to join a voice channel and play music from YouTube using `yt_dlp`.

## Features

- Joins the user's voice channel with the `!join` command.
- Plays music from YouTube with the `!playMusic <song name>` command.
- Skips the current playing song with the `!skip` command.
- Provides error feedback in the chat.
- Custom messages for when a song starts.

## Requirements

- Python 3.8 or newer.
- Packages:
  - `discord.py`
  - `yt_dlp`
  - `ffmpeg`

## Installation

1. Clone the repository: git clone <repository-url>
2. Navigate to the directory: cd <directory-name>
3. Install the necessary packages: pip install discord.py yt_dlp

4. Make sure `ffmpeg` is installed and in the system's PATH.

## Setup

1. Replace `TOKEN` in the script with your bot's token.
2. Adjust the path to `libopus.dylib` if needed (based on your system and installation).
3. Adjust the path to `ffmpeg` if different.

## Usage

1. Run the bot: python <filename>.py
2.
3. Invite the bot to your server.
4. Use the commands to control the bot in your Discord server.

## Commands

- `!join`: Makes the bot join your current voice channel.
- `!playMusic <song name>`: Searches for the song on YouTube and plays it in the voice channel.
- `!skip`: Skips the current playing song.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Code

```python
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Intents
import yt_dlp as youtube_dl
import random

if not discord.opus.is_loaded():
 discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.4/lib/libopus.dylib')

TOKEN = 'YOUR_TOKEN_HERE'

intents = Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

YDL_OPTIONS = {
 'format': 'bestaudio/best',
 'postprocessors': [{
     'key': 'FFmpegExtractAudio',
     'preferredcodec': 'opus',
     'preferredquality': '192',
 }],
 'noplaylist': 'True'
}

FFMPEG_OPTIONS = {
 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
 'options': '-vn'
}

PHRASES = [
 "Playing that super hot fire rn, hold up ({})",
 "Bro relax... you finna light my house on fire with {}",
 "Metro-booming wants some more! Go crazy kid! Now playing: {}"
]

def search_yt(song_name):
 with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
     try:
         info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
     except Exception:
         return False
 return {'title': info['title'], 'url': info['url']}

@bot.event
async def on_ready():
 print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
 await ctx.send(f'Error: {error}')

@bot.command(pass_context=True)
async def join(ctx):
 channel = ctx.message.author.voice.channel
 await channel.connect()

@bot.command(pass_context=True)
async def playMusic(ctx, *, song_name):
 if not ctx.voice_client.is_connected():
     await ctx.message.author.voice.channel.connect()

 song_info = search_yt(song_name)
 if not song_info:
     await ctx.send("Couldn't find the song.")
     return

 message = random.choice(PHRASES).format(song_info['title'])
 await ctx.send(message)
 ctx.voice_client.play(FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=song_info['url'], **FFMPEG_OPTIONS))

@bot.command(pass_context=True)
async def skip(ctx):
 if ctx.voice_client and ctx.voice_client.is_playing():
     ctx.voice_client.stop()
     await ctx.send("Skipped the current song!")
 else:
     await ctx.send("No song is playing right now!")

bot.run(TOKEN)


```
