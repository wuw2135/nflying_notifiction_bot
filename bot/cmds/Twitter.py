import discord
from discord.ext import commands
import json
import datetime
from core.classes import Cog_Extension
import asyncio
import os
import requests
import dateutil.parser
from pathlib import Path

path = Path(os.path.dirname(__file__)).parent.absolute()
sec_path = str(path) + "/secretdata.json"
with open(sec_path, "r", encoding="utf-8") as file:
    secdata = json.load(file)

payload={}
headers = {
    'Authorization': f"Bearer {secdata['Twitter']['Bearer']}",
    'Cookie': f"guest_id={secdata['Twitter']['guest_id']}"
}

class Twitter(Cog_Extension):
    # ---------------------------follow add---------------------------------
    @commands.command()
    async def twiadd(self,ctx, *args):
        account = list(args)
        passfir = []
        errors = []
        error = ""
        for i in range(len(account)):
            if "https://twitter.com/" not in account[i]:
                errors.append(account[i])
                continue
            else:
                account[i] = account[i].split('/')[3]
                passfir.append(account[i])

        accounts = ",".join(passfir)
        with open(self.bot.tw_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)

        if len(accounts):
            url = f"https://api.twitter.com/2/users/by?usernames={accounts}&user.fields=profile_image_url"        

            response = requests.request("GET", url, headers=headers, data=payload)
            rlist = response.json()
            print(rlist)
            
            if "data" in rlist:
                for test in rlist["data"]:
                    flag = False
                    for data in accdata:
                        if test["id"] == data["id"]:
                            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("twi",f"{data['username']} already exist"))
                            passfir.remove(test["username"])
                            flag = True
                            break
                    
                    if flag != True:
                        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("twi",f"What channel you want {test['username']} to post from? Use channel id!"))
                        
                        channel = 0
                        try:
                            msg = await self.bot.wait_for("message", check=lambda x: x.author.id == ctx.author.id, timeout=60.0)
                        except asyncio.TimeoutError:
                            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("twi","You are run out of time, so I will post it on this channel."))
                            channel = ctx.channel.id
                        else:
                            for ch in ctx.guild.channels:
                                if int(msg.content) == ch.id:
                                    flag = True;
                                    channel = ch.id
                                    await msg.add_reaction('👍')
                                    break

                            if flag == False:
                                channel = ctx.channel.id
                                await msg.add_reaction('👎')
                                await msg.reply(embed = self.bot.simple_format("twi","I can't find it, so I will post it on this channel."))
                            
                        accdata.append({"id" : test["id"], "username" : f"{test['name']} (@{test['username']})", "url" : f"https://twitter.com/{test['username']}" ,"profileurl" : test["profile_image_url"], "lastpost" : datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+"Z", "channel" : channel})
                        passfir.remove(test["username"])

            if "errors" in rlist:
                for i in range(len(rlist["errors"])-1):
                    error += rlist["errors"][i]["value"]+', '
                error += rlist["errors"][len(rlist["errors"])-1]["value"]
                
        if error or len(errors):
            error += (', ' if errors else '' )+', '.join(str(v) for v in errors)
            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("twi",f"{error} can't found!"))

        with open(self.bot.tw_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))

        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("twi","added!"))


    @commands.command(hidden = True)
    async def tw_update_cod(self,ctx,accdata,tw_ind):
        url = f"https://api.twitter.com/2/users/{accdata[tw_ind]['id']}/tweets?max_results=15&start_time={accdata[tw_ind]['lastpost']}&expansions=attachments.media_keys&tweet.fields=created_at&media.fields=media_key,url,preview_image_url,type"
        channel = self.bot.get_channel(accdata[tw_ind]["channel"])
        response = requests.request("GET", url, headers=headers, data=payload)
        rlist = response.json()

        for j in range(rlist["meta"]["result_count"],0,-1):
            if rlist["data"][j-1]["created_at"] == accdata[tw_ind]["lastpost"]:
                continue
            embeds = discord.Embed(title=accdata[tw_ind]["username"], url=accdata[tw_ind]["url"], color=0x82CAFF)
            embeds.description = rlist["data"][j-1]["text"]
            embeds.set_thumbnail(url = accdata[tw_ind]["profileurl"])
            embeds.add_field(name = "tweet url", value = f"https://twitter.com/{accdata[tw_ind]['username'].split('(@')[1][:-1]}/status/{rlist['data'][j-1]['id']}", inline = False)
            if "attachments" in rlist["data"][j-1]:
                first = True
                for key in rlist["data"][j-1]["attachments"]["media_keys"]:
                    for matchkey in rlist["includes"]["media"]:
                        if key == matchkey["media_key"]:
                            if matchkey["type"] == "video" and first:
                                embeds.add_field(name = "photo", value = matchkey["preview_image_url"], inline = False)
                                embeds.set_image(url = matchkey["preview_image_url"])
                            elif matchkey["type"] == "photo" and first:
                                embeds.set_image(url = matchkey["url"])
                            
                            first = False
                            if first == False and matchkey["type"] == "photo":
                                embeds.add_field(name = "photo", value = matchkey["url"], inline = False)

                            break
            embeds.timestamp = dateutil.parser.isoparse(rlist["data"][j-1]["created_at"])

            if j-1 == 0:
                accdata[tw_ind]["lastpost"] = rlist["data"][0]["created_at"]
            
            await channel.send(embed=embeds)
            
        with open(self.bot.tw_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))


def setup(bot):
    bot.add_cog(Twitter(bot))