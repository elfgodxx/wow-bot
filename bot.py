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

# Dictionary to store named to-do lists
todo_lists = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def newtodo(ctx, list_name: str):
    """Creates a new to-do list."""
    if list_name in todo_lists:
        await ctx.send(f"A to-do list named **{list_name}** already exists!")
    else:
        todo_lists[list_name] = []
        await ctx.send(f"✅ Created a new to-do list: **{list_name}**")

@bot.command()
async def todo(ctx, list_name: str, *, task: str):
    """Adds a task to a specific to-do list."""
    if list_name not in todo_lists:
        await ctx.send(f"❌ No to-do list named **{list_name}**. Use `/newtodo {list_name}` first.")
        return

    todo_lists[list_name].append({"task": task, "done": False})
    msg = await ctx.send(f"☐ **[{list_name}]** {task}")
    await msg.add_reaction("✅")  # Mark as done
    await msg.add_reaction("❌")  # Remove task

@bot.event
async def on_reaction_add(reaction, user):
    """Handles reactions to mark tasks as done or remove them."""
    if user.bot:
        return  # Ignore bot reactions

    msg = reaction.message
    content = msg.content

    # Find which to-do list the task belongs to
    for list_name, tasks in todo_lists.items():
        for task in tasks:
            if f"**[{list_name}]** {task['task']}" == content:
                if reaction.emoji == "✅":
                    task["done"] = True
                    await msg.edit(content=f"✅ ~~**[{list_name}]** {task['task']}~~")
                elif reaction.emoji == "❌":
                    tasks.remove(task)
                    await msg.delete()
                return

@bot.command()
async def showtodo(ctx, list_name: str):
    """Displays all tasks in a specific to-do list."""
    if list_name not in todo_lists:
        await ctx.send(f"❌ No to-do list named **{list_name}** found.")
        return

    tasks = todo_lists[list_name]
    if not tasks:
        await ctx.send(f"📂 **{list_name}** is empty!")
        return

    response = f"📝 **To-Do List: {list_name}**\n"
    for task in tasks:
        status = "✅" if task["done"] else "☑️"
        response += f"{status} {task['task']}\n"

    await ctx.send(response)

@bot.command()
async def deletetodo(ctx, list_name: str):
    """Deletes an entire to-do list."""
    if list_name in todo_lists:
        del todo_lists[list_name]
        await ctx.send(f"🗑️ Deleted the to-do list: **{list_name}**")
    else:
        await ctx.send(f"❌ No to-do list named **{list_name}** found.")

bot.run(TOKEN)
