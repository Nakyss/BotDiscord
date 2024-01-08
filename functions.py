import re
import json
from datetime import datetime
import pytz
import csv



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

def isInJson(id):
    with open('userTime.json', 'r') as file:
        data = json.load(file)

    return any(user['id'] == id for user in data['users'])

def createUser(id,name,url):
    with open('userTime.json', 'r') as rfile:
        data = json.load(rfile)

    nouvel_utilisateur = {
        "id": id,
        "name": name,
        "urlPP": url,
        "lastJoinAll": [],
        "lastQuitAll": [],
        "totalTimeAll": [],
        "nbSpamAll": [],
        "nbMessage": [],
        "server" : []
    }
    data['users'].append(nouvel_utilisateur)

    with open('userTime.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)

def updateUser(id,idServ,nameServ,edit,action):
    with open('userTime.json', 'r') as file:
        data = json.load(file)

    for user in data['users']:
        if user['id'] == id:
            match action:
                case 1: #mettre a jour la date de connexion
                    inlist = False
                    inJson = False
                    #regarde tout les lastjoin pour l'user 
                    for lastJoinbyServ in user['lastJoinAll']:
                        #si y'a un last join dans se serveur le mettre a jour
                        if lastJoinbyServ['idServ'] == idServ:
                            lastJoinbyServ['lastJoin'] = edit
                            inJson = True
                        
                    if not inJson:
                        for server in user['server']:
                            if server['idServ'] == idServ:
                                inlist = True
                        if not inlist:
                            new_serv = {
                                "idServ": idServ,
                                "nameServ": nameServ
                            }
                            user['server'].append(new_serv)
                        new_serv = {
                            "idServ": idServ,
                            "lastJoin": edit
                        }
                        user['lastJoinAll'].append(new_serv)

                case 2: #mettre a jour la date de deconnexion
                    inlist = False
                    inJson = False
                    #regarde tout les lastQuit pour l'user 
                    for lastQuitbyServ in user['lastQuitAll']:
                        #si y'a un last Quit dans se serveur le mettre a jour
                        if lastQuitbyServ['idServ'] == idServ:
                            lastQuitbyServ['lastQuit'] = edit
                            inJson = True
                        
                    if not inJson:
                        for server in user['server']:
                            if server['idServ'] == idServ:
                                inlist = True
                        if not inlist:
                            new_serv = {
                                "idServ": idServ,
                                "nameServ": nameServ
                            }
                            user['server'].append(new_serv)
                        new_serv = {
                            "idServ": idServ,
                            "lastQuit": edit
                        }
                        user['lastQuitAll'].append(new_serv)

                case 3: #ajouter du temps au temps en voc
                    inlist = False
                    inJson = False
                    #regarde tout les lastQuit pour l'user 
                    for totalTimeByServ in user['totalTimeAll']:
                        #si y'a un last Quit dans se serveur le mettre a jour
                        if totalTimeByServ['idServ'] == idServ:
                            totalTimeByServ['totalTime'] += edit
                            inJson = True
                        
                    if not inJson:
                        for server in user['server']:
                            if server['idServ'] == idServ:
                                inlist = True
                        if not inlist:
                            new_serv = {
                                "idServ": idServ,
                                "nameServ": nameServ
                            }
                            user['server'].append(new_serv)
                        new_serv = {
                            "idServ": idServ,
                            "totalTime": edit
                        }
                        user['totalTimeAll'].append(new_serv)

                case 4: #ajouter le nombre de message spam
                    inlist = False
                    inJson = False
                    #regarde tout les lastQuit pour l'user 
                    for nbSpamByServ in user['nbSpamAll']:
                        #si y'a un last Quit dans se serveur le mettre a jour
                        if nbSpamByServ['idServ'] == idServ:
                            nbSpamByServ['nbSpam'] += edit
                            inJson = True
                        
                    if not inJson:
                        for server in user['server']:
                            if server['idServ'] == idServ:
                                inlist = True
                        if not inlist:
                            new_serv = {
                                "idServ": idServ,
                                "nameServ": nameServ
                            }
                            user['server'].append(new_serv)

                        new_serv = {
                            "idServ": idServ,
                            "nbSpam": edit
                        }
                        user['nbSpamAll'].append(new_serv)

                case 5: #ajouter nb message envoyer
                    inlist = False
                    inJson = False
                    for nbMess in user['nbMessage']:
                        if nbMess['idServ'] == idServ:
                            nbMess['nbMessage'] += edit
                            inJson = True
                    
                        
                    if not inJson:
                        for server in user['server']:
                            if server['idServ'] == idServ:
                                inlist = True
                        if not inlist:
                            new_serv = {
                                "idServ": idServ,
                                "nameServ": nameServ
                            }
                            user['server'].append(new_serv)

                        new_serv = {
                            "idServ": idServ,
                            "nbMessage": edit
                        }
                        user['nbMessage'].append(new_serv)
                
                case 6 : #changer photo de profile
                    user["urlPP"] = edit

                case 7 : #changer le nom
                    user["name"] = edit
                
            break

    with open('userTime.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)

def calculTime(id,idServ):
    with open('userTime.json', 'r') as file:
        data = json.load(file)
 
    for user in data['users']:
        if user['id'] == id:
            lastJoin = None
            for lastJoinbyServ in user['lastJoinAll']:
                if lastJoinbyServ['idServ'] == idServ:
                    lastJoin = lastJoinbyServ['lastJoin']

            if lastJoin != None:
                for lastQuitbyServ in user['lastQuitAll']:
                    if lastQuitbyServ['idServ'] == idServ:
                        return lastQuitbyServ['lastQuit'] - lastJoin
            return 0
        
def log(time,user,action,place):
    print(f"{time} - {user} - {action} in {place}")
    
    with open('logs.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([time, user,action,place])

def NewChamp(nouveau_champ,valeur_par_defaut):
    with open('userTime.json', 'r') as rfile:
        data = json.load(rfile)


    for utilisateur in data['users']:
        utilisateur[nouveau_champ] = valeur_par_defaut

    with open('userTime.json', 'w') as wfile:
        json.dump(data, wfile, indent=2)
