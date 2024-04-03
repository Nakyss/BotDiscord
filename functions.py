import re
import json
from datetime import datetime
import pytz
import csv
import mysql.connector
import os
import shutil
import discord
from random import randint,random
import asyncio
from mutagen.mp3 import MP3
from variable import mydb
import variable as v
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
ytdl = YoutubeDL(YDL_OPTIONS)

def retirer_points(message:str):
    """Enlever la ponctuation d'un message"""

    caracteres = "!? ."
    message = message.lower()
    for x in range(len(caracteres)):
        message = message.replace(caracteres[x],"")
    return message

def procedNb(nbRep:str):
    """Transforme un str en chiffre en enlevant tout ce qui n'est pas un chiffre"""

    chiffre = re.sub(r'\D', '',nbRep)

    if (chiffre == ''):
        chiffre = '10'
    chiffre = int(chiffre)
    return chiffre

def cutMessage(message:str):
    """Coupe le message et renvoie un tableau avec le contenue et le nombre de repetition """

    #ajoute 2 espace apres les message dans le cas ou il n'y a pas d'espace pour que le split marche
    message += '  '

    #coupe le message en 3 a chaque esapce 
    splited = message.split(' ',2)


    #si le Message est vide
    if (splited[2] == '' or splited[2].startswith(' ')):
        splited[2] = "OUAIS OUAIS OUAIS"
    else:
        #enleve les suites d'espace 
        splited[2] = splited[2].strip()

    splited[1] = procedNb(splited[1])

    return splited

def calculNbMess(message:str,nbRep:int):
    """Retourne un tableau avec le nombre de message à envoyé, le nombre de rep dans les n-1 message et le nombre de rep dans le dernier."""

    tab=[5,0,0]

    #Nombre de fois le message à spam par message envoyé
    nbByMess = nbRep//5

    #Nombre de fois le message à spam pour le dernier message à envoyé
    lastMess = nbRep%5

    #Nombre de caractères par message envoyé.
    nbChar = (len(message)+1)*nbByMess

    #ça je l'ai fait mais j'ai aucune idée comment ça marche 
    if (nbChar > 2000):
        nbByMess = 2000 / int(len(message)+1)
        nbByMess=int(nbByMess)
        totalRep = nbByMess * 5

        while (nbRep - totalRep > nbByMess):
            totalRep += nbByMess
            tab[0] += 1

        lastMess = nbRep - totalRep

    tab[1] = nbByMess
    tab[2] = lastMess

    return tab

def readToken(emplacement = "token_discord.txt"):
    """Retourne le token ou n'importe quel texte entrée en première ligne d'un fichier txt"""
    fichier = open(emplacement, 'r')
    return(fichier.readline())

def getTime():
    """Retourne le timestamp de la date, heure actuel"""
    # Getting the current date and time
    dt = datetime.now()

    # getting the timestamp
    ts = datetime.timestamp(dt)

    return int(ts)

def getTimeV2():
    """Retourne l'heure et la date au format DD-MM-YYYY HH:mm:SS"""
    # Obtenez le fuseau horaire de Paris
    paris_tz = pytz.timezone('Europe/Paris')

    # Obtenez la date et l'heure actuelles en UTC
    utc_now = datetime.utcnow()

    # Convertissez la date et l'heure en UTC en utilisant le fuseau horaire de Paris
    paris_now = utc_now.replace(tzinfo=pytz.utc).astimezone(paris_tz)

    # Formatez la date et l'heure au format souhaité
    return paris_now.strftime("%d-%m-%y %H:%M:%S")

