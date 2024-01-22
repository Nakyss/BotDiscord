import discord
from os import listdir
import asyncio
from discord import app_commands
from functions import *
from random import randint, random
from discord.ext import commands




intents = discord.Intents.all()


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

mydb = {
  'host' : "host",
  'user': "user",
  'password':"password",
  'port':3306,
  'database':"db"
}

#Liste des différentes possibilités de message ainsi que leurs réponses
possibilites = {
    "quoi": ["feur", "chi", "driceps","quoicoubeh"],
    "oui": ["stiti", "ghours"],
    "mere": ["méditérannée", "rie"],
    "mère": ["méditérannée", "rie"],
    "qoi": ["feur", "chi", "driceps","quoicoubeh"],
    "quois": ["feur", "chi", "driceps","quoicoubeh"],
    "koi": ["feur", "chi", "driceps","quoicoubeh"],
    "kois": ["feur", "chi", "driceps","quoicoubeh"],
    "qoa": ["feur", "chi", "driceps","quoicoubeh"],
    "kwoi": ["feur", "chi", "driceps","quoicoubeh"],
    "kwa": ["feur", "chi", "driceps","quoicoubeh"]
}

@client.event
async def on_ready():

    print(f'Connecté en tant que {client.user.name}')

    #----------attend un temps random et rejoint un voc pour mettre airmax si il y a au moins 1 pers en voc
    while True:
        #genere le temps d'attente entre 25min et 7h
        waitTime = randint(1500,25200)
        await asyncio.sleep(waitTime)

        with mysql.connector.connect(**mydb) as db :
            with db.cursor() as c:
                c.execute(f"SELECT ID_SERVER FROM SERVER WHERE CAN_JOIN_VOC = 1")
                result = c.fetchall()

        for server in result:
            guild = client.get_guild(server[0])
            channel = guild.voice_channels[0]

            # Vérifie s'il y a au moins 1 personnes dans le canal vocal
            if len(channel.members) >= 1:
                # Génération d'un nombre aléatoire pour la condition "au hasard"
                random_number = random()

                # 50% de chance de rejoindre le canal vocal et de jouer une piste audio
                if random_number <= 0.3:
                    log(getTimeV2(),client.user.name,"Play-music-start",f"{channel.guild.name} / {channel.name}")
                    voice_channel = channel
                    voice_client = await voice_channel.connect()

                    #faire une liste de tout les fichiers dans le dossier
                    list = listdir("botSound")
                    # Remplacez 'audio_file.mp3' par le chemin de votre fichier audio
                    voice_client.play(discord.FFmpegPCMAudio("botSound/"+list[randint(0,len(list)-1)]))

                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                    await voice_client.disconnect()
                else :
                    log(getTimeV2(),client.user.name,"Play-music-but-no-chance",f"{channel.guild.name} / {channel.name}")
            else :
                log(getTimeV2(),client.user.name,"Play-music-but-nobody-in-channel",f"{channel.guild.name} / {channel.name}")

    
#-----------------------slash commande---------------------------------------------------------

#@client.command(guild=discord.Object(id=1186997974333652992))
#async def clear (ctx, nombre : int ):
#    print ("cool")
#---------------------------------------------------------------------------------------------


#-------------------------------------------------------------------
#---                     SERVER MANAGEMENT                       ---
#-------------------------------------------------------------------
            
#------------------------quand le bot est ajouter a un server---------------------------
@client.event
async def on_guild_join(guild):
    if not isServerExist(mydb,guild):
        createServer(mydb,guild)
    else:
        updateServer(mydb,guild)

@client.event
async def on_guild_remove(guild):
    updateServer(mydb,guild,"FALSE")

#-----------------------changement dans sur le serveur----------------------------------
@client.event
async def on_guild_update(before, after):
    if isServerExist(mydb,after):
        updateServer(mydb,after)
    else:
        createServer(mydb,after)

#----------------------changement de nb User--------------------------------------------
@client.event
async def on_member_join(member):
    if isServerExist(mydb,member.guild):
        updateServer(mydb,member.guild)
    else:
        createServer(mydb,member.guild)
    

@client.event
async def on_member_remove(member):
    if isServerExist(mydb,member.guild):
        updateServer(mydb,member.guild)
    else:
        createServer(mydb,member.guild)

#-------------------------------------------------------------------
#---                         USER UPDATE                         ---
#-------------------------------------------------------------------

#--------------Mise a jour des User sur des changement--------------

#- Mise a jour du profil de serveur
@client.event
async def on_member_update(before, after):

    if isServerProfileExist(mydb,after):
            updateServerProfile(mydb,after)

    if before.display_name != after.display_name: #changement de nom de server
        log(getTimeV2(),after.name,f"Change-Display_name-from-'{before.display_name}'-to-'{after.display_name}'",after.guild.name)

    if before.display_avatar.url != after.display_avatar.url:  #changement d'avatar de serveur
        log(getTimeV2(),after.name,f"Change-Server-Profil-Picture",after.guild.name)
    

