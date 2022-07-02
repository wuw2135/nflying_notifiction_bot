import discord
from discord.ext import commands
from core.classes import Cog_Extension

class ReloadCogs(Cog_Extension):
    @commands.command()
    @commands.is_owner() # 管理者才能使用
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cmds.{extension}')
        await ctx.send(f"Loaded {extension} done.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f"Un-Loaded {extension} done.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        # 如果直接更改程式碼的話就直接reload
        self.bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f"Re-Loaded {extension} done.")


def setup(bot):
    bot.add_cog(ReloadCogs(bot))