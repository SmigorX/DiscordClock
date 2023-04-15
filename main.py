import discord
import time
import asyncio
import sqlite3

from Secrets import discord_token_test as discord_token
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")

target_id = None

db_connection = sqlite3.connect("ClockBot_servers")
db_cursor = db_connection.cursor()


@bot.hybrid_command(name="add_clock", description="Select a channel for the clock")
async def add_clock(ctx, channel: discord.VoiceChannel):
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
            db_cursor.execute("SELECT channel_id FROM id_matching where channel_id = ?", (channel_id,))
            db_entry = db_cursor.fetchone()
            if db_entry is None:
                db_cursor.execute("INSERT INTO id_matching (server_id, channel_id) VALUES (?, ?)", (ctx.guild.id, channel_id))
                db_connection.commit()
                await ctx.send(f"Target channel set to {channel.mention}.")
                await on_ready()
                return
            else:
                await ctx.send("This channel already has a clock.")
                return

    except Exception as e:
        await ctx.send(f"Error: {e}")
        return


@bot.hybrid_command(name="remove_clock", description="Remove the clock from a channel")
async def remove_clock(ctx, channel: discord.VoiceChannel):
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
            db_cursor.execute("SELECT channel_id FROM id_matching where channel_id = ?", (channel_id,))
            db_entry = db_cursor.fetchone()
            if db_entry is not None:
                db_cursor.execute("DELETE FROM id_matching WHERE server_id = ? AND channel_id = ?", (ctx.guild.id, channel_id))
                db_connection.commit()
                await ctx.send(f"Clock removed from {channel.mention}.")
                await on_ready()
                return
            else:
                await ctx.send("This channel does not have a clock.")
                return

    except Exception as e:
        await ctx.send(f"Error: {e}")
        return


@bot.event
async def on_ready():
    await bot.tree.sync()
    while True:
        for guild in bot.guilds:
            db_cursor.execute("SELECT server_id, channel_id FROM id_matching where server_id = ?", (guild.id,))
            db_entry = db_cursor.fetchone()
            try:
                if db_entry is not None:
                    channel_id = db_entry[1]
                    await bot.get_channel(int(channel_id)).edit(name=time.strftime("%H:%M EVE time", time.gmtime()))
                else:
                    print("empty entry in db")
            except Exception as e:
                print(e)
                pass
            await asyncio.sleep(60)


TOKEN = discord_token
bot.run(TOKEN)
