import discord
from functions import checkCanJoinVoc,editCanJoinVoc,folderExist,createFolder,log
from discord import app_commands
from discord.ext import commands


class Disable_voc_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour activer le join random du bot
    @app_commands.command(name="enable_voc_join", description="Autorise le bot à rejoindre le vocal à des moment aleatoire")
    async def disable_voc_slash(self, interaction: discord.Interaction):

        if interaction.channel.type != discord.ChannelType.private:
            if not checkCanJoinVoc(interaction.guild.id):
                editCanJoinVoc(interaction.guild.id,1)
                if not folderExist("botSound",interaction.guild.id):
                    createFolder(interaction.guild.id,"botSound")
                log(interaction.user.name,"Enable-Bot-Random-Join-Vocal",interaction.guild)
                await interaction.response.send_message(f"{self.bot.user.name} peut desormais rejoindre des canal vocaux n'importe quand et y joué des sons.",ephemeral=True,delete_after=45)
            else:
                await interaction.response.send_message("L'option est déjà activer dans votre serveur",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Cette commandes n'est pas disponible en message privé",delete_after=120)


    @disable_voc_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Disable_voc_slash(bot))