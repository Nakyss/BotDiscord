from datetime import datetime
import pytz
import csv
import os
import shutil
from mutagen.mp3 import MP3
import json
import variable as v
from random import randint,random
import requests

#return true or false pourcentage is the chance that is true
def luck(percentage:int):
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100

    return (random() <= (percentage/100))

def openJson():
    with open('actualSession.json', 'r') as rfile:
        data = json.load(rfile)
    return data

def saveJson(data):
    with open('actualSession.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)

def removePunctuation(message:str):
    """Enlever la ponctuation d'un message"""

    caracteres = "!? ."
    message = message.lower()
    for x in range(len(caracteres)):
        message = message.replace(caracteres[x],"")
    return message


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

def setMute(user_id):
    data = openJson()

    if f"{user_id}" in data:
        if len(data[f"{user_id}"]) == 2:
            data[f"{user_id}"].append(getTime())
            data[f"{user_id}"].append(None)
        else:
            data[f"{user_id}"][2] = getTime()
            data[f"{user_id}"][3] = None

        saveJson(data)

def setUnMute(user_id):
    data = openJson()

    if f"{user_id}" in data:
       if len(data[f"{user_id}"]) == 4:
        data[f"{user_id}"][3] = getTime()

        saveJson(data)

def format_total_time(total_time):
    days = total_time // (3600 * 24)
    hours = (total_time % (3600 * 24)) // 3600
    minutes = (total_time % 3600) // 60
    seconds = total_time % 60

    result = ''
    if days > 0:
        result += str(days) + 'j '
    if hours > 0:
        result += str(hours) + 'h '
    if minutes > 0:
        result += str(minutes) + 'm '
    if seconds > 0:
        result += str(seconds) + 's'

    return result.strip()

def activityName():
    return v.someActivity[randint(0, len(v.someActivity)-1)]

def saveImgFromLink(link):
    img_data = requests.get(link).content
    with open('pp/new_pp.jpg', 'wb') as handler:
        handler.write(img_data)

def getARandomPP() -> str:
    profil_pics = v.db.select("SELECT PP_URL FROM USER")
    deleteFile("pp/new_pp.jpg")
    saveImgFromLink(profil_pics[randint(0,len(profil_pics)-1)][0])
    return "pp/new_pp.jpg"

def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)