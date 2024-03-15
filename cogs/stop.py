import discord
from discord import app_commands
from discord.ext import commands
from variable import voiceClient,musicQueue

class Stop_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="stop", description="Arrete la liste en cours et deconnecte le bot")
    @app_commands.guild_only()
    async def stop_sound(self, interaction: discord.Interaction):
        if interaction.guild.id in musicQueue:
            if interaction.user.voice != None:
                if interaction.user.voice.channel != voiceClient[interaction.guild.id][0].channel:
                    await interaction.response.send_message(f"Vous n'etes pas connecté dans le même canal vocal que {self.bot.user.name}",ephemeral=True,delete_after=30)
                    return
                
                vc = voiceClient[interaction.guild.id][0]
                musicQueue[interaction.guild.id] = [0]
                await interaction.response.send_message("Deconnexion...",ephemeral=True,delete_after=40)
                vc.pause()
                vc.stop()
                
            else:
                await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message(f"{self.bot.user.name} ne joue actuellement aucun son",ephemeral=True,delete_after=30)


    @stop_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Stop_sound(bot))
