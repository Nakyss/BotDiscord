import re
import json
from datetime import datetime
import pytz
import csv
import mysql.connector
import os
import shutil
import discord
from variable import mydb


async def admin (message):
    if message.content.lower() == "log":
        await message.channel.send(content="Voila le fichier logs",file=discord.File("logs.csv"))

    elif message.content.lower() == "server":
        with mysql.connector.connect(**mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT NAME, NB_USER, DATE_FORMAT(JOIN_DATE, '%e/%M/%Y'), CAN_JOIN_VOC, STATUS FROM SERVER")
                result = c.fetchall()
        sendableMesseage = '```'
        for serv in result:
            sendableMesseage += f'\n{serv[0]} -  {serv[1]} Utilisateurs  -  Depuis le {serv[2]}  -  Peut rejoindre le voc :{serv[3]}  -  Status : {serv[3]}'
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)

    elif message.content.lower() == "message":
        with mysql.connector.connect(**mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT U.NAME_GLOBAL, M.LENGTH, M.NB_ATTACHMEMTS, DATE_FORMAT(DATE, '%H:%i %e/%m/%Y') FROM MESSAGE M JOIN USER U ON U.ID_USER = M.ID_USER ORDER BY M.DATE DESC LIMIT 10")
                result = c.fetchall()
        sendableMesseage = '```'
        for mess in result:
            sendableMesseage += f'\n{mess[0]} - {mess[1]} Caractères - {mess[2]} Fichier - {mess[3]} '
        sendableMesseage += '\n```'
        await message.channel.send(sendableMesseage)


def retirer_points(message):
    caracteres = "!? ."
    message = message.lower()
    for x in range(len(caracteres)):
        message = message.replace(caracteres[x],"")
    return message

def procedNb(nbRep):
    chiffre = re.sub(r'\D', '',nbRep)

    if (chiffre == ''):
        chiffre = '10'

    chiffre = int(chiffre)
    return chiffre

def cutMessage(message):
    #ajoute 2 espace apres les message dans le cas ou il n'y a pas d'espace pour que le split marche
    message += '  '

    #coupe le message en 3 a chaque esapce 
    splited = message.split(' ',2)


    #si le Message est vide
    if (splited[2] == '' or splited[2].startswith(' ')):
        splited[2] = "OUAIS OUAIS OUAIS"
    else:
        splited[2] = splited[2].strip()

    splited[1] = procedNb(splited[1])

    return splited

def calculNbMess(message,nbRep):

    tab=[5,0,0]

    nbByMess = nbRep//5
    lastMess = nbRep%5

    nbChar = (len(message)+1)*nbByMess

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
    fichier = open(emplacement, 'r')
    return(fichier.readline())

def getTime():
    # Getting the current date and time
    dt = datetime.now()

    # getting the timestamp
    ts = datetime.timestamp(dt)

    return int(ts)

def getTimeV2():
    # Obtenez le fuseau horaire de Paris
    paris_tz = pytz.timezone('Europe/Paris')

    # Obtenez la date et l'heure actuelles en UTC
    utc_now = datetime.utcnow()

    # Convertissez la date et l'heure en UTC en utilisant le fuseau horaire de Paris
    paris_now = utc_now.replace(tzinfo=pytz.utc).astimezone(paris_tz)

    # Formatez la date et l'heure au format souhaité
    return paris_now.strftime("%d-%m-%y %H:%M:%S")

def log(user,action,place):
    time = getTimeV2()
    print(f"{time} - {user} - {action} in {place}")
    
    with open('logs.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([time,user,action,place])

def clearQuotes(message):
    return message.replace("'","\\'")

def clearBackslashN(message):
    return message.replace("\n","\\n ")

def folderExist (nameDirectory,nameFolder):
    directory = os.listdir(nameDirectory)

    for folder in directory:
        if folder == f"{nameFolder}":
            return True
    return False

def createFolder(name,directory):
    os.makedirs(f"{directory}/{name}")
    shutil.copy(f"{directory}/PROUT.mp3",f"{directory}/{name}/")

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

def canJoinVocalServer(guild,bool):
    with mysql.connector.connect(**mydb) as db :
        with db.cursor() as c:
            c.execute(f"UPDATE `SERVER` SET  CAN_JOIN_VOC = {bool} WHERE `SERVER`.`ID_SERVER` = {guild.id}")
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