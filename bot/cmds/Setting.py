import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio

def get_path(self,key):
    if key == "twi":
        path = self.bot.tw_csv_path
    elif key == "yt":
        path = self.bot.yt_csv_path
    elif key == "ytl":
        path = self.bot.ytl_csv_path
    elif key == "vli":
        path = self.bot.vli_csv_path
    elif key == "ins":
        path = self.bot.ins_csv_path

    return path

class Setting(Cog_Extension):
    
    # ---------------------------follow delete---------------------------------
    @commands.command()
    async def datadel(self,ctx,*args):
        path = get_path(self,args[0])

        with open(path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        
        for i in range(1,len(args)):
            flag = True
            for j in range(len(accdata)):
                if args[i] == accdata[j]["id"]:
                    flag = False
                    accdata.pop(j)
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format(args[0],f"{args[i]} deleted!"))
                    break

            if flag:
                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format(f"{args[i]} can't found!"))

        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))
    
     # ---------------------------follow search---------------------------------
    @commands.command()
    async def datafol(self,ctx,key):
        path = get_path(self,key)

        with open(path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        
        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.search_embed(key,accdata))

     # ---------------------------channel send setting---------------------------------
    @commands.command()
    async def dataset(self, ctx, *args):
        path = get_path(self,args[0])

        with open(path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        
        for i in range(1,len(args)):
            flag = False
            for data in accdata:
                if args[i] == data["id"]:
                    flag = True
                    await ctx.channel.send(ctx.message.author.mention ,embed = self.bot.simple_format(args[0],f"What channel you want {data['username']} to post from? Use channel id!"))

                    try:
                        msg = await self.bot.wait_for("message", check=lambda x: x.author.id == ctx.author.id, timeout=60.0)
                    except asyncio.TimeoutError:
                        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format(args[0],"You are run out of time, so I will post it on the original channel."))
                    else:
                        flag2 = False;
                        for ch in ctx.guild.channels:
                            if int(msg.content) == ch.id:
                                flag2 = True;
                                data["channel"] = int(msg.content)
                                await msg.add_reaction('👍')
                                break

                        if flag2 == False:
                            channel = ctx.channel.id
                            await msg.add_reaction('👎')
                            await msg.reply(embed = self.bot.simple_format(args[0],"I can't find it, so I will post it on the original channel."))

                    break
            
            if flag == False:
                await ctx.channel.send(ctx.message.author.mention ,embed = self.bot.simple_format(args[0],f"I can't find {args[i]} !"))

        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))



def setup(bot):
    bot.add_cog(Setting(bot))