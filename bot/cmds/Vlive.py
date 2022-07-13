import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time
import datetime
import dateutil.parser
import json
import asyncio
import os
import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



class Vlive(Cog_Extension):
    # ---------------------------follow add---------------------------------
    @commands.command()
    async def vliadd(self,ctx,*args):
        #only accept Notice fir and StarB format
        
        with open(self.bot.vli_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        for arg in args:
            try:
                self.bot.vli_driver.get(arg)
            except:
                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli",f"{arg} didn't exist"))
                continue

            time.sleep(random.randint(3,6))
            soup = BeautifulSoup(self.bot.vli_driver.page_source, "html.parser")

            if soup.select('div[class^="empty_page"]'):
                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli",f"{arg} didn't exist"))
                continue
            chid = arg.split('/')[4]

            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli","data loading..."))
            flag = False
            for j in range(len(accdata)):
                if chid == accdata[j]["id"]:
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli",f"{arg} already exist"))
                    flag = True
                    break

            if flag != True:
                board = "https://www.vlive.tv"+soup.select('a[class^="board_link"]')[1].get("href")
                notice = "https://www.vlive.tv"+soup.select('a[class^="board_link"]')[0].get("href")
                profileurl = soup.find("img").get("src")
                username = soup.find("strong").get_text()
                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli","data loading..."))

                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli",f"What channel you want {username} to post from? Use channel id!"))
                
                channel = 0
                try:
                    msg = await self.bot.wait_for("message", check=lambda x: x.author.id == ctx.author.id, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli","You are run out of time, so I will post it on this channel."))
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
                        await msg.reply(embed = self.bot.simple_format("vli","I can't find it, so I will post it on this channel."))
                
                nowtime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+"Z"
                accdata.append({"id" : chid, "username" : username ,"url" : arg ,"profileurl" : profileurl, "starboard": board, "notice": notice, "lastpost" : nowtime, "nolastpost": nowtime, "channel" : channel})
            time.sleep(random.randint(3,6))

        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("vli","added!"))


        with open(self.bot.vli_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))


    @commands.command(hidden = True)
    async def vli_update_cod(self,ctx,accdata,vli_ind):
        channel = self.bot.get_channel(accdata[vli_ind]["channel"])

        self.bot.vli_task_driver.get(accdata[vli_ind]["starboard"])
        time.sleep(10)
        soup = BeautifulSoup(self.bot.vli_task_driver.page_source, "html.parser")
        if soup.select('a[class^="post_area"]'):
            for i in range(len(soup.select('a[class^="post_area"]'))):
                post = soup.select('a[class^="post_area"]')[i]

                liveflag = False
                    
                if post.select('em[class*=liveon]'):
                    liveflag = True

                url = "https://www.vlive.tv"+post.get("href")
                title = post.select_one('strong[class^="title_text"]').get_text()
                thumbstr = post.select_one('span[class^="covered_image"]')["style"]
                if liveflag:
                    thumbnail = thumbstr[thumbstr.find("url(\"")+5:thumbstr.find("\");")]
                else:
                    thumbnail = thumbstr[thumbstr.find("url(\"")+5:thumbstr.find("?type=")]

                self.bot.vli_task_driver.get(url)
                time.sleep(random.randint(8,10))
                posttime = self.bot.vli_task_driver.find_element(By.CSS_SELECTOR, "body > script[type='text/javascript']").get_attribute('innerHTML')
                posttimeslice = posttime[posttime.find(',"onAirStartAt":')+16:]
                posttime = datetime.datetime.fromtimestamp(int(posttimeslice[:posttimeslice.find('000,')]))
                posttimestr = posttime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+"Z"

                if dateutil.parser.isoparse(posttimestr) > dateutil.parser.isoparse(accdata[vli_ind]["lastpost"]):
                    if i == 0:
                        accdata[vli_ind]["lastpost"] = posttimestr
                    embeds = discord.Embed(title = title, url = url, color = 0x80ffff)
                    embeds.set_author(name = accdata[vli_ind]["username"], url = accdata[vli_ind]["url"], icon_url= accdata[vli_ind]["profileurl"])
                    if liveflag:
                        embeds.description = f"{accdata[vli_ind]['username']} is streaming!"
                    else:
                        embeds.description = f"{accdata[vli_ind]['username']} upload new video!"
                    
                    embeds.set_image(url = thumbnail)
                    embeds.timestamp = posttime

                    await channel.send(embed = embeds)
                else:
                    break

        
        self.bot.vli_task_driver.get(accdata[vli_ind]["notice"])
        time.sleep(10)
        soup = BeautifulSoup(self.bot.vli_task_driver.page_source, "html.parser")
        if soup.select('a[class^="post_item"]'):
            for i in range(len(soup.select('a[class^="post_item"]'))):
                post = soup.select('a[class^="post_item"]')[i]
                url = "https://www.vlive.tv"+post.select_one('a[class^="post_area"]').get("href")
                title = post.select_one('strong[class^="title_text"]').get_text()
                thumbstr = post.select_one('span[class^="covered_image"]').get("style")
                thumbnail = thumbstr[thumbstr.find("url(\"")+5:thumbstr.find("?type=")]
                authorname = post.select_one('em[class^="writer"]').get_text()
                authorpro = post.select_one('image[mask^="url(#thumbnail-mask-30)"]').get("xlink:href")
                authorurl = "https://www.vlive.tv"+post.select('a[class^="link_profile"]').get("href")

                self.bot.vli_task_driver.get(url)
                time.sleep(random.randint(8,10))
                posttime = self.bot.vli_task_driver.find_element(By.CSS_SELECTOR, "body > script[type='text/javascript']").get_attribute('innerHTML')
                posttimeslice = posttime[posttime.find(',"createdAt":')+13:]
                posttime = datetime.datetime.fromtimestamp(int(posttimeslice[:posttimeslice.find(',"')-3]))
                posttimestr = posttime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+"Z"

                if dateutil.parser.isoparse(posttimestr) > dateutil.parser.isoparse(accdata[vli_ind]["nolastpost"]):
                    if i == 0:
                        accdata[vli_ind]["nolastpost"] = posttimestr
                    embeds = discord.Embed(title = title, url = url, color = 0x80ffff)
                    embeds.set_author(name = authorname, url = authorurl, icon_url= authorpro)
                    embeds.description = f"{accdata[vli_ind]['username']} upload new post!"
                    embeds.set_image(url = thumbnail)
                    embeds.timestamp = posttime

                    await channel.send(embed = embeds)
                else:
                    break
        
        
        with open(self.bot.vli_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))

def setup(bot):
    bot.add_cog(Vlive(bot))