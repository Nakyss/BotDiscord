import discord
from os import listdir
from discord import app_commands
import functions
from discord.ext import commands

class List_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="list_sound", description="Affiche tout les sons pour votre serveur")
    @app_commands.guild_only()               
    async def list_sound(self, interaction: discord.Interaction):
        if functions.folderExist("botSound",f"{interaction.guild.id}"):
            listSound = listdir(f"botSound/{interaction.guild.id}")
            if len(listSound)==0:
                await interaction.response.send_message("Aucun sons enregistrés",ephemeral=True,delete_after=30)

            displayList = ""
            for i in range(len(listSound)):
                nameSong = listSound[i][:-4].replace("_", '\\_')
                displayList += f"\n{nameSong}"   #enleve le .mp3 a la fin du fichier et l'ajoute au message
            await interaction.response.send_message(displayList,ephemeral=True,delete_after=300)
        else: 
            await interaction.response.send_message("L'option n'est pas activé sur votre serveur",ephemeral=True,delete_after=30)
    



    @list_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)




async def setup(bot):
    await bot.add_cog(List_sound(bot))