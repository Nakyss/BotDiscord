import discord
from discord import app_commands
from discord.ext import commands
import os



class Add_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MAX = 50

    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="add_sound", description="Ajouter des sons pour le bot dans votre serveur")
    @app_commands.guild_only()    
    async def add_sound(self, interaction: discord.Interaction, fichier:discord.Attachment):         #recupère un fichier en plus

        if fichier.content_type == "audio/mpeg":                #verifie qu'il s'agit d'un mp3
            if len(os.listdir(f"botSound/{interaction.guild.id}")) >= self.MAX:
                await interaction.response.send_message(f"La limite de {self.MAX} fichiers à été atteinte",ephemeral=True,delete_after=30)
                return
            name = fichier.filename
               #les '_' change l'affichage dans discord donc pour eviter des problèmes d'affichage 
            await fichier.save(f"botSound/{interaction.guild.id}/{name}")

            name = name.replace("_", '\\_')
            await interaction.response.send_message(f"{name} bien enregistré",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Envoyer seulement des fichier au format .mp3",ephemeral=True,delete_after=30)


    @add_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Add_sound(bot))