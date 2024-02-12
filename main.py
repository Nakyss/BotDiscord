import discord
from os import listdir
from discord import app_commands
import functions as f
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



#Liste des différentes possibilités de message ainsi que leurs réponses

@bot.event
async def on_ready():
    for filename in listdir("cogs"):
        if filename.endswith(".py"):
            if filename[:-3] not in ["view"]:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Cogs chargé : {filename}")

    print(f'Connecté en tant que {bot.user.name}')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)



#----------------------------------------------------------------------------------------------------
#---                                    SERVER MANAGEMENT                                         ---
#----------------------------------------------------------------------------------------------------




            
#------------------------quand le bot est ajouter a un server---------------------------
@bot.event
async def on_guild_join(guild):
    f.log(bot.user.name,"Added-to-server",guild.name)
    if not f.isServerExist(guild):
        f.createServer(guild)
    else:
        f.updateServer(guild)


@bot.event
async def on_guild_remove(guild):
    f.log(bot.user.name,"Kick-from-server",guild.name)
    f.updateServer(guild,0)

#-----------------------changement dans sur le serveur----------------------------------
@bot.event
async def on_guild_update(before, after):
    if f.isServerExist(after):
        f.updateServer(after)
    else:
        f.createServer(after)

#----------------------changement de nb User--------------------------------------------
@bot.event
async def on_member_join(member):
    if f.isServerExist(member.guild):
        f.updateServer(member.guild)
    else:
        f.createServer(member.guild)
    

@bot.event
async def on_member_remove(member):
    if f.isServerExist(member.guild):
        f.updateServer(member.guild)
    else:
        f.createServer(member.guild)



bot.run(f.readToken("token_discord.txt"))