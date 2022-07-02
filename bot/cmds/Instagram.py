import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time
import datetime
import json
import asyncio
import dateutil.parser
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

path = Path(os.path.dirname(__file__)).parent.absolute()
sec_path = str(path) + "/secretdata.json"
with open(sec_path, "r", encoding="utf-8") as file:
    secdata = json.load(file)

class Instagram(Cog_Extension):
    # ---------------------------follow add---------------------------------
    @commands.command()
    async def login(self,ctx):
        self.bot.ins_driver.set_window_size(1920, 1080)
        self.bot.ins_driver.get("https://www.instagram.com/")
        time.sleep(5)
        username = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        username.send_keys(secdata["Instagram"]["account"])
        password = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password.send_keys(secdata["Instagram"]["passward"])
        time.sleep(5)
        login = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login.click()
        time.sleep(10)

        self.bot.ins_driver.get_screenshot_as_file("screenshot.png")
        

    @commands.command()
    async def insadd(self,ctx,*args):
        with open(self.bot.ins_csv_path, "r", encoding="utf-8") as file:
            accdata = json.load(file)
        
        errors = []
        for arg in args:
            if "https://www.instagram.com/" not in arg:
                errors.append(arg)
                continue

            self.bot.ins_driver.get(arg)
            time.sleep(10)

            try:
                self.bot.ins_driver.find_element(By.CLASS_NAME, "_aa_t")
            except:
                pass
            else:
                errors.append(arg)
                continue

            userid = arg.split('/')[3]
            
            flag = True
            for data in accdata:
                if data["id"] == userid:
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ins",f"{userid} already exist"))
                    flag = False
                    break
            
            if flag:
                profileurl = self.bot.ins_driver.find_element(By.CLASS_NAME, "_aa8j").get_attribute('src')
                try:
                    username = self.bot.ins_driver.find_element(By.CLASS_NAME, "_aacl._aacp._aacw._aacx._aad7._aade").text
                except:
                    username = userid

                shorttime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+"Z"
                lastpost = shorttime

                await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ins",f"What channel you want {username} to post from? Use channel id!"))
                
                channel = 0
                try:
                    msg = await self.bot.wait_for("message", check=lambda x: x.author.id == ctx.author.id, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ins","You are run out of time, so I will post it on this channel."))
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
                        await msg.reply(embed = self.bot.simple_format("ins","I can't find it, so I will post it on this channel."))
                
                accdata.append({"id": userid, "username" : username, "url" : arg, "profileurl": profileurl, "lastpost": lastpost, "lastshort": shorttime, "channel": channel})

            time.sleep(random.randint(3,6))
    
        if errors:
            error = ', '.join(str(v) for v in errors)
            await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ins",f"{error} can't found! or maybe it is private."))

        with open(self.bot.ins_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))
        
        await ctx.channel.send(ctx.message.author.mention, embed = self.bot.simple_format("ins","added!"))


    @commands.command(hidden = True)
    async def ins_update_cod(self,ctx,accdata,ins_ind):
        channel = self.bot.get_channel(accdata[ins_ind]["channel"])

        lastshort = dateutil.parser.isoparse(accdata[ins_ind]["lastshort"])
        lastpost = dateutil.parser.isoparse(accdata[ins_ind]["lastpost"])

        self.bot.ins_driver.get(accdata[ins_ind]["url"])
        time.sleep(random.randint(10,15))
        posts = self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aabd._aa8k._aanf")
        WebDriverWait(self.bot.ins_driver, 60).until(EC.element_to_be_clickable(posts[0].find_element(By.CSS_SELECTOR, "[role='link']"))).click()
        for j in range(len(posts)):
            time.sleep(random.randint(5,10))
            postdatatime = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "time[class='_aaqe']").get_attribute("datetime")
            posttime = dateutil.parser.isoparse(postdatatime)
            if posttime > lastpost:
                if j == 0:
                    accdata[ins_ind]["lastpost"] = postdatatime
                embeds = discord.Embed(title = accdata[ins_ind]["username"]+ " new post!", url = self.bot.ins_driver.current_url, color=0x7D0552)
                embeds.description = self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aacl._aaco._aacu._aacx._aad7._aade")[0].text
                embeds.set_author(name = accdata[ins_ind]["username"],url = accdata[ins_ind]["url"], icon_url=accdata[ins_ind]["profileurl"])
                if self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aagu._aamh") or self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aagu._aato"):
                    try:
                        embeds.set_image(url = self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aagu._aamh")[0].find_element(By.CLASS_NAME,"_aagt").get_attribute("src"))
                    except:
                        embeds.set_image(url = self.bot.ins_driver.find_elements(By.CLASS_NAME, "_aagu._aato")[0].find_element(By.CLASS_NAME,"_aagt").get_attribute("src"))
                else:
                    embeds.set_image(url = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "[class^='_ab1d']").get_attribute("poster"))
                
                embeds.timestamp = posttime

                await channel.send(embed = embeds)

            else:
                break

            self.bot.ins_driver.find_element(By.CLASS_NAME, "_aaqg._aaqh").find_element(By.CSS_SELECTOR, "button[class='_abl-']").click()

        self.bot.ins_driver.get(accdata[ins_ind]["url"])
        time.sleep(random.randint(10,15))
        short = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "[class^='_aarf']")
        if short.get_attribute("tabindex") == '-1':
            pass
        else:
            short.click()
            time.sleep(3)
            try:
                self.bot.find_element(By.CLASS_NAME,"_acan._acap._acau._acav")
            except:
                pass
            else:
                print("here")
                self.bot.find_element(By.CLASS_NAME,"_acan._acap._acau._acav").click()

            stopbu = self.bot.ins_driver.find_elements(By.CSS_SELECTOR, "button[class='_abl-'][type='button']")[0]
            WebDriverWait(self.bot.ins_driver, 60).until(EC.element_to_be_clickable(stopbu)).click()
        
            while True:  
                if "https://www.instagram.com/stories/" not in self.bot.ins_driver.current_url:
                    break
                        
                postdatatime = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "time[class='_ac0t']").get_attribute("datetime")
                shorttime = dateutil.parser.isoparse(postdatatime)

                if shorttime > lastshort:
                    embeds = discord.Embed(title = accdata[ins_ind]["username"]+ " new short!", url = self.bot.ins_driver.current_url, color=0x7D0552)
                    embeds.set_author(name = accdata[ins_ind]["username"],url = accdata[ins_ind]["url"], icon_url=accdata[ins_ind]["profileurl"])
                    embeds.set_image(url = self.bot.ins_driver.find_element(By.CSS_SELECTOR, "img[class^='_aa63']").get_attribute("src"))
                    embeds.timestamp = shorttime

                    accdata[ins_ind]["lastshort"] = postdatatime
                    await channel.send(embed = embeds)
                
                WebDriverWait(self.bot.ins_driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='_ac0d']"))).click()
                time.sleep(2)
                stopbu = self.bot.ins_driver.find_elements(By.CSS_SELECTOR, "button[class='_abl-'][type='button']")[0]
                WebDriverWait(self.bot.ins_driver, 60).until(EC.element_to_be_clickable(stopbu)).click()

        with open(self.bot.ins_csv_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(accdata, ensure_ascii=False, indent=1))
    

def setup(bot):
    bot.add_cog(Instagram(bot))