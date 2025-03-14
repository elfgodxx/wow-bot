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

bot.run(TOKEN)
