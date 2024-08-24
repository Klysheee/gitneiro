import os
from discord.ext import commands
from discord import Intents

# Configuration
openweather_api_key = 'your_openweather_api_key_here'
bot_token = 'your_discord_bot_token_here'

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
async def setup_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            cog = filename[:-3]
            await bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await setup_cogs()

@bot.command(name='Погода')
async def get_weather(ctx, *, city: str):
    from utils.weather import fetch_weather
    await fetch_weather(ctx, city, openweather_api_key)

@bot.command(name='Участники')
async def count_members(ctx):
    await ctx.send(f'На сервере "{ctx.guild.name}" {ctx.guild.member_count} участников.')

@bot.command(name='Активность')
async def suggest_activity(ctx):
    from utils.activities import suggest_activity
    await suggest_activity(ctx)

@bot.command(name='Музыка')
async def play_music(ctx, *, search_query: str):
    from cogs.music import play
    await play(ctx, search_query)

@bot.command(name='Остановить')
async def stop_music(ctx):
    from cogs.music import stop
    await stop(ctx)

@bot.command(name='Игра')
async def play_game(ctx, *, game: str):
    from cogs.games import start_tic_tac_toe, start_guess_number
    if game.lower() == 'крестики-нолики':
        await start_tic_tac_toe(ctx)
    elif game.lower() == 'угадай число':
        await start_guess_number(ctx)
    else:
        await ctx.send("Выберите игру: Крестики-нолики, Угадай число.")

@bot.command(name='Игры')
async def list_games(ctx):
    from utils.games_list import list_games
    await list_games(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена. Попробуйте другую команду.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Недостаточно аргументов для выполнения команды.")
    else:
        await ctx.send(f"Произошла ошибка: {str(error)}")

if __name__ == "__main__":
    if bot_token:
        bot.run('MTI3NTM3Nzg1MjA2NTI1MTQwMw.GABedr.14RYDijMy15r8f4b24JE4u6tkpYKt9XNzQ44Nk')
    else:
        print("Ошибка: Токен бота не установлен. Пожалуйста, проверьте переменные окружения.")
