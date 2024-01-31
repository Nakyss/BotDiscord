import discord
from functions import isServerProfileExist,log,isUserExist,isServerExist,createServer,createServerProfile,createUser,newVocalSession,closeVocalSession
from discord.ext import commands

class Join_leave_voice_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        # Vérifie si le membre a rejoint un canal vocal
        if before.channel is None and after.channel is not None and member != member.bot:

            if not isServerExist(member.guild):
                createServer(member.guild)
            if not isUserExist(member):
                createUser(member)
            if not isServerProfileExist(member):
                createServerProfile(member)

            log(member.name,"Join-Voice-Channel",f"{member.guild.name} / {after.channel.name}")

            newVocalSession(member)


        #verifie si le membre a quitte le canal
        elif before.channel is not None and after.channel is None and member != member.bot:
            closeVocalSession(member)

            log(member.name,"Left-Voice-Channel",f"{member.guild.name} / {before.channel.name}")

async def setup(bot):
    await bot.add_cog(Join_leave_voice_channel(bot))