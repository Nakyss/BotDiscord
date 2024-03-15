import discord
from functions import checkCanJoinVoc,editCanJoinVoc,folderExist,createFolder,log
from discord import app_commands
from discord.ext import commands
from variable import cantJoin

class Disable_voc_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour activer le join random du bot
    @app_commands.command(name="enable_voc_join", description="Autorise le bot à rejoindre le vocal à des moment aleatoire")
    @app_commands.guild_only()
    async def disable_voc_slash(self, interaction: discord.Interaction):
        if not checkCanJoinVoc(interaction.guild.id):
            editCanJoinVoc(interaction.guild.id,1)
            if not folderExist("botSound",interaction.guild.id):
                createFolder(interaction.guild.id,"botSound")
            
            if interaction.guild.id in cantJoin:
                del cantJoin[interaction.guild.id]
            log(interaction.user.name,"Enable-Bot-Random-Join-Vocal",interaction.guild)
            await interaction.response.send_message(f"{self.bot.user.name} peut desormais rejoindre des canal vocaux n'importe quand et y joué des sons.",ephemeral=True,delete_after=45)
        else:
            await interaction.response.send_message("L'option est déjà activer dans votre serveur",ephemeral=True,delete_after=30)


    @disable_voc_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Disable_voc_slash(bot))