import discord
from discord import app_commands
from discord.ext import commands
from variable import allServer
from functions import audioDuration, getTime
import asyncio

def displayBar(actual,total):
    SIZEDISPLAY = 45

    size = int((actual*SIZEDISPLAY)/total)
    if size == 0:
        size = 1

    actual = audioDuration(actual)

    total = audioDuration(total)
    
    return f" {actual} [{'='*(size-1)}|{'-'*(SIZEDISPLAY-size)}] {total}"

class Display_Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(name="display_queue", description="Affiche tout les sons dans le liste de lecture")
    @app_commands.guild_only()
    async def display_queue(self, interaction: discord.Interaction):
        server = allServer[interaction.guild.id]
        nbMusic = len(server.musicQueue)
        if nbMusic != 0:
            actualTime = getTime() - server.beginningTime
            embed = discord.Embed(title=server.musicQueue[0]['title'].replace('_', '\\_'), description=displayBar(actualTime,server.musicQueue[0]['duration']),color=0x20e7ff)
            if len(server.musicQueue) > 1 : 
                embed.add_field(name="A venir", value="-----------------------------------------------------------------", inline=False)
                for i in range (1,len(server.musicQueue)):
                    title = server.musicQueue[i]['title'].replace('_', '\\_')
                    embed.add_field(name=f"#{i} - {title}", value=f"Volume : {server.musicQueue[i]['volume']}%   Durée : {audioDuration(server.musicQueue[i]['duration'])}", inline=False)
            await interaction.response.send_message(embed=embed,silent=True)


            while(len(server.musicQueue)):
                if len(server.musicQueue) == nbMusic:
                    actualTime = getTime() - server.beginningTime
                    upadateEmbed = discord.Embed(title=server.musicQueue[0]['title'].replace('_', '\\_'), description=displayBar(actualTime,server.musicQueue[0]['duration']),color=0x20e7ff)
                    for field in embed.fields:
                        upadateEmbed.add_field(name=field.name, value=field.value, inline=field.inline)

                else:
                    embed.clear_fields()
                    if len(server.musicQueue) > 1 :
                        embed.add_field(name="A venir", value="-----------------------------------------------------------------", inline=False)
                        for i in range (1,len(server.musicQueue)):
                            title = server.musicQueue[i]['title'].replace('_', '\\_')
                            embed.add_field(name=f"#{i} - {title}", value=f"Volume : {server.musicQueue[i]['volume']}%   Durée : {audioDuration(server.musicQueue[i]['duration'])}", inline=False)

                try:
                    await interaction.edit_original_response(embed=upadateEmbed)
                except discord.errors.NotFound:
                    print("display queue suprimmer return, arret de la fonction")
                    return
                nbMusic = len(server.musicQueue)
                await asyncio.sleep(1)
                
            await interaction.delete_original_response()    
        else:
            await interaction.response.send_message("Aucun élement dans la liste",ephemeral=True,delete_after=30)
        

    @display_queue.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)
        print(error)


async def setup(bot):
    await bot.add_cog(Display_Queue(bot))
