import discord
from variable import mydb
import mysql.connector
from discord import app_commands
from discord.ext import commands
from functions import log

class Delete_last_spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commande pour supprimer le dernier spam envoyé
    @app_commands.command(name="delete_last_spam", description="Supprime les messages du dernier spam envoyé")
    @app_commands.guild_only()
    async def delete_last_spam(self, interaction: discord.Interaction):

        db = mysql.connector.connect(**mydb)
        c = db.cursor()
        c.execute(f"SELECT LS.ID_SPAM ,LS.ID_MESSAGE, S.ID_USER FROM LAST_SPAM LS JOIN SPAM S ON LS.ID_SPAM = S.ID_SPAM WHERE LS.ID_CHANNEL = {interaction.channel.id};")
        result = c.fetchall()


        if (interaction.user.id == result[0][2] or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_messages):
            allMessage = []

            if not len(result):
                await interaction.response.send_message("Aucun spam enregistré dans ce channel")
                c.close()
                db.close()
                return

            allMessage.append(interaction.channel.get_partial_message(result[0][0]))

            for line in result:
                allMessage.append(interaction.channel.get_partial_message(line[1]))

            await interaction.response.send_message("C'est bon y'a moins de spam, normalement les messages vont se supprimer")
            log(interaction.user.name,"Delete-the-last-spam",f"{interaction.guild.name} / {interaction.channel.name}")
            try : 
                await interaction.channel.delete_messages(allMessage)
            except Exception:
                await interaction.response.send_message("Je crois bien que tu va pas pouvoir effacer ta trace",ephemeral=True,delete_after=30)

            c.execute(f"DELETE FROM LAST_SPAM WHERE ID_CHANNEL = {interaction.channel.id};")
            db.commit()
        else:
            await interaction.response.send_message("Tu ne peux pas supprimer un spam que tu n'as pas envoyé",ephemeral=True,delete_after=30)

        c.close()
        db.close()
        

        

    @delete_last_spam.error
    async def say_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Oups, une erreur est arrivé !!!!",ephemeral=True,delete_after=30)


async def setup(bot):
    await bot.add_cog(Delete_last_spam(bot))