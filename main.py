import discord
from os import listdir, environ,path
from discord.ext import commands, tasks
from classServer import Server
import variable as v
from classDB import DB
from dotenv import load_dotenv
import functions as f

load_dotenv('.env')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

client = discord.Client(intents=intents)

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

if __name__ == "__main__":
    bot.run(environ.get('DISCORD_BOT_TOKEN'))
