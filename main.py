import discord
from os import listdir
import mysql.connector
import asyncio
from discord import app_commands
import functions as f
from random import randint, random
from discord.ext import commands
from variable import mydb

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


    #----------attend un temps random et rejoint un voc pour mettre airmax si il y a au moins 1 pers en voc
    while True:
        #genere le temps d'attente entre 25min et 7h
        waitTime = randint(1500,25200)
        await asyncio.sleep(waitTime)

        with mysql.connector.connect(**mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT ID_SERVER FROM SERVER WHERE CAN_JOIN_VOC = 1 AND STATUS = 1")
                result = c.fetchall()

        for server in result:
            guild = bot.get_guild(server[0])
            channel = guild.voice_channels[0]

            # Vérifie s'il y a au moins 1 personnes dans le canal vocal
            if len(channel.members) >= 1:
                # Génération d'un nombre aléatoire pour la condition "au hasard"
                random_number = random()

                # 50% de chance de rejoindre le canal vocal et de jouer une piste audio
                if random_number <= 0.3:
                    f.log(bot.user.name,"Play-music-start",f"{channel.guild.name} / {channel.name}")
                    voice_channel = channel
                    voice_client = await voice_channel.connect()

                    #faire une liste de tout les fichiers dans le dossier
                    if not f.folderExist("botSound",guild.id):
                        f.createFolder(guild.id,"botSound")
                    list = listdir(f"botSound/{guild.id}")
                    # Remplacez 'audio_file.mp3' par le chemin de votre fichier audio
                    voice_client.play(discord.FFmpegPCMAudio(f"botSound/{guild.id}/"+list[randint(0,len(list)-1)]))

                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                    await voice_client.disconnect()
                else :
                    f.log(bot.user.name,"Play-music-but-no-chance",f"{channel.guild.name} / {channel.name}")
            else :
                f.log(bot.user.name,"Play-music-but-nobody-in-channel",f"{channel.guild.name} / {channel.name}")

    


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