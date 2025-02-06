import discord
from discord import app_commands
from discord.ext import commands

class Stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stat", description="Accedez à vos statistiques")
    async def stat(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Vous pouvez acceder à vos statistiques ici !\nhttps://nakyss.fr/user_stats.php?user={interaction.user.id}&serv={interaction.guild.id}",ephemeral=True)


    @stat.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Stat(bot))
