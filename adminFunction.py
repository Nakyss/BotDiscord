import discord
from variable import db
import variable as v
import os


async def admin (bot,message):
    #Envoie le fichier de log
    if message.content.lower()[4:] == "log":
        await message.channel.send(content="Voila le fichier logs",file=discord.File("logs.csv"))

    #Envoie une liste des serveurs
    elif message.content.lower()[4:] == "server":
        result = db.select("SELECT NAME, NB_USER, DATE_FORMAT(JOIN_DATE, '%e/%M/%Y'), CAN_JOIN_VOC, STATUS FROM SERVER")
        sendableMesseage = '```'
        for serv in result:
            sendableMesseage += f'\n{serv[0]} -  {serv[1]} Utilisateurs  -  Depuis le {serv[2]}  -  Peut rejoindre le voc :{serv[3]}  -  Status : {serv[4]}'
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)

    #Envoie les infos des 10 dernier messages
    elif message.content.lower()[4:] == "message":
        result = db.select("SELECT U.NAME_GLOBAL, M.LENGTH, M.NB_ATTACHMEMTS, DATE_FORMAT(DATE, '%H:%i %e/%m/%Y') FROM MESSAGE M JOIN USER U ON U.ID_USER = M.ID_USER ORDER BY M.DATE DESC LIMIT 10")
        sendableMesseage = '```'
        for mess in result:
            sendableMesseage += f'\n{mess[0]} - {mess[1]} Caractères - {mess[2]} Fichier - {mess[3]} '
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)
    
    #Recharge un cog ou tous
    elif message.content.lower().startswith("cmd reload"):
        if message.content.lower()=="cmd reload all":
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    if filename[:-3] not in ["view"]:
                        await bot.reload_extension(f"cogs.{filename[:-3]}")
                        print(f"Cogs chargé : {filename}")
            await message.reply(f"tout les cogs rechargé")
        else:
            content = message.content[4:]
            splited = content.split(' ')
            cogs = os.listdir("cogs")
            if splited[1] in cogs:
                await bot.reload_extension(f"cogs.{splited[1][:-3]}")
                print(f"{splited[1]} à été rechargé")
                await message.reply(f"{splited[1]} rechargé")
            else:
                await message.reply(f"{splited[1]} introuvable")

    #Charge un Cog
    elif message.content.lower().startswith("cmd load"):
        content = message.content[4:]
        splited = content.split(' ')
        cogs = os.listdir("cogs")
        if splited[1] in cogs:
            await bot.load_extension(f"cogs.{splited[1][:-3]}")
            print(f"{splited[1]} à été chargé")
            await message.reply(f"{splited[1]} chargé")
        else:
            await message.reply(f"{splited[1]} introuvable")

    #Affiche la liste des serveur avec le random join lancé
    elif message.content.lower()[4:] == "random join":
        sendableMesseage = '```'
        nbServ = 0
        for server in v.allServer:
            if v.allServer[server].isRandomJoinActive:
                nbServ +=1
                sendableMesseage += f'{v.allServer[server].id}'
        sendableMesseage += '\n```'

        if nbServ == 0:
            await message.reply("Random join n'est actif sur aucun serveur")
        else:
            await message.channel.send(sendableMesseage)

    #Affiche la liste des cogs
    elif message.content.lower()[4:] == "ls cogs":
        cogs = os.listdir("cogs")
        sendableMesseage = '```'
        for cog in cogs:
                if cog.endswith(".py"):
                    sendableMesseage += f'\n{cog}'
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)

    #Affiche la liste des possibilé de commande
    elif message.content.lower()[4:] == "ls":
        sendableMesseage = "```"
        sendableMesseage+= "log\n"
        sendableMesseage+= "server\n"
        sendableMesseage+= "message\n"
        sendableMesseage+= "reload\n"
        sendableMesseage+= "load\n"
        sendableMesseage+= "random join\n"
        sendableMesseage+= "sync\n"
        sendableMesseage+= "ls cogs ```"
        await message.reply(sendableMesseage)

    elif message.content.lower()[4:] == "sync":
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
            await message.reply(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

    elif message.content.lower()[4:] == "deco":
        db.disconnect()
        await message.reply("deco")
