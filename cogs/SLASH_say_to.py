import discord
from discord import app_commands
from discord.ext import commands
from functions import log
from variable import db


class Say_to(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say_to", description="Envoie un message privé à quelqu'un anonymement ou pas ")
    @app_commands.guild_only()
    async def say_to(self, interaction: discord.Interaction, member: discord.Member , message:str):
        
        await member.send(message)
        await interaction.response.send_message(f"Le message suivant à été envoyé à <@{member.id}>:\n{message}",ephemeral=True)
        log(interaction.user.name,f"Send a message to {member.name}",f"{interaction.guild.name} / {interaction.channel.name}")


        #check dans la db si l'auteur existe sinon le crée 
        if not db.isServerExist(interaction.guild.id):
                db.createServer(interaction.guild)
        if not db.isUserExist(interaction.user.id):
            db.createUser(interaction.user)
        if not db.isServerProfileExist(interaction.user):
            db.createServerProfile(interaction.user)



        db.newSay_To(interaction.user.id, member.id, message)
        
    @say_to.error
    async def say_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Say_to(bot)) 