import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)



@bot.command()
async def latest(ctx):
    url = 'https://mangabuddy.com/latest'
    browser = webdriver.Chrome()
    browser.delete_all_cookies()
    browser.get(url)
    bait = browser.find_elements(By.TAG_NAME, 'h3')
    chapters = browser.find_elements(By.CLASS_NAME, 'latest-chapter')
    embedvar = discord.Embed(title="**__TOP 10 LATEST UPDATES__**", color=0x0000FF)
    count = 10
    start = 0
    for tit in bait:
        if(count > start):           
            linkExtension = "https://mangabuddy.com/" + tit.text.replace(' ', '-')
            embedvar.add_field(name='**TITLE: **' + tit.text , value= "**Chapter:**" + chapters[start].text.replace('CHAPTER', '') + " [READ HERE]" + "(" + linkExtension + ")", inline=False)
            start += 1
        else:
            break
    browser.close()
    await ctx.send(embed = embedvar)
    

bot.run(os.environ.get("api-token"))