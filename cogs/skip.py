import discord
from discord import app_commands
from discord.ext import commands
import functions
from variable import voiceClient,musicQueue

class Skip_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="skip", description="Passe au son suivant dans la liste")
    @app_commands.guild_only()
    async def skip_sound(self, interaction: discord.Interaction):
        if interaction.guild.id in musicQueue:
            if interaction.user.voice != None:
                if interaction.user.voice.channel != voiceClient[interaction.guild.id][0].channel:
                    await interaction.response.send_message(f"Vous n'etes pas connecté dans le même canal vocal que {self.bot.user.name}",ephemeral=True,delete_after=30)
                    return
                
                if len(musicQueue[interaction.guild.id]) > 1:
                    await interaction.response.send_message(f"Lancement de **'{musicQueue[interaction.guild.id][1]['title']}'**",ephemeral=True,delete_after=40)
                else:
                    await interaction.response.send_message(f"C'etait le dernier son de la liste. Deconnexion",ephemeral=True,delete_after=40)
                vc = voiceClient[interaction.guild.id][0]
                vc.pause()
                vc.stop()
            else:
                await interaction.response.send_message("Vous n'etes pas connecté dans un canal vocal",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message(f"{self.bot.user.name} ne joue actuellement aucun son",ephemeral=True,delete_after=30)


    @skip_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Skip_sound(bot))
