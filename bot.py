import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()  # Load environment variables from .env
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def search(ctx, *, query: str):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find('div', class_='BNeawe').text
    await ctx.send(f"Top result for '{query}':\n{result}")

@bot.command()
async def check(ctx, filename: str = "Unknown File"):
    # Check if an attachment exists
    if not ctx.message.attachments:
        await ctx.send("Please upload an image with the command.")
        return

    # Get the uploaded image
    attachment = ctx.message.attachments[0]
    
    # Send a message with the filename and uploader
    response = f"{filename} uploaded by {ctx.author.mention}"
    msg = await ctx.send(response)

    # React with ✅ and ❌
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def pong(ctx):
    await ctx.send("ping")

@bot.command()
async def wowhelp(ctx):
	help_message = (
		"**Available Commands:**\n"
		"`/wowhelp` - Shows this help message.\n"
        "`/check [filename]` - Upload an image with this command to check it. Default filename is 'Unknown File'.\n"
        "`/ping` - Responds with 'pong'.\n"
        "`/pong` - Responds with 'ping'."
        )
	await ctx.send(help_message)

bot.run(TOKEN)