import discord
from discord.ext import commands, tasks
import json
from discord.utils import get


class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
