import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension

import json

tw_ind = 0
yt_ind = 0
ytl_ind = 0
vli_ind = 0
ins_ind = 0

class Loop(Cog_Extension):
    # ---------------------------Twitter Update---------------------------------
    @tasks.loop(seconds = 3)
    async def tw_update(self,ctx):
        with open(self.bot.tw_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        global tw_ind

        if len(accdata):
            tw_ind %= len(accdata)
            await self.bot.get_command('tw_update_cod').callback(self,ctx,accdata,ins_ind)
            tw_ind += 1
            


    # ---------------------------Youtube Update---------------------------------   
    @tasks.loop(seconds=11)
    async def yt_update(self,ctx):
        with open(self.bot.yt_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        global yt_ind
        
        if len(accdata):
            yt_ind %= len(accdata)
            await self.bot.get_command('ytl_update_cod').callback(self,ctx,accdata,yt_ind)
            yt_ind += 1
            


    # ---------------------------Youtube Live Update---------------------------------            
    @tasks.loop(minutes=15)
    async def yt_live_update(self,ctx):
        with open(self.bot.ytl_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        global ytl_ind
        
        if len(accdata):
            ytl_ind %= len(accdata)
            await self.bot.get_command('ytl_update_cod').callback(self,ctx,accdata,ytl_ind)
            ytl_ind += 1


    # ---------------------------Vlive Update--------------------------------- 
    @tasks.loop(minutes=5)
    async def vli_update(self,ctx):
        with open(self.bot.vli_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        global vli_ind

        if len(accdata):
            vli_ind %= len(accdata)
            await self.bot.get_command('vli_update_cod').callback(self,ctx,accdata,vli_ind)
            vli_ind += 1


    # ---------------------------Instagram Update---------------------------------
    @tasks.loop(minutes=5)
    async def ins_update(self,ctx):
        with open(self.bot.ins_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        global ins_ind

        if len(accdata):
            ins_ind %= len(accdata)
            await self.bot.get_command('ins_update_cod').callback(self,ctx,accdata,ins_ind)
            ins_ind += 1

    # ---------------------------To Start---------------------------------
    @commands.command()
    async def tw_update_start(self,ctx):
        self.tw_update.start(ctx)

    @commands.command()
    async def yt_update_start(self,ctx):
        self.yt_update.start(ctx)

    @commands.command()
    async def ytl_update_start(self,ctx):
        self.yt_live_update.start(ctx)

    @commands.command()
    async def vli_update_start(self,ctx):
        self.vli_update.start(ctx)

    @commands.command()
    async def ins_update_start(self,ctx):
        self.ins_update.start(ctx)

    @commands.command()
    async def tw_update_stop(self,ctx):
        self.tw_update.cancel()

    @commands.command()
    async def yt_update_stop(self,ctx):
        self.yt_update.cancel()

    @commands.command()
    async def ytl_update_stop(self,ctx):
        self.yt_live_update.cancel()

    @commands.command()
    async def vli_update_stop(self,ctx):
        self.vli_update.cancel()

    @commands.command()
    async def ins_update_stop(self,ctx):
        self.ins_update.cancel()

def setup(bot):
    bot.add_cog(Loop(bot))