def log(user,action,place):
    """Ajoute des infos log dans le fichier logs.csv"""
    time = getTimeV2()
    print(f"{time} - {user} - {action} in {place}")
    
    with open('logs.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([time,user,action,place])

def clearQuotes(message):
    """ajoute des backslash devant les ' pour eviter les probleme avec SQL"""
    return message.replace("'","\\'")

def clearBackslashN(message):
    """ajoute un backslash devant les \n pour eviter les probleme avec SQL"""
    return message.replace("\n","\\n ")

def folderExist (nameDirectory,nameFolder):
    """Retourne si un dossier existe"""
    directory = os.listdir(nameDirectory)

    for folder in directory:
        if folder == f"{nameFolder}":
            return True
    return False

def createFolder(name,directory):
    """Créer un dossier un ajoute le fichier PROUT.mp3 dedans"""
    os.makedirs(f"{directory}/{name}")
    shutil.copy(f"{directory}/PROUT.mp3",f"{directory}/{name}/")

def maxUser(voice_channel):
    """retourne le channel vocal avec le plus de personne connecté parmis tout les channel vocal du serveur"""
    lenMaxChannel = 0
    maxChannel = ()
    for channel in voice_channel:
        if len(channel.members) >= lenMaxChannel:
            maxChannel = channel
            lenMaxChannel = len(channel.members)
    return maxChannel
    
def getAllSong(interaction):
        """Retourne un tableau avec tout les sons(fichier) dans un dossier donné"""
        choice = []
        if folderExist("botSound",f"{interaction.guild.id}"):
                listSound = os.listdir(f"botSound/{interaction.guild.id}")
                if len(listSound) == 0:
                    choice.append("Aucun son disponible")
                    return choice
                for sound in listSound:
                    choice.append(sound[:-4])
        return choice

def isInVoiceChannel(client,guild):
    """Retourne si le client est dans un channel vocal dans le serveur""" 
    voiceClient = client.voice_clients
    if len(voiceClient) == 0:
        return False
    
    for client in voiceClient:
        if client.guild.id == guild.id:
            return True
    return False

async def randomJoin(bot,guild):
    stop = 0
    while stop < 5:
        #genere le temps d'attente entre 25min et 7h
        waitTime = randint(1500,25200)
        await asyncio.sleep(waitTime)

        if checkCanJoinVoc(guild.id):
            channel = maxUser(guild.voice_channels)


            # Vérifie s'il y a au moins 1 personnes dans le canal vocal
            if len(channel.members) >= 1:
                # Génération d'un nombre aléatoire pour la condition "au hasard"
                random_number = random()

                # 50% de chance de rejoindre le canal vocal et de jouer une piste audio
                if random_number <= 0.3:
                    if not isInVoiceChannel(bot,guild):
                        log(bot.user.name,"Play-music-start",f"{channel.guild.name} / {channel.name}")
                        stop = 0
                        voice_channel = channel
                        voice_client = await voice_channel.connect()

                        #faire une liste de tout les fichiers dans le dossier
                        if not folderExist("botSound",guild.id):
                            createFolder(guild.id,"botSound")
                        list = os.listdir(f"botSound/{guild.id}")
                        # Remplacez 'audio_file.mp3' par le chemin de votre fichier audio
                        voice_client.play(discord.FFmpegPCMAudio(f"botSound/{guild.id}/"+list[randint(0,len(list)-1)]))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        await voice_client.disconnect()
                    else:
                        log(bot.user.name,"Can't-join-because-already-here",channel.guild.name)
                else :
                    log(bot.user.name,"Play-music-but-no-chance",f"{guild.name} / {channel.name}")
                    stop = 0
            else :
                log(bot.user.name,"Play-music-but-nobody-in-a-voice-channel",guild.name)
                stop += 1
        else:
            for i in range (len(v.guild_status)):
                if v.guild_status[i] == guild.id:
                    del(v.guild_status[i])
                    return

def deleteLastSpam(channel):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"DELETE FROM LAST_SPAM WHERE ID_CHANNEL = {channel.id};")
            db.commit()

async def saveSpamMessage(message,c,db):
    async for newMessage in message.channel.history(limit=1):
        c.execute(f"INSERT INTO LAST_SPAM (ID_SPAM , ID_CHANNEL, ID_MESSAGE ) VALUES ({message.id} ,{message.channel.id}, {newMessage.id})")
        db.commit()

#------------------------------------------functions for Data-Base-------------------------------------------------
def isServerExist(guild):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"SELECT COUNT(*) FROM SERVER WHERE ID_SERVER = {guild.id}")
            result = c.fetchone()
    
    return (result[0] == 1)

def createServer(guild):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f'''INSERT INTO `SERVER` (`ID_SERVER`, `NAME`, `ICON_URL`,`NB_USER`, `JOIN_DATE`, `CAN_JOIN_VOC`, `STATUS`) 
                      VALUES ({guild.id} ,'{clearQuotes(guild.name)}', '{guild.icon.with_size(128).url}',{guild.member_count}, CURDATE(), FALSE, TRUE)''')
            db.commit()

def updateServer(guild, status = 1):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"UPDATE `SERVER` SET `NAME` = '{clearQuotes(guild.name)}', `ICON_URL` = '{guild.icon.with_size(128).url}', NB_USER = {guild.member_count}, STATUS = {status} WHERE `SERVER`.`ID_SERVER` = {guild.id}")
            db.commit()


