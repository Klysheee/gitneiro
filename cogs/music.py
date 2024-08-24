import discord
import yt_dlp as youtube_dl

async def play(ctx, search_query: str):
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice_client is None or not voice_client.is_connected():
        voice_client = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            url = info_dict['entries'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print(f"Error occurred: {e}") if e else None)
            await ctx.send(f"Now playing: {info_dict['entries'][0]['title']}")
    except Exception as e:
        await ctx.send(f"An error occurred while playing: {str(e)}")

async def stop(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Music stopped.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")