# - Mise a jour du profil
@client.event
async def on_user_update(before, after):

    if isUserExist(mydb,after):
        updateUser(mydb,after)

    if before.name != after.name:    #changement de nom
        log(getTimeV2(),after.name,f"Change-name-from-'{before.name}'-to-'{after.name}'","Nowhere")

    if before.global_name != after.global_name: #changement de nom d'affichage
        log(getTimeV2(),after.name,f"Change-Global_name-from-'{before.global_name}'-to-'{after.global_name}'","Nowhere")

    if before.avatar.url != after.avatar.url:   #changement d'avatar
        log(getTimeV2(),after.name,f"Change-Profil-Picture","Nowhere")


#----------------------action quand quelle qu'un rejoint ou quitte un voc ------------------------

@client.event
async def on_voice_state_update(member, before, after):
    # Vérifie si le membre a rejoint un canal vocal
    if before.channel is None and after.channel is not None and member != client.user:

        if not isServerExist(mydb,member.guild):
            createServer(mydb,member.guild)
        if not isUserExist(mydb,member):
            createUser(mydb,member)
        if not isServerProfileExist(mydb,member):
            createServerProfile(mydb,member)

        log(getTimeV2(),member.name,"Join-Voice-Channel",f"{member.guild.name} / {after.channel.name}")

        newVocalSession(mydb,member)


    #verifie si le membre a quitte le canal
    elif before.channel is not None and after.channel is None and member != client.user:
        closeVocalSession(mydb,member)

        log(getTimeV2(),member.name,"Left-Voice-Channel",f"{member.guild.name} / {before.channel.name}")



#---------------------action a l'envoie d'un message---------------------------------------------


#definie le statue d'un channel
channel_status = {}


@client.event
async def on_message(message):
    #On vérifie que ce n'est pas nous même (le bot) qui envoie le message
    if message.author == client.user:
        return
    

    #Si c'est un message de bienvenue 
    if message.type == discord.MessageType.new_member:
        return
    
    #si l'utilisateur n'existe pas dans la db ou qu'il n'a pas de profil de server
    if not isServerExist(mydb,message.guild):
            createServer(mydb,message.guild)
    if not isUserExist(mydb,message.author):
        createUser(mydb,message.author)
    if not isServerProfileExist(mydb,message.author):
        createServerProfile(mydb,message.author)


    # Prise en charge des majuscules et mininuscules
    #si le message commence par spam 
    if message.content.lower().startswith('spam'):


        # Vérifie si le canal est déjà occupé
        if message.channel.id in channel_status and channel_status[message.channel.id]:
            await message.channel.send("Un spam est déjà en cours, veuillez patienter.")
            return

        #decoupe le message a chaque espace
        cutedContent=cutMessage(message.content)

        nbRep = cutedContent[1]
        messSpam = cutedContent[2]

        # Marque le canal comme occupé
        channel_status[message.channel.id] = True

        #si plus de 2000 rep pas faire 
        if (nbRep >2000):
            log(getTimeV2(),message.author,f"Send-4-'{clearBackslashN(messSpam)}'",f"{message.guild.name} / {message.channel.name}")

            await message.channel.send("frero abuse, dose un peu")

            for i in range(4):
                await message.channel.send(messSpam)
            await message.channel.send("4 fois c'est deja pas mal")

            newSpam(mydb,message,4,messSpam)  #add to db
            
            channel_status[message.channel.id] = False
            return
        
        log(getTimeV2(),message.author,f"Send-{nbRep}-'{clearBackslashN(messSpam)}'",f"{message.guild.name} / {message.channel.name}")
        
        newSpam(mydb,message,nbRep,messSpam) #add to db

        # si plus de 6 rep repartir les rep dans plusieur messages
        if (nbRep > 6 ):
            tab = calculNbMess(messSpam,nbRep)
            
            for i in range (tab[0]):
                await message.channel.send((messSpam+"\n")*tab[1])
            if (tab[2] != 0):
                await message.channel.send((cutedContent[2]+"\n")*tab[2])
            
        elif(nbRep > 0):
        #envoie nbRep fois le messages
            for i in range (nbRep):
                await message.channel.send(messSpam)

        else:
            await message.channel.send("Pourquoi faire ?")

        channel_status[message.channel.id] = False
        return
    else:
        #ajoute un message si c'est pas un spam
        newMessage(mydb,message)

    

    # Si le contenu du message dont on a enlevé la ponctuation et les espaces termine par un des mots listés dans le dictionnaire possibilites, alors répondre au hasard une des réponses présente dans la liste correspondante
    for i in possibilites:
        if retirer_points(message.content).endswith(i): 
            await message.channel.send(possibilites[i][randint(0, len(possibilites[i]) - 1)])


client.run(readToken("token_discord.txt"))

