import discord
from functions import log
from discord import app_commands
from discord.ext import commands
from variable import db


class Disable_voc_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour desactiver le join random du bot
    @app_commands.command(name="disable_voc_join", description="Empeche le bot de rejoindre le vocal à des moment aleatoire")
    @app_commands.guild_only()
    async def disable_voc_join(self, interaction: discord.Interaction):
        if db.checkCanJoinVoc(interaction.guild.id):
            db.editCanJoinVoc(interaction.guild.id,0)
            await interaction.response.send_message(f"{self.bot.user.name} ne peut plus rejoindre des canal vocaux dans se serveur.",ephemeral=True,delete_after=45)
            log(interaction.user.name,"Disable-Bot-Random-Join-Vocal",interaction.guild)
        else:
            await interaction.response.send_message("L'option est déjà désactiver dans votre serveur",ephemeral=True,delete_after=30)

    @disable_voc_join.error
    async def say_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Disable_voc_join(bot))

