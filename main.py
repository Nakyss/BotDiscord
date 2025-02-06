import discord
from os import listdir, environ,path
from discord.ext import commands, tasks
from classServer import Server
import variable as v
from classDB import DB
from dotenv import load_dotenv
import functions as f

import datetime

load_dotenv('.env')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

client = discord.Client(intents=intents)

wasSent = True

@tasks.loop(hours = 2)
async def myLoop():
    await bot.change_presence(activity=discord.Game(f.activityName()))
    #change pp with a pp of one of the users

    if (f.luck(7)):
        with open(f.getARandomPP(), mode='rb') as file:
            try:
                await bot.user.edit(avatar=file.read())
                f.log(bot.user.name,"Change-is-profil-picture","everywhere")
            except discord.errors.HTTPException:
                print("changing pp to fast")
    else:
        if path.exists("pp/new_pp.png"):
            f.deleteFile("pp/new_pp.png")
            with open(environ.get('DISCORD_BOT_PP_PATH'), mode='rb') as file:
                await bot.user.edit(avatar=file.read())
    
@tasks.loop(minutes=2)
async def sendMessageEveryWere():
    global wasSent

    if datetime.datetime.now() >= datetime.datetime.strptime("2024-12-23 13:00:00", "%Y-%m-%d %H:%M:%S") and wasSent == False:
        message ="**Aujourd'hui ça fait 1 an que je suis sur discord ! 🎉🎉🎉**\n\nPour l'occasion vous pouvez accéder à votre rewind de l'année avec la commande `/rewind` \n\n Bonne fêtes de fin d'années\n -Bot2con"
        wasSent = True
        servers = v.db.getAllServer()
        for server in servers:
            thisserver = bot.get_guild(server[0])
            ls = ["GENERAL", "GÉNÉRAL"]
            sent_message = False  # Variable pour vérifier si un message a été envoyé
            print(thisserver.name)
            
            for channel in thisserver.text_channels:
                for word in ls:
                    if word in channel.name.upper():
                        await channel.send(message)
                        sent_message = True
                        break
                if sent_message:
                    break  # Quitte la boucle principale des canaux si un message a été envoyé

            if sent_message:
                continue  # Passe au prochain serveur s'il y a eu un message envoyé

            for channel in thisserver.text_channels:
                if len(channel.members) == channel.guild.member_count and channel.permissions_for(channel.guild.me).send_messages:
                    await channel.send(message)
                    break



@bot.event
async def on_ready():
    v.db = DB()

    #charge tout les cogs dans le dossier
    for filename in listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cogs chargé : {filename}")

    print(f'Connecté en tant que {bot.user.name}')

    # Crée un objet pour chaque server
    servers = v.db.getAllServer()
    for server in servers:
        v.allServer[server[0]] = Server(server[0])

    #synchronise les commandes avec discord et affiche le nombre de commandes
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

    myLoop.start()
    #sendMessageEveryWere.start()

if __name__ == "__main__":
    bot.run(environ.get('DISCORD_BOT_TOKEN'))
