import discord
import os
from discord import app_commands
from discord.ext import commands
from typing import List
import functions

class Del_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def del_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        choices = functions.getAllSong(interaction)
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

    #Commande pour supprimé des fichier dans la liste
    @app_commands.command(name="del_sound", description="Supprime des sons à pour le bot dans votre serveur")
    @app_commands.guild_only()   
    @app_commands.autocomplete(fichier=del_autocomplete)
    @app_commands.describe(fichier='Nom du fichier à supprimer') 
    async def del_slash(self, interaction: discord.Interaction, fichier: str):
        if not fichier.endswith(".mp3"):
            fichier += ".mp3"              #ajoute .mp3 on nom du fichier a supprimé
        if os.path.exists(f"botSound/{interaction.guild.id}/{fichier}"):
            os.remove(f"botSound/{interaction.guild.id}/{fichier}")
            fichier = fichier.replace("_",'\_') 
            await interaction.response.send_message(f"{fichier} à été supprimé",ephemeral=True,delete_after=30)
        else:
            fichier = fichier.replace("_",'\_') 
            await interaction.response.send_message(f"{fichier} est introuvable",ephemeral=True,delete_after=30)
        


    @del_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Del_slash(bot))