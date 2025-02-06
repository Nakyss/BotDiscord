import discord
from discord import app_commands
from discord.ext import commands
from typing import List
from variable import allServer
import functions as f

class Dl_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def dl_sound_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        server = allServer[interaction.guild.id]
        choices = server.getAllSong()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]


    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="download_sound", description="Permet de télécharger un son du serveur ou via Youtube, avec un URL ou une simple recherche")
    @app_commands.autocomplete(son=dl_sound_autocomplete)
    @app_commands.describe(son='Un son parmi ceux proposés ou un lien ou titre de video youtube')
    @app_commands.guild_only()
    async def dl_sound(self, interaction: discord.Interaction, son:str):
        server = allServer[interaction.guild.id]
        
        await interaction.response.send_message(f"Un instant le fichier arrive ....",ephemeral=True,delete_after=30)
        download = server.downloadSong(son)
        if download == None:
            appInfo = await self.bot.application_info()
            await interaction.edit_original_response(content=f"Il y'a un problème avec les videos Youtube, vous pouvez contacter <@{appInfo.owner.id}>")
            return
        await interaction.channel.send(f"Le fichier **{download['title']}** est prêt à être télécharger",file=discord.File(download['source']))
        f.log(interaction.user.name,"file-"+download['title']+"-downloaded",f"{interaction.guild.name} / {interaction.channel.name}")

        if download['delete']:
            f.deleteFile(download['source'])


    @dl_sound.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.edit_original_response(content="Oups, une erreur est arrivé !!!!")
        print(error)


async def setup(bot):
    await bot.add_cog(Dl_sound(bot))
