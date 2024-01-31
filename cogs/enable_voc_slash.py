import discord
from functions import checkCanJoinVoc,editCanJoinVoc,log
from discord import app_commands
from discord.ext import commands


class Enable_voc_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour desactiver le join random du bot
    @app_commands.command(name="disable_voc_join", description="Empeche le bot à rejoindre le vocal à des moment aleatoire")
    async def enable_voc_slash(self, interaction: discord.Interaction):

        if interaction.channel.type != discord.ChannelType.private:
            if checkCanJoinVoc(interaction.guild.id):
                editCanJoinVoc(interaction.guild.id,0)
                await interaction.response.send_message(f"{self.bot.user.name} ne peut plus rejoindre des canal vocaux dans se serveur.",ephemeral=True,delete_after=45)
                log(interaction.user.name,"Disable-Bot-Random-Join-Vocal",interaction.guild)
            else:
                await interaction.response.send_message("L'option est déjà désactiver dans votre serveur",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Cette commandes n'est pas disponible en message privé",delete_after=120)


    @enable_voc_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Enable_voc_slash(bot))