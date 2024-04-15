from functions import log
from discord.ext import commands
from variable import db



class Server_update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #------------------------quand le bot est ajouter a un server---------------------------
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        log(self.bot.user.name,"Added-to-server",guild.name)
        if not db.isServerExist(guild):
            db.createServer(guild)
        else:
            db.updateServer(guild)

    #-----------------------Quand le bot est kick d'un serveur------------------------------
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        log(self.bot.user.name,"Kick-from-server",guild.name)
        db.updateServer(guild,0)


    #-----------------------changement dans sur le serveur----------------------------------
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if db.isServerExist(after.id):
            db.updateServer(after)
        else:
            db.createServer(after)



    #----------------------changement de nb User--------------------------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        log(member,"Join the server",member.guild.name)
        if db.isServerExist(member.guild.id):
            db.updateServer(member.guild)
        else:
            db.createServer(member.guild)
        


    @commands.Cog.listener()
    async def on_member_remove(self, member): 
        log(member,"Left the server",member.guild.name)
        db.deleteUser_Server(member.guild.id,member.id)
        if db.isServerExist(member.guild.id):
            db.updateServer(member.guild)
        else:
            db.createServer(member.guild)



async def setup(bot):
    await bot.add_cog(Server_update(bot))                