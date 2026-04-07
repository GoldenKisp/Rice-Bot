"""
Title: Rice Bot
Description: Custom made Discord bot using py-cord's API
Date Created: 10/13/22
Author: GoldenKisp
"""

# Required Packages
from discord.ext.commands import MissingPermissions
from discord.commands import Option
from discord.ext import commands
from discord.ui import Button
from discord.ui import View
import wikipedia
import datetime
import asyncio
import discord
import random
import time
import json
import os
#--------------------------------------------------#

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)
helpGuide = json.load(open("help.json"))
#--------------------------------------------------#

# Variables
color = 5763719
colorfail = 15548997
riceFail = "<:riceFail:1049137599408779294>"
riceSuccess = "<:riceSuccess:1049137555771228201>"	
blacklisted = []
#--------------------------------------------------#

# On Ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('with RICE'))
    print(f'Logged in as {bot.user.name} | ID: {bot.user.id}')
#--------------------------------------------------#

# Help Command
def createHelpEmbed(pageNum=0, inline=False):
	pageNum = (pageNum) % len(list(helpGuide))
	pageTitle = list(helpGuide)[pageNum]
	embed=discord.Embed(color=color, title=pageTitle)
	for key, val in helpGuide[pageTitle].items():
		embed.add_field(name=key, value=val, inline=inline)
		embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
	return embed

@bot.slash_command(name="help", description="Help Command")
async def help(ctx):
	currentPage = 0
	async def next_callback(interaction):
		nonlocal currentPage, sent_msg
		currentPage += 1
		await interaction.response.edit_message(embed=createHelpEmbed(pageNum=currentPage), view=myview)

	async def previous_callback(interaction):
		nonlocal currentPage, sent_msg
		currentPage -= 1
		await interaction.response.edit_message(embed=createHelpEmbed(pageNum=currentPage), view=myview)

	previousButton = Button(label="◀️", style=discord.ButtonStyle.blurple)
	nextButton = Button(label="▶️", style=discord.ButtonStyle.blurple)
	previousButton.callback = previous_callback
	nextButton.callback =  next_callback
	myview = View(timeout=180)
	myview.add_item(previousButton)
	myview.add_item(nextButton)
	sent_msg = await ctx.respond(embed=createHelpEmbed(currentPage), view=myview)
#--------------------------------------------------#

