import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send("🎧 Bin im Sprachkanal!")

    else:
        await ctx.send("Du musst zuerst in einem Sprachkanal sein!")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Verlassen!")

    else:
        await ctx.send("Ich bin in keinem Sprachkanal.")


@bot.command()
async def radio(ctx):
    if not ctx.voice_client:

        if ctx.author.voice:
            await ctx.author.voice.channel.connect()

        else:
            await ctx.send("Du musst zuerst in einem Sprachkanal sein!")
            return


    radio_url = "https://streams.ilovemusic.de/iloveradio1.mp3"


    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()


    audio = discord.FFmpegPCMAudio(
    radio_url,
    executable="C:/Users/Samu/Downloads/ffmpeg-8.1.2-essentials_build/ffmpeg-8.1.2-essentials_build/bin/ffmpeg.exe"
)
    ctx.voice_client.play(audio)

    await ctx.send("📻 Radio läuft!")


@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Musik gestoppt!")


bot.run(TOKEN)