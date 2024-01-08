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

@client.event
async def on_ready():

    print(f'Connecté en tant que {client.user.name}')

    try: 
        synced = await tree.sync(guild=discord.Object(id=1186997974333652992))
        print(f"{len(synced)} commandes syncroniser")
        
    except Exception as e:
        print(e)

    #----------attend un temps random et rejoint un voc pour mettre airmax si il y a au moins 1 pers en voc
    while True:
        #genere le temps d'attente entre 25min et 7h
        waitTime = randint(1500,25200)
        await asyncio.sleep(30)

        # Vérifie s'il y a au moins 2 personnes dans le canal vocal
        channel = client.get_channel(1186997975843618829)
        if len(channel.members) >= 1:
            # Génération d'un nombre aléatoire pour la condition "au hasard"
            random_number = random()

            # 50% de chance de rejoindre le canal vocal et de jouer une piste audio
            if random_number <= 1.3:
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

#-------------------- sur un changement de pp----------------------------------------------
@client.event
async def on_user_update(before, after):

    if before.name != after.name:
        # le nom de l'utilisateur a changer
        print(f"Changement de nom détecté pour {before.name} / {after.name}")
        updateUser(before.id,None,None,after.name,7)


    if before.avatar.url != after.avatar.url:
        # L'avatar de l'utilisateur a changé
        print(f"Changement d'avatar détecté pour {after.name}")
        user_avatar_url = after.avatar.url
        updateUser(before.id,None,None,user_avatar_url,6)

#----------------------action quand quelle qu'un rejoint ou quitte un voc ------------------------

@client.event
async def on_voice_state_update(member, before, after):
    # Vérifie si le membre a rejoint un canal vocal
    if before.channel is None and after.channel is not None and member != client.user:
        channel_name = after.channel.name

        if isInJson(member.id):
            updateUser(member.id,member.guild.id,member.guild.name,getTime(),1)
        else:
            user_avatar_url = member.avatar.url
            createUser(member.id,member.name,user_avatar_url)
            updateUser(member.id,member.guild.id,member.guild.name,getTime(),1)

        log(getTimeV2(),member.name,"Join-Voice-Channel",f"{member.guild.name} / {channel_name}")

    #verifie si le membre a quitte le canal
    elif before.channel is not None and after.channel is None and member != client.user:
        channel_name = before.channel.name

        if not isInJson(member.id):
            user_avatar_url = member.avatar.url
            createUser(member.id,member.name,user_avatar_url)

        updateUser(member.id,member.guild.id,member.guild.name,getTime(),2)

        newTime = calculTime(member.id,member.guild.id)
        updateUser(member.id,member.guild.id,member.guild.name,newTime,3)

        log(getTimeV2(),member.name,"Left-Voice-Channel",f"{member.guild.name} / {channel_name}")



#---------------------action a l'envoie d'un message---------------------------------------------

#Liste des différentes possibilités de message ainsi que leurs réponses
possibilites = {"quoi": ["feur", "chi", "driceps","quoicoubeh"],
                 "oui": ["stiti", "ghours"],
                 "mere": ["méditérannée", "rie"],
                 "mère": ["méditérannée", "rie"],
                 "qoi": ["feur", "chi", "driceps","quoicoubeh"],
                 "quois": ["feur", "chi", "driceps","quoicoubeh"],
                 "koi": ["feur", "chi", "driceps","quoicoubeh"],
                 "kois": ["feur", "chi", "driceps","quoicoubeh"],
                 "qoa": ["feur", "chi", "driceps","quoicoubeh"],
                 "kwoi": ["feur", "chi", "driceps","quoicoubeh"],
                 "kwa": ["feur", "chi", "driceps","quoicoubeh"]}

#definie le statue d'un channel
channel_status = {}



@client.event
async def on_message(message):
    #On vérifie que ce n'est pas nous même (le bot) qui envoie le message
    if message.author == client.user:
        return
    


    #rajoute 1 au nombre de message de la personne
    if not isInJson(message.author.id):
        user_avatar_url = message.author.avatar.url
        createUser(message.author.id,message.author.name,user_avatar_url)
    updateUser(message.author.id,message.guild.id,message.guild.name,1,5)

    # Prise en charge des majuscules et mininuscules
    #si le message commence par spam 
    if message.content.lower().startswith('spam'):

        channel_id = message.channel.id

        # Vérifie si le canal est déjà occupé
        if channel_id in channel_status and channel_status[channel_id]:
            await message.channel.send("Un spam est déjà en cours, veuillez patienter.")
            return

        #decoupe le message a chaque 
        cutedContent=cutMessage(message.content)

        nbRep = cutedContent[1]
        messSpam = cutedContent[2]

        # Marque le canal comme occupé
        channel_status[channel_id] = True

        #si plus de 2000 rep pas faire 
        if (nbRep >2000):
            log(getTimeV2(),message.author,f"Send-4-'{messSpam}'",f"{message.guild.name} / {message.channel.name}")

            await message.channel.send("frero abuse, dose un peu")

            for i in range(4):
                await message.channel.send(messSpam)
            await message.channel.send("4 fois c'est deja pas mal")

            
            #stock le nombre de message envoyer
            if not isInJson(message.author.id):
                user_avatar_url = message.author.avatar.url
                createUser(message.author.id,message.author.name,user_avatar_url)
            updateUser(message.author.id,message.guild.id,message.guild.name,nbRep,4)
            return
        
        log(getTimeV2(),message.author,f"Send-{nbRep}-'{messSpam}'",f"{message.guild.name} / {message.channel.name}")

        if not isInJson(message.author.id):
                user_avatar_url = message.author.avatar.url
                createUser(message.author.id,message.author.name,user_avatar_url)
        updateUser(message.author.id,message.guild.id,message.guild.name,nbRep,4)

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

        channel_status[channel_id] = False
        return

    # Si le contenu du message dont on a enlevé la ponctuation et les espaces termine par un des mots listés dans le dictionnaire possibilites, alors répondre au hasard une des réponses présente dans la liste correspondante
    for i in possibilites:
        if retirer_points(message.content).endswith(i): 
            await message.channel.send(possibilites[i][randint(0, len(possibilites[i]) - 1)])


client.run(readToken("token_discord.txt"))