# Moderation
@bot.slash_command(name="kick", description="Kick a member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason: str):
    if user.guild_permissions.kick_members:
      embed = discord.Embed(color=colorfail, description=f"{riceFail} That user is a mod/admin, I can't do that")
      await ctx.respond(embed=embed)
    else:
      await user.kick(reason=reason)
      embed = discord.Embed(color=color, description=f"{riceSuccess} {user.mention} was kicked")
      await ctx.respond(embed=embed)
@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
      embed = discord.Embed(color=colorfail, description=f"{riceFail} You are not authorized to use this command")
      await ctx.respond(embed=embed)
    else:
      embed = discord.Embed(color=colorfail, description=f"{riceFail} Bot is missing access")
      await ctx.respond(embed=embed)

@bot.slash_command(name="ban", description="Ban a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    if user.guild_permissions.ban_members:
      embed=discord.Embed(color=colorfail)
      embed = discord.Embed(color=colorfail, description=f"{riceFail} That user is a mod/admin, I can't do that")
      await ctx.respond(embed=embed)
    else:
      await user.ban(reason=reason)
      embed = discord.Embed(color=color, description=f"{riceSuccess} {user.mention} was banned")
      await ctx.respond(embed=embed)
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
      embed = discord.Embed(color=colorfail, description=f"{riceFail} You are not authorized to use this command")
      await ctx.respond(embed=embed)
    else:
      embed = discord.Embed(color=colorfail, description=f"{riceFail} Bot is missing access")
      await ctx.respond(embed=embed)

@bot.slash_command(name="purge", description="Deletes messages")
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, count: Option(int, required = True, max_value=50)):
  await ctx.defer()
  purgelen = await ctx.channel.purge(limit = count + 1)
  embed = discord.Embed(color=color, description=f"{riceSuccess} I have purged {len(purgelen)-1} messages!")
  await ctx.send(embed=embed, delete_after=5)
@purge.error
async def purgeerror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed = discord.Embed(color=colorfail, description=f"{riceFail} {error}")
      await ctx.respond(embed=embed)
    elif isinstance(error, MissingPermissions):
      embed = discord.Embed(color=colorfail, description=f"{riceFail} You are not authorized to use this command")
      await ctx.respond(embed=embed)
    else:
      embed = discord.Embed(color=colorfail, description=f"{riceFail} Bot is missing access")
      await ctx.respond(embed=embed)
#--------------------------------------------------#

# Slash Commands
@bot.slash_command(name="ping", description="Bot Latency")
async def ping(ctx):
    latency = round(bot.latency * 1000, 1)
    embed = discord.Embed(color=color, description=f"Pong! {latency}ms")
    await ctx.respond(embed=embed)

@bot.slash_command(name="devping",description="Ping a specific role")
@commands.cooldown(1, 7200, commands.BucketType.user)
@commands.has_role("Serverevents")
async def devping(ctx, role: Option(str, "Ping a specific role", choices=["Giveaway", "Event"])):
    if role == "Giveaway":
        if ctx.channel.id == 1038551210111795380:
            embed = discord.Embed(color=color, description=f"{riceSuccess} Pinged Giveaways")
            await ctx.respond(embed=embed, ephemeral=True)
            await ctx.send("<@&1033379696567648257>, deleting in 5 seconds", delete_after=5)
        else:
            embed = discord.Embed(color=colorfail, description=f"{riceFail} You can only run this commmand in <#1038551210111795380>")
            await ctx.respond(embed=embed)
    elif role == "Event":
        if ctx.channel.id == 1058211124618727485:
            embed = discord.Embed(color=color, description=f"{riceSuccess} Pinged Events")
            await ctx.respond(embed=embed, ephemeral=True)
            await ctx.send("<@&1058211200627912725>, deleteing in 5 seconds", delete_after=5)
        else:
            embed = discord.Embed(color=colorfail, description=f"{riceFail} You can only run this commmand in <#1058211124618727485>")
            await ctx.respond(embed=embed)
    else:
            devping.reset_cooldown(ctx)
            embed = discord.Embed(color=colorfail, description=f"{riceFail} Unable to ping that role")
            await ctx.respond(embed=embed)
@devping.error
async def devping(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      time = datetime.datetime.utcnow().timestamp() + error.retry_after
      embed = discord.Embed(color=colorfail, description=f'{riceFail} This command is on cooldown, Try again in <t:%d:R>' % time)
      await ctx.respond(embed=embed)
    else:
      embed = discord.Embed(color=colorfail, description=f"{riceFail} You are not authorized to use this command")
      await ctx.respond(embed=embed)

@bot.slash_command(name="8ball", description="8Ball Command")
async def eightball(ctx, *, question: str):
    responses = ['100% no doubt', 'That is kinda obvious', 'Most likely', 'About 75% chance yes', 'Maybe not', 'No', 'You know thats a no', 'Not a chance']
    embed = discord.Embed(color=color, description=f'🇶 Question: {question}\n🇦 Answer: {random.choice(responses)}')
    await ctx.respond(embed=embed)

@bot.slash_command(name="ricefacts", description="Fun facts about rice")
async def ricefacts(ctx):
    embed = discord.Embed(color=color)
    rf = open("ricefacts.txt", "r")
    rflines = rf.readlines()
    rfsend = random.choice(rflines)
    embed.add_field(name="Rice Fact", value=f"{rfsend}")
    await ctx.respond(embed=embed)

@bot.slash_command(name = 'wikipedia', description='Returns a Wikipedia summary')
async def summary(ctx, search: Option(str, required = True)):
    if ctx.author.id in blacklisted:
      embed = discord.Embed(color=colorfail)
      embed.add_field(name="Blacklisted", value=f"{riceFail} You are blacklisted to use this command!")
      embed.set_image(url="https://media.tenor.com/wIxFiobxxbIAAAAd/john-jonah-jameson-lol.gif")
      await ctx.respond(embed=embed)
    else:
      await ctx.channel.trigger_typing()
      try:
          thesummary = wikipedia.summary(search, chars = 1950)
          try:
              await ctx.respond(thesummary)
          except:
              await ctx.send("")
      except:
          searchsummary = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
          try:

              await ctx.respond(f"I can't seem to find a summary for that.. Did you mean: {searchsummary}")
          except:
              await ctx.send("")

bot.run("")
