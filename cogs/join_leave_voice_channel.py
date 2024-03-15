import discord
import functions as f
from discord.ext import commands
import variable as v

class Join_leave_voice_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        # Vérifie si le membre a rejoint un canal vocal
        if before.channel is None and after.channel is not None and not member.bot:

            f.log(member.name,"Join-Voice-Channel",f"{member.guild.name} / {after.channel.name}")

            if not f.isServerExist(member.guild):
                f.createServer(member.guild)
            if not f.isUserExist(member):
                f.createUser(member)
            if not f.isServerProfileExist(member):
                f.createServerProfile(member)

            f.newVocalSession(member)

            if not member.guild.id in v.guild_status:
                if member.guild.id in v.cantJoin:
                    if v.cantJoin[member.guild.id] <= f.getTime():
                        del v.cantJoin[member.guild.id]

                if not member.guild.id in v.cantJoin:
                    if f.checkCanJoinVoc(member.guild.id):
                        v.guild_status.append(member.guild.id)
                        await f.randomJoin(self.bot,member.guild)
                    else:
                        v.cantJoin[member.guild.id] = f.getTime()+10800
            
                


        #verifie si le membre a quitte le canal
        elif before.channel is not None and after.channel is None and not member.bot:
            f.log(member.name,"Left-Voice-Channel",f"{member.guild.name} / {before.channel.name}")
            f.closeVocalSession(member)

            

async def setup(bot):
    await bot.add_cog(Join_leave_voice_channel(bot))