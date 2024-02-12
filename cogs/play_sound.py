import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import functions
from typing import List
from variable import musicQueue
from yt_dlp import YoutubeDL


YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
ytdl = YoutubeDL(YDL_OPTIONS)

class Play_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def play_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        choices = functions.getAllSong(interaction)
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]


    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="play", description="Joue un son specifier parmit les son disponible")
    @app_commands.guild_only()
    @app_commands.autocomplete(son=play_autocomplete)
    async def play_sound(self, interaction: discord.Interaction, son:str):        #recupère un fichier en plus
        if interaction.guild.id in musicQueue:
            await functions.addSong(son,interaction)
        else:
            if interaction.user.voice == None:
                await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)
                return
            await functions.newJoin(son,interaction)

        


    @play_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Play_sound(bot))
