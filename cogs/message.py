import discord
import functions as f
from discord.ext import commands
from random import randint
from variable import pv_mess_possibilities,channel_status,possibilites

class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        #--On vérifie que ce n'est pas nous même (le bot) qui envoie le message---
        if message.author.bot:
            return
        
        #--Si il s'agit d'un message privé--------
        if message.channel.type == discord.ChannelType.private:
            appInfo = await self.bot.application_info()
            #si le message viens du createur du bot il a acces à des commandes
            if message.author == appInfo.owner:
                await f.admin(message)
                return
            
            #Sinon envoyé un message parmit cette liste
            else : 
                await message.channel.send(pv_mess_possibilities[randint(0,len(pv_mess_possibilities) -1)])
                return


        #--Si c'est un message de bienvenue----
        if message.type == discord.MessageType.new_member:
            return
        

        #----------si l'utilisateur n'existe pas dans la db ou qu'il n'a pas de profil de server--------
        if not f.isServerExist(message.guild):
                f.createServer(message.guild)
        if not f.isUserExist(message.author):
            f.createUser(message.author)
        if not f.isServerProfileExist(message.author):
            f.createServerProfile(message.author)


        # Prise en charge des majuscules et mininuscules
        #si le message commence par spam 
        if message.content.lower().startswith('spam'):
            # Vérifie si le canal est déjà occupé
            if message.channel.id in channel_status and channel_status[message.channel.id]:
                await message.channel.send("Un spam est déjà en cours, veuillez patienter.")
                return

            #decoupe le message a chaque espace
            cutedContent=f.cutMessage(message.content)

            nbRep = cutedContent[1]
            messSpam = cutedContent[2]

            # Marque le canal comme occupé
            channel_status[message.channel.id] = True

            #si plus de 2000 rep pas faire 
            if (nbRep >2000):
                f.log(message.author,f"Send-4-'{f.clearBackslashN(messSpam)}'",f"{message.guild.name} / {message.channel.name}")

                await message.channel.send("frero abuse, dose un peu")

                for i in range(4):
                    await message.channel.send(messSpam)
                await message.channel.send("4 fois c'est deja pas mal")

                f.newSpam(message,4,messSpam)  #add to db
                
                channel_status[message.channel.id] = False
                return
            
            f.log(message.author,f"Send-{nbRep}-'{f.clearBackslashN(messSpam)}'",f"{message.guild.name} / {message.channel.name}")
            
            f.newSpam(message,nbRep,messSpam) #add to db

            # si plus de 6 rep repartir les rep dans plusieur messages
            if (nbRep > 6 ):
                tab = f.calculNbMess(messSpam,nbRep)
                
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
            f.newMessage(message)

        

        # Si le contenu du message dont on a enlevé la ponctuation et les espaces termine par un des mots listés dans le dictionnaire possibilites, alors répondre au hasard une des réponses présente dans la liste correspondante
        for i in possibilites:
            if f.retirer_points(message.content).endswith(i): 
                await message.channel.send(possibilites[i][randint(0, len(possibilites[i]) - 1)])
        


async def setup(bot):
    await bot.add_cog(MessageCog(bot))