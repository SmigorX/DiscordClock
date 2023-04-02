import discord
import time
import asyncio
from Secrets import discord_token
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(intents=intents, command_prefix="!")


async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def setup(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel ID.")
    else:
        await ctx.send(f"Target channel set to {channel.mention}.")
        while True:
            try:
                now = time.strftime("%H:%M EVE time", time.gmtime())
                await channel.edit(name=now)
                await asyncio.sleep(600)
            except Exception as e:
                ctx.send(f"An error occurred: {e} \n")
                break


TOKEN = discord_token
bot.run(TOKEN)
