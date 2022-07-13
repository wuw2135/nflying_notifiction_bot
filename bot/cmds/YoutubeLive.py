import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import datetime
import asyncio
import os
import requests
import dateutil.parser
from pathlib import Path

path = Path(os.path.dirname(__file__)).parent.absolute()
sec_path = str(path) + "/secretdata.json"
with open(sec_path, "r", encoding="utf-8") as file:
    secdata = json.load(file)


class YoutubeLive(Cog_Extension):
    # ---------------------------follow add---------------------------------
    @commands.command()
    async def ytlivadd_id(self,ctx,*args):
        account = list(args)
        passfir = []
        errors = []
        tests = ""
        for i in range(len(account)):
            if "https://www.youtube.com/c/" in account[i] or "https://www.youtube.com/channel/" not in account[i]:
                errors.append(account[i])
                continue
            else:
                account[i] = account[i].split('/')[4]
                passfir.append(account[i])
                tests += "&id="+account[i]

        with open(self.bot.ytl_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        
        if len(tests):
            url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet{tests}&key={secdata['Youtube']['ytl_apikey']}"
            response = requests.request("GET", url)
            rlist = response.json()

        if rlist["pageInfo"]["totalResults"]:
            for test in rlist["items"]:
                flag = True
                for data in accdata:
                    if data["id"] == test["id"]:
                        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl",f"{test['snippet']['title']} already exist"))
                        passfir.remove(test["id"])
                        flag = False
                        break
                
                if flag:
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl",f"What channel you want {test['snippet']['title']} to post from? Use channel id!"))
                    
                    channel = 0
                    try:
                        msg = await self.bot.wait_for("message", check=lambda x: x.author.id == ctx.author.id, timeout=60.0)
                    except asyncio.TimeoutError:
                        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl","You are run out of time, so I will post it on this channel."))
                        channel = ctx.channel.id
                    else:
                        flag = False;
                        for ch in ctx.guild.channels:
                            if int(msg.content) == ch.id:
                                flag = True;
                                channel = ch.id
                                await msg.add_reaction('👍')
                                break

                        if flag == False:
                            channel = ctx.channel.id
                            await msg.add_reaction('👎')
                            await msg.reply(embed = self.bot.simple_format("ytl","I can't find it, so I will post it on this channel."))
                    
                    accdata.append({"id": test["id"], "username" : test["snippet"]["title"], "url" : f"https://www.youtube.com/channel/{test['id']}", "profileurl": test["snippet"]["thumbnails"]["high"]["url"], "lastpost": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]+"Z", "channel": channel})
                    passfir.remove(test["id"])
        
        if len(errors) or len(passfir):
            [errors.append(v) for v in passfir]
            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl",f"{', '.join(str(v) for v in errors)} use URL that have channelID! ex.https://www.youtube.com/channel/[channelID]"))

        with open(self.bot.ytl_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))

        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl","added!"))
        
    @commands.command()
    async def ytlivadd_vid(self, ctx, *args):
        links = list(args)
        
        tmplinks = []
        passfir = []
        errors = []
        tests = ""
        for i in range(len(links)):
            if "https://www.youtube.com/watch?v=" not in links[i]:
                errors.append(links[i])
                continue
            else:
                links[i] = links[i].split('v=')[1].split('&')[0] if  links[i].find('&') >= 0 else links[i].split('v=')[1]
                tests += "&id="+links[i]
                passfir.append(links[i])

        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet{tests}&key={secdata['Youtube']['ytl_apikey']}"
        response = requests.request("GET", url)
        rlist = response.json()

        if rlist["pageInfo"]["totalResults"]:
            for test in rlist["items"]:
                tmplinks.append(f"https://www.youtube.com/channel/{test['snippet']['channelId']}")
                passfir.remove(test["id"])

        if len(errors) or len(passfir):
            [errors.append(v) for v in passfir]
            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ytl",f"{', '.join(str(v) for v in errors)} can't found!"))

        if len(tmplinks):
            await self.bot.get_command('ytlivadd_id').callback(self,ctx, *tmplinks)


    @commands.command(hidden = True)
    async def ytl_update_cod(self,ctx,accdata,ytl_ind):
        channel = self.bot.get_channel(accdata[ytl_ind]["channel"])
        url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId="+accdata[ytl_ind]["id"]+"&eventType=live&maxResults=25&publishedAfter="+accdata[ytl_ind]["lastpost"]+"&type=video&key="+secdata['Youtube']['ytl_apikey']
        response = requests.request("GET", url)
        rlist = response.json()

        if "pageInfo" in rlist:
            for j in range(len(rlist["items"]),0,-1):
                if rlist["items"][j-1]["snippet"]["channelTitle"] != accdata[ytl_ind]["username"] or accdata[ytl_ind]["lastpost"] == dateutil.parser.isoparse(rlist["items"][j-1]["snippet"]["publishedAt"]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]+"Z":
                    continue
        
                embeds = discord.Embed(title=f"{rlist['items'][j-1]['snippet']['title']}", url="https://www.youtube.com/watch?v="+rlist["items"][j-1]["id"]["videoId"], color=0xff0000)
                embeds.set_author(name = accdata[ytl_ind]["username"], url = accdata[ytl_ind]["url"], icon_url=accdata[ytl_ind]["profileurl"])
                embeds.description = accdata[ytl_ind]["username"]+" is live streaming!"
                imgurl = str()
                ind = 4
                imgsize = ['default','medium','high','standard','maxres']
                while ind>=0:
                    if imgsize[ind] in rlist["items"][j-1]["snippet"]["thumbnails"]:
                        imgurl = rlist["items"][j-1]["snippet"]["thumbnails"][imgsize[ind]]["url"]
                        break
                    else:
                        ind -= 1
                embeds.set_image(url = imgurl)
                embeds.timestamp = dateutil.parser.isoparse(rlist["items"][j-1]["snippet"]["publishedAt"])
                await channel.send(embed=embeds)

                if j-1 == 0:
                    accdata[ytl_ind]["lastpost"] = dateutil.parser.isoparse(rlist["items"][0]["snippet"]["publishedAt"]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]+"Z"

            with open(self.bot.ytl_csv_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(accdata, ensure_ascii=False, indent=1))



def setup(bot):
    bot.add_cog(YoutubeLive(bot))