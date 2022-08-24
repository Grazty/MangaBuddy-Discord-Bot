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
    fullmessage = ''
    bait = browser.find_elements(By.TAG_NAME, 'h3')
    chapters = browser.find_elements(By.CLASS_NAME, 'latest-chapter')
    count = 10
    start = 0
    fullmessage += ("**__TOP 10 LATEST UPDATES__**"+ '\n')
    for tit in bait:
        if(count > start):
            fullmessage += ('**TITLE: **' + tit.text + " **Chapter:**" + chapters[start].text.replace('CHAPTER', '') + '\n')
            start += 1
        else:
            break
    browser.close()
    await ctx.send(fullmessage)
    

bot.run(os.environ.get("api-token"))