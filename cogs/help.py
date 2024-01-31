import discord
from discord import app_commands
from discord.ext import commands
from variable import helpmessage
 

class Help_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande help
    @app_commands.command(name="help", description="Liste des possibilité du bot")
    async def help_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(helpmessage,ephemeral=True,delete_after=400)


    @help_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Help_slash(bot))