def isUserExist(user):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"SELECT COUNT(*) FROM USER WHERE ID_USER = {user.id}")
            result = c.fetchone()
    
    return (result[0] == 1)

def updateUser(user):
    #garde le nom si le nom d'affichage n'existe pas 
    if user.global_name == None:
       globalName = user.name
    else:
       globalName = user.global_name


    #verifie si il a une pp ou pas
    if user.avatar == None :
        avatarUrl = user.default_avatar.with_size(128).url
    else:
        avatarUrl = user.avatar.with_size(128).url

    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"UPDATE `USER` SET `NAME` = '{user.name}', `NAME_GLOBAL` = '{globalName}',`PP_URL` = '{avatarUrl}' WHERE `USER`.`ID_USER` = {user.id}")
            db.commit()

def createUser(user):
    #garde le nom si le nom d'affichage n'existe pas 
    if user.global_name == None:
       globalName = user.name
    else:
       globalName = user.global_name


    #verifie si il a une pp ou pas
    if user.avatar == None :
        avatarUrl = user.default_avatar.with_size(128).url
    else:
        avatarUrl = user.avatar.with_size(128).url

       
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
       
            c.execute(f"INSERT INTO `USER` (`ID_USER`, `NAME`, `NAME_GLOBAL`, `PP_URL`) VALUES ({user.id} ,'{clearQuotes(user.name)}','{clearQuotes(globalName)}', '{avatarUrl}')")
            db.commit()


def isServerProfileExist(user):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"SELECT COUNT(*) FROM USER_SERVER WHERE ID_USER = {user.id} AND ID_SERVER = {user.guild.id}")
            result = c.fetchone()
    
    return (result[0] == 1)
    
def updateServerProfile(user):
    #verifie si il a une pp ou pas
    if user.display_avatar != None:
        avatarUrl = user.display_avatar.with_size(128).url
    else:
        if user.avatar != None:
            avatarUrl = user.avatar.with_size(128).url
        else:
            avatarUrl = user.default_avatar.with_size(128).url


    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"UPDATE `USER_SERVER` SET `NAME_SERVER` = '{clearQuotes(user.display_name)}', `PP_URL_SERVER` = '{avatarUrl}' WHERE `USER_SERVER`.`ID_USER` = {user.id} AND `USER_SERVER`.`ID_SERVER` = {user.guild.id}")
            db.commit()

def createServerProfile(user):
    if user.display_avatar != None:
        avatarUrl = user.display_avatar.with_size(128).url
    else:
        if user.avatar != None:
            avatarUrl = user.avatar.with_size(128).url
        else:
            avatarUrl = user.default_avatar.with_size(128).url

    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:

            c.execute(f"INSERT INTO `USER_SERVER` (`ID_USER`, `ID_SERVER`, `NAME_SERVER`,`PP_URL_SERVER`) VALUES ({user.id} ,{user.guild.id}, '{clearQuotes(user.display_name)}', '{avatarUrl}')")
            db.commit()


def newVocalSession(member):
    #---add the session to the db
    join = getTime()
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
        
            val = (join,member.id,member.guild.id)
            c.execute("INSERT INTO `VOCAL_SESSION` (`ID_VOC`, `JOIN`, `QUIT`, `ID_USER`, `ID_SERVER`, `TIME_VOC`) VALUES (NULL ,%s,NULL, %s, %s, NULL)",val)
            db.commit()
            id=c.lastrowid
    
    #--add the id of the session in a file
    with open('actualSession.json', 'r') as rfile:
        data = json.load(rfile)

    data[member.id] = [id,join]

    with open('actualSession.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)

def closeVocalSession(member):
    with open('actualSession.json', 'r') as rfile:
        data = json.load(rfile)

    #-check if the id exist else return bcs join wasn't save 
    if not f"{member.id}" in data:
        return 


    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            time = getTime()
            c.execute(f"UPDATE `VOCAL_SESSION` SET `QUIT` = {time}, `TIME_VOC` = {time-data[f'{member.id}'][1]} WHERE `VOCAL_SESSION`.`ID_VOC` = {data[f'{member.id}'][0]}")
            db.commit()


    del data[f'{member.id}']
    with open('actualSession.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)


def newMessage(message):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
                
            c.execute(f"INSERT INTO `MESSAGE` (ID_MESSAGE, LENGTH, NB_ATTACHMEMTS, DATE, ID_USER, ID_SERVER) VALUES ({message.id} , {len(message.content)}, {len(message.attachments)},STR_TO_DATE('{getTimeV2()}','%d-%m-%y %H:%i:%S'), {message.author.id}, {message.guild.id})")
            db.commit()

def newSpam(message,nbrep,content):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:

            c.execute(f"INSERT INTO `SPAM` (`ID_SPAM`, `NB_REP`, `CONTENT`, `DATE`, `ID_USER`, `ID_SERVER`) VALUES ({message.id} , {nbrep}, '{clearQuotes(content)}', STR_TO_DATE('{getTimeV2()}','%d-%m-%y %H:%i:%S'), {message.author.id}, {message.guild.id})")
            db.commit()

#---------------------------------SLASH COMMANDS------------------------------------
            
def checkCanJoinVoc(guildId):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"SELECT CAN_JOIN_VOC FROM SERVER WHERE ID_SERVER = {guildId}")
            result = c.fetchone()
    
    return result[0]

def editCanJoinVoc(guildId,statut):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"UPDATE SERVER SET CAN_JOIN_VOC = {statut} WHERE ID_SERVER = {guildId}")
            db.commit()

