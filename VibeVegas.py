import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory database for storing user balances
user_balances = {}

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is now running!')

@bot.command(name='balance')
async def balance(ctx):
    user_id = ctx.author.id
    balance = user_balances.get(user_id, 0)
    await ctx.send(f'{ctx.author.name}, you have {balance} Vcoins.')

@bot.command(name='daily')
async def daily(ctx):
    user_id = ctx.author.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    user_balances[user_id] += 100  # Award 100 Vcoins daily
    await ctx.send(f'{ctx.author.name}, you received 100 Vcoins!')

@bot.command(name='bet')
async def bet(ctx, amount: int):
    user_id = ctx.author.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    
    if amount <= 0:
        await ctx.send(f'{ctx.author.name}, the bet amount must be greater than 0.')
        return

    if user_balances[user_id] < amount:
        await ctx.send(f'{ctx.author.name}, you do not have enough Vcoins to place this bet.')
        return

    # Simple win/lose mechanic
    if random.choice([True, False]):
        user_balances[user_id] += amount
        await ctx.send(f'{ctx.author.name}, you won {amount} Vcoins!')
    else:
        user_balances[user_id] -= amount
        await ctx.send(f'{ctx.author.name}, you lost {amount} Vcoins.')

@bot.command(name='give')
async def give(ctx, member: discord.Member, amount: int):
    giver_id = ctx.author.id
    recipient_id = member.id

    if giver_id not in user_balances:
        user_balances[giver_id] = 0

    if amount <= 0:
        await ctx.send(f'{ctx.author.name}, the gift amount must be greater than 0.')
        return

    if user_balances[giver_id] < amount:
        await ctx.send(f'{ctx.author.name}, you do not have enough Vcoins to give.')
        return

    if recipient_id not in user_balances:
        user_balances[recipient_id] = 0

    user_balances[giver_id] -= amount
    user_balances[recipient_id] += amount
    await ctx.send(f'{ctx.author.name} gave {amount} Vcoins to {member.name}.')

TOKEN = 'MTMzNTI1NDgzOTA5NzE2Nzg4Mg.GK6Psi.lfP0x5vxmnmsC9aK_w30NVrZW4IRkS4a6ho1EQ'
bot.run(TOKEN)
