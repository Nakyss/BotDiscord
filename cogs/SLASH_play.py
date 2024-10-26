import discord
from discord import app_commands
from discord.ext import commands
from typing import List
from variable import allServer,secrets
import functions as f

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def play_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        server = allServer[interaction.guild.id]
        choices = server.getAllSong()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]


    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="play", description="Joue un son, soit un des son proposé ou alors avec Youtube, avec un URL ou une simple recherche")
    @app_commands.guild_only()
    @app_commands.autocomplete(son=play_autocomplete)
    @app_commands.describe(son='Un son parmi ceux proposés ou un lien ou titre de video youtube',volume='Le volume du media, 100 par defaut')
    async def play(self, interaction: discord.Interaction, son:str, volume:int=100, secret:str=None):
        if interaction.user.voice == None:
            if (secret == None):
                await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)
                return
            elif(f"{interaction.user.id}" in secrets and secrets[f"{interaction.user.id}"] == secret):
                pass
            else:
                await interaction.response.send_message("EH NON C'EST PAS EN ECRIVANT CA DANS SECRET QUE CA VA MARCHER",ephemeral=True,delete_after=30)
                return
        


        server = allServer[interaction.guild.id]
        if len(server.musicQueue):
            if (secret == None):
                if server.voiceClient != None and interaction.user.voice.channel != server.voiceClient.channel:
                    await interaction.response.send_message(f"Vous n'etes pas connecté dans le même canal vocal que {self.bot.user.name}",ephemeral=True,delete_after=30)
                    return
                
            await interaction.response.send_message(f"Veuillez patienter.....",ephemeral=True,delete_after=40)
            song = server.getSong(son, volume)
            server.musicQueue.append(song)
            songName = song['title'].replace('_', '\\_')
            await interaction.edit_original_response(content=f"Ajout de **'{songName}'** en {len(server.musicQueue)} eme position de la liste")
                
        else:
            await interaction.response.send_message(f"Veuillez patienter.....",ephemeral=True,delete_after=40)
            song = server.getSong(son, volume)
            songName = song['title'].replace('_', '\\_')
            await interaction.edit_original_response(content=f"Lancement de **'{songName}'**")
            server.musicQueue = [song]
            if (secret == None):
                voice_channel = interaction.user.voice.channel
            else:
                voice_channel = f.maxUser(interaction.guild.voice_channels)

            vc = await voice_channel.connect()
            server.voiceClient = vc

            await server.playSong(interaction)



    @play.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Play(bot))
