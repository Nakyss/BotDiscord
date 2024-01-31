import discord
from functions import isServerProfileExist,updateServerProfile,log,isUserExist,updateUser
from discord.ext import commands

class User_update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        if isServerProfileExist(after):
                updateServerProfile(after)

        if before.display_name != after.display_name: #changement de nom de server
            log(after.name,f"Change-Display_name-from-'{before.display_name}'-to-'{after.display_name}'",after.guild.name)

        if before.display_avatar.url != after.display_avatar.url:  #changement d'avatar de serveur
            log(after.name,f"Change-Server-Profil-Picture",after.guild.name)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):

        if isUserExist(after):
            updateUser(after)

        if before.name != after.name:    #changement de nom
            log(after.name,f"Change-name-from-'{before.name}'-to-'{after.name}'","Nowhere")

        if before.global_name != after.global_name: #changement de nom d'affichage
            log(after.name,f"Change-Global_name-from-'{before.global_name}'-to-'{after.global_name}'","Nowhere")

        if before.avatar.url != after.avatar.url:   #changement d'avatar
            log(after.name,f"Change-Profil-Picture","Nowhere")

async def setup(bot):
    await bot.add_cog(User_update(bot))