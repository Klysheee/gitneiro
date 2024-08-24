import discord
import random
from discord.ext import commands
from asyncio import TimeoutError

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='крестики-нолики')
    async def start_tic_tac_toe(self, ctx):
        board = [" " for _ in range(9)]
        players = [ctx.author, None]
        current_player = 0
        game_active = True

        def display_board():
            return "\n".join([
                f"{board[0]} | {board[1]} | {board[2]}",
                "---------",
                f"{board[3]} | {board[4]} | {board[5]}",
                "---------",
                f"{board[6]} | {board[7]} | {board[8]}"
            ])

        def check_winner():
            win_conditions = [
                (0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)
            ]
            for x, y, z in win_conditions:
                if board[x] == board[y] == board[z] and board[x] != " ":
                    return board[x]
            return None

        def check_draw():
            return " " not in board

        await ctx.send(f"Игра началась!\n{display_board()}")
        while game_active:
            def check(msg):
                return msg.author == players[current_player] and msg.channel == ctx.channel and msg.content.isdigit()

            try:
                move_msg = await self.bot.wait_for('message', check=check, timeout=60)
                move = int(move_msg.content) - 1
                if board[move] != " ":
                    await ctx.send("Эта клетка уже занята. Попробуйте другую.")
                    continue

                board[move] = "X" if current_player == 0 else "O"
                await ctx.send(display_board())

                winner = check_winner()
                if winner:
                    await ctx.send(f"Победитель: {players[current_player].mention}")
                    game_active = False
                elif check_draw():
                    await ctx.send("Ничья!")
                    game_active = False
                else:
                    current_player = 1 - current_player
                    await ctx.send(f"Ход игрока {players[current_player].mention}")

            except TimeoutError:
                await ctx.send("Время ожидания истекло. Игра окончена.")
                game_active = False

    @commands.command(name='угадай число')
    async def start_guess_number(self, ctx):
        number = random.randint(1, 100)
        attempts = 0

        await ctx.send("Я загадал число от 1 до 100. Попробуйте его угадать!")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

        while True:
            try:
                guess_msg = await self.bot.wait_for('message', check=check, timeout=60)
                guess = int(guess_msg.content)
                attempts += 1

                if guess < number:
                    await ctx.send("Слишком маленькое число. Попробуйте снова.")
                elif guess > number:
                    await ctx.send("Слишком большое число. Попробуйте снова.")
                else:
                    await ctx.send(f"Поздравляю! Вы угадали число {number} за {attempts} попыток.")
                    break

            except TimeoutError:
                await ctx.send("Время ожидания истекло. Игра окончена.")
                break

async def setup(bot):
    await bot.add_cog(Games(bot))
