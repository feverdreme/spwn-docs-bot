import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Embed
from src.Searcher import Searcher
from src.Collector import Collector
from src.Entry import Entry

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
# bot.remove_command('help')
collector = Collector()
searcher = Searcher(collector.builtins)


@bot.event
async def on_ready():
    print("Logged in")


# @bot.command()
# async def help(ctx):
#     await ctx.send("""
# ```
# Basic

# Can search for a function or type in the spwn_docs repository
# To use, simply type in 
# $sdoc SEARCH_TERM

# **Commands**

# - desc
# $sdoc desc SEARCH_TERM
# Gives retrieved description and uses for term (needs to be exact)
# ```
#     """)


@bot.command()
async def sdoc(ctx, search_term: str):
    embed_params: dict[str, str] = {
        "title": f"Search results for `{search_term}`",
        "description": "",
        "type": "rich"
    }
    entrylist_template = "[`{title}`]({url})"

    results: list[Entry] = searcher.search_for(search_term, max_distance=1)
    for entry in results:
        title, desc = entry.display()

        embed_params["description"] += entrylist_template.format(
            title=title, url=entry.url)

        if entry.ldistance == 0:
            embed_params["description"] += " - exact match"

        embed_params["description"] += '\n'

    await ctx.send(embed=Embed(**embed_params))

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN if DISCORD_TOKEN is not None else os.environ.get('DISCORD_TOKEN'))
