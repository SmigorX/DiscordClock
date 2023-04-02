import discord
import time
import asyncio
from Secrets import discord_token
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def setchannel(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel ID.")
    else:
        await ctx.send(f"Target channel set to {channel.mention}.")
        while True:
            now = time.strftime("%H:%M EVE time", time.gmtime())
            await channel.edit(name=now)
            print(now)
            print(channel)
            await asyncio.sleep(600)


TOKEN = discord_token
bot.run(TOKEN)
