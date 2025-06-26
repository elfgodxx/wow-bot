import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.ext import commands

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

# commands added
@bot.command()
async def wiki(ctx, *, query: str):
    """Provides a direct Wowhead search link for the given query."""
    base_url = "https://www.wowhead.com/search?q="
    search_query = query.replace(" ", "+")  # Replace spaces with '+'
    search_url = f"{base_url}{search_query}"
    await ctx.send(f"Search results for '{query}': {search_url}")

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

# command for help
# always add a help for your command
# here each time you add new one
@bot.command()
async def wowhelp(ctx):
	help_message = (
		"**Available Commands:**\n"
		"`/wowhelp` - Shows this help message.\n"
        "`/check [filename]` - Upload an image with this command to check it. Default filename is 'Unknown File'.\n"
        "`/wiki` - searches the wowhead site with keyword you added.\n"
        "`/ping` - Responds with 'pong'.\n"
        "`/pong` - Responds with 'ping'."
        )
	await ctx.send(help_message)

@bot.command()
async def wowjia(ctx):
	await ctx.send("**I love my bunsy forever!**\n")

# bot runner
bot.run(TOKEN)
