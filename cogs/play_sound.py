import discord
from discord import app_commands
from discord.ext import commands
import functions
from typing import List
from variable import musicQueue,voiceClient


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
    @app_commands.command(name="play", description="Joue un son, soit un des son proposé ou alors avec Youtube, avec un URL ou une simple recherche")
    @app_commands.guild_only()
    @app_commands.autocomplete(son=play_autocomplete)
    @app_commands.describe(son='Un son parmi ceux proposés ou un lien ou titre de video youtube',volume='Le volume du media, 100 par defaut')
    async def play_sound(self, interaction: discord.Interaction, son:str, volume:int=100):
        if interaction.user.voice != None:
            song = functions.getSong(son,interaction,volume)

            if interaction.guild.id in musicQueue:
                if interaction.user.voice.channel != voiceClient[interaction.guild.id][0].channel:
                    await interaction.response.send_message(f"Vous n'etes pas connecté dans le même canal vocal que {self.bot.user.name}",ephemeral=True,delete_after=30)
                    return
                musicQueue[interaction.guild.id].append(song)
                await interaction.response.send_message(f"Ajout de **'{song['title']}'** en {len(musicQueue[interaction.guild.id])} eme position de la liste",ephemeral=True,delete_after=40)

            else:
                await interaction.response.send_message(f"Lancement de **'{song['title']}'**",ephemeral=True,delete_after=40)
                musicQueue[interaction.guild.id] = [song]
                voice_channel = interaction.user.voice.channel

                vc = await voice_channel.connect()
                voiceClient[interaction.guild.id] = [vc,0]
                await functions.playSong(interaction)
        else:
            await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)



    @play_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Play_sound(bot))
