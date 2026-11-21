import discord
from discord import app_commands
from discord.ext import commands
import requests
import random
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = "/", intents = intents)

dog_api = "https://dog.ceo/api/breeds/image/random"
cat_api = "https://api.thecatapi.com/v1/images/search"
facts_api = "https://uselessfacts.jsph.pl/api/v2/facts/random"
meme_api = f"https://api.imgur.com/3/gallery/t/meme/top/month/10"
meme_client_id = os.getenv("IMGUR_CLIENT_ID")
meme_headers = {"Authorization": f"Client-ID {meme_client_id}"}

def embed(title, description, footer = "", footer_url = "", image_url = "", thumbnail_url = "", colour_rgb = (0, 0, 0)):
    colour_rgb = discord.Color.from_rgb(colour_rgb[0], colour_rgb[1], colour_rgb[2])

    EmbedMessage = discord.Embed(title = title, description = description, color = colour_rgb)
    EmbedMessage.set_footer(text = footer, icon_url = footer_url)
    EmbedMessage.set_image(url = image_url)
    EmbedMessage.set_thumbnail(url = thumbnail_url)

    return EmbedMessage

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name = "fact", description = "Random fact.")
async def fact(interaction: discord.Interaction):
    fact_request = requests.get(facts_api)

    if fact_request.status_code == 200:
        fact_data = fact_request.json()
        fact = fact_data["text"]
        if fact:
            await interaction.response.send_message(fact)
        else:
            await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nNo facts found.\n```")
    elif fact_request.status_code == 404:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnknown HTTP 404, invalid/outdated API.\n```")
    else:
        await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nHTTP {fact_request.status_code}\n```")

@bot.tree.command(name = "dog", description = "Fetch a random dog picture.")
async def dog(interaction: discord.Interaction):
    dog_request = requests.get(dog_api)

    if dog_request.status_code == 200:
        dog_data = dog_request.json()
        if dog_data:
            dog_pic = dog_data["message"]
            await interaction.response.send_message(dog_pic)
        else:
            await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nNo dog pictures found.\n```")
    elif dog_request.status_code == 401:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnauthorized HTTP 401, check client id.\n```")
    elif dog_request.status_code == 404:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnknown HTTP 404, invalid/outdated API.\n```")
    else:
        await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nHTTP {dog_request.status_code}\n```")

@bot.tree.command(name = "cat", description = "Fetch a random cat picture.")
async def cat(interaction: discord.Interaction):
    cat_request = requests.get(cat_api)

    if cat_request.status_code == 200:
        cat_data = cat_request.json()
        if cat_data:
            cat_pic = cat_data[0]["url"]
            await interaction.response.send_message(cat_pic)
        else:
            await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nNo cat pictures found.\n```")
    elif cat_request.status_code == 401:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnauthorized HTTP 401, check client id.\n```")
    elif cat_request.status_code == 404:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnknown HTTP 404, invalid/outdated API.\n```")
    else:
        await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nHTTP {cat_request.status_code}\n```")

@bot.tree.command(name = "meme", description = "Fetch a random meme.")
async def meme(interaction: discord.Interaction):
    if not meme_client_id:
        await interaction.response.send_message("Set IMGUR_CLIENT_ID to enable memes.", ephemeral=True)
        return
    meme_request = requests.get(meme_api, headers = meme_headers)

    if meme_request.status_code == 200:
        meme_data = meme_request.json()
        memes = meme_data["data"]["items"]
        if memes != []:
            random_meme = random.choice(memes)
            meme = random_meme["images"][0]["link"]
            await interaction.response.send_message(meme)
        else:
            await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nNo memes found.\n```")
    elif meme_request.status_code == 401:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnauthorized HTTP 401, check client id.\n```")
    elif meme_request.status_code == 404:
        await interaction.response.send_message("❌ There was an error fetching a meme.\n```\nUnknown HTTP 404, invalid/outdated API.\n```")
    else:
        await interaction.response.send_message(f"❌ There was an error fetching a meme.\n```\nHTTP {meme_request.status_code}\n```")

@bot.tree.command(name = "server_info", description = "Get information about the server.")
@app_commands.guild_only()
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    name = guild.name
    owner = guild.owner
    avatar = guild.icon.url if guild.icon else None
    humans = 0
    bots = 0
    text_channels = 0
    voice_channels = 0
    roles = 0
    boost_level = guild.premium_tier
    boosts = guild.premium_subscription_count
    verification_level = guild.verification_level
    for i in range(len(guild.roles)): roles += 1
    for i in range(len(guild.text_channels)): text_channels += 1
    for i in range(len(guild.voice_channels)): voice_channels += 1
    for i in range(len(guild.members)):
        member = guild.members[i]
        if member.bot:
            bots += 1
        else:
            humans += 1
    embedInfo = embed(
        title = f"{name} Information ",
        description = f"🪧 **Official Name:** {name}\n👑 **Official Owner:** <@{guild.owner_id}>\n☑️ **Verification Level:** {verification_level}\n🚀 **Boost Level:** {boost_level}\n🚀 **Boost Count:** {boosts}\n🗂️ **Role Count:** {roles}\n🌆 **Total Channels:** {text_channels+voice_channels}\n💬 **Text Channels:** {text_channels}\n🎙️ **Voice Channels:** {voice_channels}\n👥 **Total Members:** {humans+bots}\n👤 **Human Members:** {humans}\n🤖 **Bot Members:** {bots}\n",
        footer = f"{datetime.now().strftime("%d/%m/%Y")} (DD/MM/YYYY)",
        thumbnail_url = avatar,
        colour_rgb = (74, 246, 97)
    )
    await interaction.response.send_message(embed = embedInfo)

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
