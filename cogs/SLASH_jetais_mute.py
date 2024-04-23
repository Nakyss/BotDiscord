import discord
from discord import app_commands
from discord.ext import commands
from functions import openJson,format_total_time,getTime

class Jetais_mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="jetais_mute", description="Pour savoir depuis combien de temps tu etait mute")
    @app_commands.guild_only()
    async def jetais_mute(self, interaction: discord.Interaction):
        data = openJson()
        if f"{interaction.user.id}" in data:
            if len(data[f"{interaction.user.id}"]) == 2:
                await interaction.response.send_message("Tu t'es pas mute",ephemeral=True ,delete_after=15)
            else:
                if data[f"{interaction.user.id}"][3] == None:
                    await interaction.response.send_message("Oui mais t'es encore mute gros con",ephemeral=True ,delete_after=30)
                else:
                    time_since = int(getTime()-data[f"{interaction.user.id}"][3])
                    totaltime = int(data[f"{interaction.user.id}"][3]-data[f"{interaction.user.id}"][2])
                    await interaction.response.send_message(f"<@{interaction.user.id}> est demute depuis {format_total_time(time_since)} mais il était mute pendant {format_total_time(totaltime)} (gros con)")
        else:
            await interaction.response.send_message("T'es même pas en vocal",ephemeral=True ,delete_after=15)

    @jetais_mute.error
    async def say_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Jetais_mute(bot)) 