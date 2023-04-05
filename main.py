import discord
import time
import asyncio

from Secrets import discord_token
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")


@bot.hybrid_command(name="clock", description="Select the clock channel.")
async def clock(ctx, channel: discord.VoiceChannel):
    channel_id = channel.id
    if ctx.channel.permissions_for(ctx.author).manage_channels is False:
        await ctx.send("You do not have needed permissions to use this command.")
        return
    if channel_id is None:
        await ctx.send("Please specify a channel ID.")
        return
    try:
        channel = bot.get_channel(int(channel_id))
        if channel is None:
            await ctx.send("Invalid channel ID.")
            return
        else:
            await ctx.send(f"Target channel set to {channel.mention}.")
            while True:
                now = time.strftime("%H:%M EVE time", time.gmtime())
                await channel.edit(name=now)
                await asyncio.sleep(600)
    except Exception as e:
        await ctx.send(f"Error: {e}")
        return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()


TOKEN = discord_token
bot.run(TOKEN)
