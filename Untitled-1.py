from email import message
import atexit
from logging import exception
from datetime import datetime
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
now = datetime.now()
date_time = now.strftime("%m-%d-%Y_%H.%M.%S")
logfile = open("logs/" + date_time + ".txt", "w+")

@atexit.register 
def goodbye(): 
    logfile.close()
    print("Exiting Python Script!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("The fuck am I searching idiot, you didn’t give me shit to search for. Do you need another brain cell or something?")

@bot.command()
async def latest(ctx):
    author = ctx.message.author
    print(author.name + " Has sent the latest command which was >latest")
    logfile.write(author.name + " Has sent the latest command which was >latest\n")
    logfile.flush()
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
    
@bot.command()
async def search(ctx, *, messages: str): 
    author = ctx.message.author
    print(author.name + " has sent the search command which was >search " + messages)
    logfile.write(author.name + " has sent the search command which was >search " + messages + "\n")
    logfile.flush()
    await ctx.send(messages)
    

bot.run(os.environ.get("api-token"))