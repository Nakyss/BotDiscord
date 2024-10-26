import discord
import os
from discord import app_commands
from discord.ext import commands
from typing import List
from variable import allServer
from functions import log

class Delete_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def del_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        choices = allServer[interaction.guild.id].getAllSong()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

    #Commande pour supprimé des file dans la liste
    @app_commands.command(name="delete_sound", description="Supprime des sons pour le bot dans votre serveur")
    @app_commands.guild_only()   
    @app_commands.autocomplete(file=del_autocomplete)
    @app_commands.describe(file='Nom du file à supprimer') 
    async def delete_sound(self, interaction: discord.Interaction, file: str):
        if not file.endswith(".mp3"):
            file += ".mp3"              #ajoute .mp3 on nom du file a supprimé
        if os.path.exists(f"botSound/{interaction.guild.id}/{file}"):
            os.remove(f"botSound/{interaction.guild.id}/{file}")
            file = file.replace("_", '\\_')
            await interaction.response.send_message(f"{file} à été supprimé",ephemeral=True,delete_after=30)
            log(interaction.user.name,f"deleted-the-sound-{file}",interaction.guild.name)
        else:
            file = file.replace("_", '\\_')
            await interaction.response.send_message(f"{file} est introuvable",ephemeral=True,delete_after=30)
        


    @delete_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Delete_sound(bot))