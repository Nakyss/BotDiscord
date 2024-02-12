import discord
import variable as v
import mysql.connector
import os



async def admin (bot,message):
    #Envoie le fichier de log
    if message.content.lower() == "log":
        await message.channel.send(content="Voila le fichier logs",file=discord.File("logs.csv"))

    #Envoie une liste des serveurs
    elif message.content.lower() == "server":
        with mysql.connector.connect(**v.mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT NAME, NB_USER, DATE_FORMAT(JOIN_DATE, '%e/%M/%Y'), CAN_JOIN_VOC, STATUS FROM SERVER")
                result = c.fetchall()
        sendableMesseage = '```'
        for serv in result:
            sendableMesseage += f'\n{serv[0]} -  {serv[1]} Utilisateurs  -  Depuis le {serv[2]}  -  Peut rejoindre le voc :{serv[3]}  -  Status : {serv[4]}'
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)

    #Envoie les infos des 10 dernier messages
    elif message.content.lower() == "message":
        with mysql.connector.connect(**v.mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT U.NAME_GLOBAL, M.LENGTH, M.NB_ATTACHMEMTS, DATE_FORMAT(DATE, '%H:%i %e/%m/%Y') FROM MESSAGE M JOIN USER U ON U.ID_USER = M.ID_USER ORDER BY M.DATE DESC LIMIT 10")
                result = c.fetchall()
        sendableMesseage = '```'
        for mess in result:
            sendableMesseage += f'\n{mess[0]} - {mess[1]} Caractères - {mess[2]} Fichier - {mess[3]} '
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)
    
    #Recharge un cog ou tous
    elif message.content.lower().startswith("reload"):
        if message.content.lower()=="reload all":
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    if filename[:-3] not in ["view"]:
                        await bot.reload_extension(f"cogs.{filename[:-3]}")
                        print(f"Cogs chargé : {filename}")
            await message.reply(f"tout les cogs rechargé")
        else:
            splited = message.content.split(' ')
            cogs = os.listdir("cogs")
            if splited[1] in cogs:
                await bot.reload_extension(f"cogs.{splited[1][:-3]}")
                print(f"{splited[1]} à été rechargé")
                await message.reply(f"{splited[1]} rechargé")
            else:
                await message.reply(f"{splited[1]} introuvable")

    #Charge un Cog
    elif message.content.lower().startswith("load"):
        splited = message.content.split(' ')
        cogs = os.listdir("cogs")
        if splited[1] in cogs:
            await bot.load_extension(f"cogs.{splited[1][:-3]}")
            print(f"{splited[1]} à été chargé")
            await message.reply(f"{splited[1]} chargé")
        else:
            await message.reply(f"{splited[1]} introuvable")

    #Affiche la liste des serveur avec le random join lancé
    elif message.content.lower() == "random join":
        if len(v.guild_status) != 0:
            sendableMesseage = '```'
            for serv in v.guild_status:
                sendableMesseage += f'\n{serv}'
            sendableMesseage += '\n```'
            await message.channel.send(sendableMesseage)
        else:
            await message.reply("Random join n'est actif sur aucun serveur")

    #Affiche la liste des cogs
    elif message.content.lower() == "ls cogs":
        cogs = os.listdir("cogs")
        sendableMesseage = '```'
        for cog in cogs:
                if cog.endswith(".py"):
                    sendableMesseage += f'\n{cog}'
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)

    #Affiche la liste des possibilé de commande
    elif message.content.lower() == "ls":
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

    elif message.content.lower() == "sync":
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
            await message.reply(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)