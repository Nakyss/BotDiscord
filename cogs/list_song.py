import discord
from discord import app_commands
from discord.ext import commands
from variable import voiceClient,musicQueue
from functions import audioDuration, getTime

def displayBar(actual,total):
    SIZEDISPLAY = 45

    size = int((actual*SIZEDISPLAY)/total)
    if size == 0:
        size = 1

    actual = audioDuration(actual)

    total = audioDuration(total)
    
    return f" {actual} [{'='*(size-1)}|{'-'*(SIZEDISPLAY-size)}] {total}"

class List_Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(name="display_queue", description="Affiche tout les sons dans le liste de lecture")
    @app_commands.guild_only()
    async def ls_slash(self, interaction: discord.Interaction):
        if interaction.guild.id in musicQueue and len(musicQueue[interaction.guild.id]) != 0:

            actualTime = getTime() - voiceClient[interaction.guild.id][1]
            embed = discord.Embed(title=musicQueue[interaction.guild.id][0]['title'], description=displayBar(actualTime,musicQueue[interaction.guild.id][0]['duration']),color=0x20e7ff)
            if len(musicQueue[interaction.guild.id]) > 1 : 
                embed.add_field(name="A venir", value="-----------------------------------------------------------------", inline=False)
                for i in range (1,len(musicQueue[interaction.guild.id])):
                    embed.add_field(name=f"#{i} - {musicQueue[interaction.guild.id][i]['title']}",value=f"Volume : {musicQueue[interaction.guild.id][i]['volume']}%   Durée : {audioDuration(musicQueue[interaction.guild.id][i]['duration'])}", inline=False)
            
            await interaction.response.send_message(embed=embed,delete_after=(musicQueue[interaction.guild.id][0]['duration']-actualTime),silent=True)

        else:
            await interaction.response.send_message("Aucun élement dans la liste",ephemeral=True,delete_after=30)
        


    @ls_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(List_Song(bot))
