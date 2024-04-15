from datetime import datetime
import pytz
import csv
import os
import shutil
from mutagen.mp3 import MP3


def removePunctuation(message:str):
    """Enlever la ponctuation d'un message"""

    caracteres = "!? ."
    message = message.lower()
    for x in range(len(caracteres)):
        message = message.replace(caracteres[x],"")
    return message

def readToken(emplacement = "TOKEN.txt"):
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