#--playSong-------

def audioDuration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
    
    result = ""

    if hours != 0:
        result += f'{hours}:'
    
    if mins < 10:
        if mins == 0:
            result += "00:"
        else:
            result += f'0{mins}:'
    else:
        result += f"{mins}:"

    if seconds < 10:
        if seconds == 0:
            result += "00"
        else:
            result += f'0{seconds}'
    else:
        result += f'{seconds}'

    return result  # returns the duration

def getAudioDuration(audio):
    audio = MP3(audio)
    return int(audio.info.length)

async def playSong(interaction):
    vc = v.voiceClient[interaction.guild.id][0]
    while len(v.musicQueue[interaction.guild.id]):   #boucle tant que la liste n'est pas vide
        if not vc.is_connected():
            del v.musicQueue[interaction.guild.id]
            return
        if not len(interaction.user.voice.channel.members) > 1:   #se deconnecte si le bot est tout seul en voc
            del v.musicQueue[interaction.guild.id]
            return
        
        volume = v.musicQueue[interaction.guild.id][0]['volume'] / 100

        if v.musicQueue[interaction.guild.id][0]['source'].startswith("https://"):    #Lance le son si il s'agit d'une video youtube

            data = ytdl.extract_info(v.musicQueue[interaction.guild.id][0]['source'], download=False)
            song = data['url']
            log(interaction.user.name,f"Play-{v.musicQueue[interaction.guild.id][0]['title']}",f"{interaction.guild.name} / {vc.channel.name}")
            vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),0.15*volume))
        else:
            if not v.musicQueue[interaction.guild.id][0]['source'].endswith(".mp3"):   #Lance le son si il s'agit d'un son du serveur
                    v.musicQueue[interaction.guild.id][0]['source'] += ".mp3"
            log(interaction.user.name,f"Play-{v.musicQueue[interaction.guild.id][0]['title']}",f"{interaction.guild.name} / {vc.channel.name}")
            vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(v.musicQueue[interaction.guild.id][0]['source']),0.65*volume))

        v.voiceClient[interaction.guild.id][1] = getTime()
        while vc.is_playing() and vc.is_connected():
            await asyncio.sleep(1)
        v.musicQueue[interaction.guild.id].pop(0) #enleve le son de la liste a la fin du son
    vc.cleanup()
    await vc.disconnect()
    del v.voiceClient[interaction.guild.id]
    del v.musicQueue[interaction.guild.id]

def getSong(son,interaction,volume):
    #pour un url recuperer la video
    if son.startswith("https://"):
        data = ytdl.extract_info(son, download=False)
        song = {'source':son, 'title':data['title'], 'volume':volume, 'duration': data['duration']}

    #si c'est pas un url verifie si le son existe dans les fichier du bot
    elif os.path.exists(f"botSound/{interaction.guild.id}/{son}.mp3"):
        song = {'source':f"botSound/{interaction.guild.id}/{son}.mp3", 'title':son, 'volume':volume, 'duration': getAudioDuration(f"botSound/{interaction.guild.id}/{son}.mp3")}
    
    #si c'est pas dans les fichier du bot alors faire un recherche youtube
    else:
        search = VideosSearch(son, limit=1)
        song = {'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"], 'volume':volume, 'duration':ytdl.extract_info(search.result()["result"][0]["link"], download=False)['duration']}

    return song

