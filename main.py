import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Intents
import yt_dlp as youtube_dl
import random

if not discord.opus.is_loaded():
    discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.4/lib/libopus.dylib')  # Use one of the paths you found

TOKEN = "enter your discord token key"

intents = Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Modify the YDL options for best audio quality.
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
    'noplaylist': 'True'
}

# Additional FFmpeg options for better quality and error handling.
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

    # Send the message to the text channel, including the song title.
    message = random.choice(PHRASES).format(song_info['title'])
    await ctx.send(message)

    # Specify FFmpeg executable path and use the improved FFmpeg options.
    ctx.voice_client.play(FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=song_info['url'], **FFMPEG_OPTIONS))

@bot.command(pass_context=True)
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped the current song!")
    else:
            await ctx.send("No song is playing right now!")

bot.run(TOKEN)
