async def list_games(ctx):
    games = [
        "Крестики-нолики",
        "Угадай число",
        "Другие интересные игры..."
    ]
    await ctx.send("Доступные игры:\n" + "\n".join(games))
