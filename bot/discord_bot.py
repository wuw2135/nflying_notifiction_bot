import discord
from discord.ext import commands

import datetime
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------Data Location---------------------------------
tw_csv_path = "cmds\data\Twitterfol.json"
tw_csv_path = os.path.join(os.path.dirname(__file__), tw_csv_path)
bot.tw_csv_path = tw_csv_path

options = Options()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"')
options.add_argument("--disable-notifications")

vli_dri_path = 'cmds\data\driver_vli_com.exe'
vli_dri_path = os.path.join(os.path.dirname(__file__), vli_dri_path)
vli_driver = webdriver.Chrome(vli_dri_path, chrome_options=options)
bot.vli_driver = vli_driver

vli_task_dri_path = 'cmds\data\driver_vli_cra.exe'
vli_task_dri_path = os.path.join(os.path.dirname(__file__), vli_task_dri_path)
bot.vli_task_driver = webdriver.Chrome(vli_task_dri_path, options=options)

ins_dri_path = 'cmds\data\driver_ins_com.exe'
ins_dri_path = os.path.join(os.path.dirname(__file__), ins_dri_path)
ins_driver = webdriver.Chrome(ins_dri_path, chrome_options=options)
bot.ins_driver = ins_driver

vli_csv_path = "cmds\data\Vlivefol.json"
vli_csv_path = os.path.join(os.path.dirname(__file__), vli_csv_path)
bot.vli_csv_path = vli_csv_path

yt_csv_path = "cmds\data\Youtubefol.json"
yt_csv_path = os.path.join(os.path.dirname(__file__), yt_csv_path)
bot.yt_csv_path = yt_csv_path

ytl_csv_path = "cmds\data\YoutubeLivefol.json"
ytl_csv_path = os.path.join(os.path.dirname(__file__), ytl_csv_path)
bot.ytl_csv_path = ytl_csv_path

ins_csv_path = "cmds\data\Instagramfol.json"
ins_csv_path = os.path.join(os.path.dirname(__file__), ins_csv_path)
bot.ins_csv_path = ins_csv_path

# ---------------------------Often Use Function---------------------------------
def simple_format(key,reply=str):
    color = 0x82CAFF
    if key == "twi":
        color = 0x82CAFF
    elif key == "yt" or key == "ytl":
        color = 0xff0000
    elif key == "vli":
        color = 0x80ffff
    elif key == "ins":
        color = 0x7D0552

    embed = discord.Embed(title=reply, color=color)
    return embed

bot.simple_format = simple_format

def search_embed(key,reply):
    color = 0x82CAFF
    fol = ""
    url = ""
    if key == "twi":
        fol = "Twitter"
        color = 0x82CAFF
        url = "http://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png"
    elif key == "yt" or key == "ytl":
        if key == "ytl":
            fol = "Youtube Live"
        else:
            fol = "Youtube"
        color = 0xff0000
        url = "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
    elif key == "vli":
        fol = "Vlive"
        color = 0x80ffff
        url = "https://ssl.pstatic.net/static/m/vlive/mobile/2020/09/16/android_192x192_xxxhpdi.png"
    elif key == "ins":
        fol = "Instagram"
        color = 0x7D0552
        url = "https://cdn-icons-png.flaticon.com/512/174/174855.png"

    embed = discord.Embed(title=f"{fol} Follow", color=color)
    embed.set_thumbnail(url=url)
    for i in range(len(reply)):
        embed.add_field(name=reply[i]["username"], value=f"id: {reply[i]['id']}\nurl: {reply[i]['url']}\nchannel: {str(reply[i]['channel'])}\nlast post: {reply[i]['lastpost']}", inline= False)
    embed.timestamp = datetime.datetime.utcnow()
    return embed

bot.search_embed = search_embed


# ---------------------------join server---------------------------------


@bot.event
async def on_guild_join(guild):
    await guild.text_channels[0].send(
        "已加入 {}!\n請先設定更新訊息發送頻道!\n若未設定將不發送任何更新訊息!".format(guild.name)
    )


# ---------------------------send update message---------------------------------


@bot.event
async def on_ready():
    print("Bot已經上線!")


# ---------------------------custom help---------------------------------


# ---------------------------update---------------------------------
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")


if __name__ == "__main__":
    sec_path = "secretdata.json"
    sec_path = os.path.join(os.path.dirname(__file__), sec_path)
    with open(sec_path, "r", encoding="utf-8") as file:
        secdata = json.load(file)
    bot.run(secdata["Discord"]["token"])
