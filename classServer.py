import discord
import os
from functions import folderExist,maxUser,log,createFolder,getTime,getAudioDuration
from random import random,randint
import asyncio
import variable
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

class Server:
    isChannelSpamming:bool = False
    isRandomJoinDisable:bool = False
    lastActualisation:int
    isRandomJoinActive:bool = False
    musicQueue = []
    voiceClient = None
    beginningTime = 0
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
    ytdl = YoutubeDL(YDL_OPTIONS)


    def __init__(self,id):
        self.id = id
        
        
    def getAllSong(self):
        """Retourne un tableau avec tout les sons(fichier) dans un dossier donné"""
        choice = []
        if folderExist("botSound",f"{self.id}"):
                listSound = os.listdir(f"botSound/{self.id}")
                if len(listSound) == 0:
                    choice.append("Aucun son disponible")
                    return choice
                for sound in listSound:
                    choice.append(sound[:-4])
        return choice

    def isInVoiceChannel(self,client):
        """Retourne si le client est dans un channel vocal dans le serveur""" 
        voiceClient = client.voice_clients
        if len(voiceClient) == 0:
            return False
        
        for client in voiceClient:
            if client.guild.id == self.id:
                return True
        return False

    async def randomJoin(self,bot,guild):
        stop = 0
        self.isRandomJoinActive = True
        while stop < 5:
            #genere le temps d'attente entre 25min et 7h
            waitTime = randint(1500,25200)
            await asyncio.sleep(waitTime)

            if variable.db.checkCanJoinVoc(self.id):
                channel = maxUser(guild.voice_channels)


                # Vérifie s'il y a au moins 1 personnes dans le canal vocal
                if len(channel.members) >= 1:
                    # Génération d'un nombre aléatoire pour la condition "au hasard"
                    random_number = random()

                    # 50% de chance de rejoindre le canal vocal et de jouer une piste audio
                    if random_number <= 0.3:
                        if not self.isInVoiceChannel(bot):
                            log(bot.user.name,"Play-music-start",f"{channel.guild.name} / {channel.name}")
                            stop = 0
                            voice_channel = channel
                            voice_client = await voice_channel.connect()
                            self.voiceClient = voice_client
                            self.musicQueue = [{'source':"tkt", 'title':"Son au Hasard", 'volume':100, 'duration': -1}] 

                            #faire une liste de tout les fichiers dans le dossier
                            if not folderExist("botSound",guild.id):
                                createFolder(guild.id,"botSound")
                            list = os.listdir(f"botSound/{guild.id}")
                            # Remplacez 'audio_file.mp3' par le chemin de votre fichier audio
                            voice_client.play(discord.FFmpegPCMAudio(f"botSound/{guild.id}/"+list[randint(0,len(list)-1)]))

                            while voice_client.is_playing():
                                await asyncio.sleep(1)

                            await voice_client.disconnect()
                            self.voiceClient = None
                            self.musicQueue = []
                        else:
                            log(bot.user.name,"Can't-join-because-already-here",channel.guild.name)
                            stop = 0
                    else :
                        log(bot.user.name,"Play-music-but-no-chance",f"{guild.name} / {channel.name}")
                        stop = 0
                else :
                    log(bot.user.name,"Play-music-but-nobody-in-a-voice-channel",guild.name)
                    stop += 1
            else:
                self.isRandomJoinActive = False
                return
        #si on a eu 5 essai sans persone alors arreter et supprimé ce serveur de la liste en cours  
        self.isRandomJoinActive = False
        return

    async def playSong(self,interaction):
        while len(self.musicQueue):   #boucle tant que la liste n'est pas vide
            if not self.voiceClient.is_connected():
                self.musicQueue = []
                return
            
            volume = self.musicQueue[0]['volume'] / 100

            if self.musicQueue[0]['source'].startswith("https://"):    #Lance le son si il s'agit d'une video youtube

                log(interaction.user.name,f"Play-{self.musicQueue[0]['title']}",f"{interaction.guild.name} / {self.voiceClient.channel.name}")
                self.voiceClient.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.musicQueue[0]['source'], before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),0.11*volume))
            else:
                if not self.musicQueue[0]['source'].endswith(".mp3"):   #Lance le son si il s'agit d'un son du serveur
                        self.musicQueue[0]['source'] += ".mp3"
                log(interaction.user.name,f"Play-{self.musicQueue[0]['title']}",f"{interaction.guild.name} / {self.voiceClient.channel.name}")
                self.voiceClient.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.musicQueue[0]['source']),0.65*volume))

            self.beginningTime = getTime()
            while self.voiceClient.is_playing() and self.voiceClient.is_connected():
                await asyncio.sleep(1)
            self.musicQueue.pop(0) #enleve le son de la liste a la fin du son

            if not len(self.voiceClient.channel.members) > 1:   #se deconnecte si le bot est tout seul en voc
                self.musicQueue = []

        self.voiceClient.cleanup()
        await self.voiceClient.disconnect()
        self.voiceClient = None 
        self.musicQueue = []

    def getSong(self, son, volume):
        #pour un url recuperer la video
        if son.startswith("https://"):
            data = self.ytdl.extract_info(son, download=False)
            song = {'source':data['url'], 'title':data['title'], 'volume':volume, 'duration': data['duration']}

        #si c'est pas un url verifie si le son existe dans les fichier du bot
        elif os.path.exists(f"botSound/{self.id}/{son}.mp3"):
            song = {'source':f"botSound/{self.id}/{son}.mp3", 'title':son, 'volume':volume, 'duration': getAudioDuration(f"botSound/{self.id}/{son}.mp3")}
        
        #si c'est pas dans les fichier du bot alors faire un recherche youtube
        else:
            search = VideosSearch(son, limit=1)
            data = self.ytdl.extract_info(search.result()["result"][0]["link"], download=False)
            song = {'source':data['url'], 'title':data['title'], 'volume':volume, 'duration': data['duration']}

        return song