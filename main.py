import discord
from os import listdir, environ
from discord.ext import commands
from classServer import Server
import variable as v
from classDB import DB
from dotenv import load_dotenv

load_dotenv('.env')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

client = discord.Client(intents=intents)


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

    game = discord.Game("Pignouf")
    await bot.change_presence(activity=game)


bot.run(environ.get('DISCORD_BOT_TOKEN'))
