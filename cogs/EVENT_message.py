import discord
from functions import log,removePunctuation
import adminFunction
from discord.ext import commands
from random import randint
from variable import pv_mess_possibilities,allServer,possibilites,db

from classSpam import Spam

class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #--Si c'est un message system----
        if message.is_system():
            return

        #--On vérifie que ce n'est pas un bot qui envoie le message---
        if message.author.bot:
            return

        #--Si il s'agit d'un message privé--------
        if message.channel.type == discord.ChannelType.private:
            appInfo = await self.bot.application_info()
            #si le message viens du createur du bot il a acces à des commandes
            if message.author == appInfo.owner:
                if message.content.lower().startswith("cmd"):
                    await adminFunction.admin(self.bot,message)
                    return
            author = db.getSay_to(message.author.id)
            if author == None:
                await message.channel.send(pv_mess_possibilities[randint(0,len(pv_mess_possibilities) -1)])
            else:
                receiver = self.bot.get_user(author[0])
                if message.content != "":
                    await receiver.send(message.content)
                    if not db.isUserExist(message.author.id):
                        db.createUser(message.author)
                    db.newSay_To(message.author.id, author[0], db.clearQuotes(message.content))
                elif len(message.attachments) != 0:
                    await message.reply("Je peut pas envoyer de fichier pour le moment parce que <@423482629220990985> avait la flemme de le coder")
            return



        

        #----------si l'utilisateur n'existe pas dans la db ou qu'il n'a pas de profil de server--------
        if not db.isServerExist(message.guild.id):
                db.createServer(message.guild)
        if not db.isUserExist(message.author.id):
            db.createUser(message.author)
        if not db.isServerProfileExist(message.author):
            db.createServerProfile(message.author)


        #si le message commence par spam 
        if message.content.lower().startswith('spam'):
            server = allServer[message.guild.id]
            # Vérifie si le canal est déjà occupé
            if server.isChannelSpamming:
                await message.channel.send("Un spam est déjà en cours, veuillez patienter.")
                return

            #crée l'objet spam
            spam = Spam(message.content)

            # Marque le canal comme occupé
            server.isChannelSpamming = True
            
            #connexion db
            db.deleteLastSpam(message.channel)

            #si plus de 2000 rep pas faire 
            if (spam.nbRep >2000):
                log(message.author,f"Send-4-'{db.clearBackslashN(spam.messageToSpam)}'",f"{message.guild.name} / {message.channel.name}")

                await message.channel.send("frero abuse, dose un peu")
                await db.saveSpamMessage(message)

                for i in range(4):
                    await message.channel.send(spam.messageToSpam)
                    await db.saveSpamMessage(message)
                await message.channel.send("4 fois c'est deja pas mal")
                await db.saveSpamMessage(message)

                db.newSpam(message,4,spam.messageToSpam)  #add to db
                
                server.isChannelSpamming = False
                return
            
            log(message.author,f"Send-{spam.nbRep}-'{db.clearBackslashN(spam.messageToSpam)}'",f"{message.guild.name} / {message.channel.name}")
            
            db.newSpam(message,spam.nbRep,spam.messageToSpam) #add to db

            # si plus de 6 rep repartir les rep dans plusieur messages
            if (spam.nbRep > 6 ):
                for i in range (spam.nbMessageToSend):
                    await message.channel.send((spam.messageToSpam+"\n")*spam.nbRepByMessage)
                    await db.saveSpamMessage(message)
                if (spam.nbRepByMessage != 0):
                    await message.channel.send((spam.messageToSpam+"\n")*spam.nbRepByMessage)
                    await db.saveSpamMessage(message)
                
            elif(spam.nbRep > 0):
            #envoie nbRep fois le messages
                for i in range (spam.nbRep):
                    await message.channel.send(spam.messageToSpam)
                    await db.saveSpamMessage(message)

            else:
                await message.channel.send("Pourquoi faire ?")

            server.isChannelSpamming = False
            return
        else:
            #ajoute un message si c'est pas un spam
            db.newMessage(message)

        

        # Si le contenu du message dont on a enlevé la ponctuation et les espaces termine par un des mots listés dans le dictionnaire possibilites, alors répondre au hasard une des réponses présente dans la liste correspondante
        for i in possibilites:
            if removePunctuation(message.content).endswith(i): 
                await message.reply(possibilites[i][randint(0, len(possibilites[i]) - 1)])
        


async def setup(bot):
    await bot.add_cog(MessageCog(bot))