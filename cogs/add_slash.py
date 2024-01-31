import discord
from discord import app_commands
from discord.ext import commands


class Add_slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour ajouter des fichier dans la liste
    @app_commands.command(name="add_sound", description="Ajouter des sons à pour le bot dans votre serveur")    
    async def add_slash(self, interaction: discord.Interaction, fichier:discord.Attachment):         #recupère un fichier en plus
        if interaction.channel.type != discord.ChannelType.private:

            if fichier.content_type == "audio/mpeg":                #verifie qu'il s'agit d'un mp3
                name = fichier.filename
                name = name.replace("_",'-')    #les '_' change l'affichage dans discord donc pour eviter des problèmes d'affichage 
                await fichier.save(f"botSound/{interaction.guild.id}/{name}")
                await interaction.response.send_message(f"{name} bien enregistré",ephemeral=True,delete_after=30)
            else:
                await interaction.response.send_message("Envoyer seulement des fichier au format .mp3",ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Cette commandes n'est pas disponible en message privé",delete_after=120)


    @add_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Add_slash(bot))