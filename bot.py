import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

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
async def help(ctx):
	help_message = (
		"**Available Commands:**\n"
		"`!help` - Shows this help message.\n"
        "`!check [filename]` - Upload an image with this command to check it. Default filename is 'Unknown File'.\n"
        "`!ping` - Responds with 'pong'.\n"
        "`!pong` - Responds with 'ping'."
        )
	await ctx.send(help_message)

bot.run(TOKEN)