import discord
import os
from discord import app_commands
from discord.ext import commands

class Del_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour supprimé des fichier dans la liste
    @app_commands.command(name="del_sound", description="Supprime des sons à pour le bot dans votre serveur")    
    async def del_slash(self, interaction: discord.Interaction, fichier: str):
        if interaction.channel.type != discord.ChannelType.private:

            if not fichier.endswith(".mp3"):
                fichier += ".mp3"              #ajoute .mp3 on nom du fichier a supprimé
            if os.path.exists(f"botSound/{interaction.guild.id}/{fichier}"):
                os.remove(f"botSound/{interaction.guild.id}/{fichier}")
                await interaction.response.send_message(f"{fichier} à été supprimé",ephemeral=True,delete_after=30)
            else:
                await interaction.response.send_message(f"{fichier} est introuvable",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Cette commandes n'est pas disponible en message privé",delete_after=120)


    @del_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Del_slash(bot))