import discord
from discord import app_commands
from discord.ext import commands
from variable import allServer

class Remove_Last(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    #Commande pour enlever le dernier element de la liste
    @app_commands.command(name="remove_last", description="Enlève le dernier son ajouté dans le liste")
    @app_commands.guild_only()
    async def remove_last(self, interaction: discord.Interaction):
        server = allServer[interaction.guild.id]
        vc = server.voiceClient
        if len(server.musicQueue):
            if interaction.user.voice != None:
                if interaction.user.voice.channel != vc.channel:
                    await interaction.response.send_message(f"Vous n'etes pas connecté dans le même canal vocal que {self.bot.user.name}",ephemeral=True,delete_after=30)
                    return
                
                if len(server.musicQueue) > 1:
                    nameOfSong=server.musicQueue[-1]['title']
                    server.musicQueue.pop(-1)
                    await interaction.response.send_message(f"C'est bon **'{nameOfSong}'** a été supprimé de la liste",ephemeral=True,delete_after=10)
                else:
                    await interaction.response.send_message(f"Vous êtes déjà en train d'ecouter le dernier son, utiliser `/stop` ou `/skip` pour arreté.",ephemeral=True,delete_after=25)
            else:
                await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message(f"Aucun élément dans la liste",ephemeral=True,delete_after=30)


    @remove_last.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Remove_Last(bot))
