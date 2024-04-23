from functions import log,getTime,setMute,setUnMute
from discord.ext import commands
from variable import db,allServer

class Join_leave_voice_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        # Vérifie si le membre a rejoint un canal vocal
        if before.channel is None and after.channel is not None and not member.bot:
            server = allServer[member.guild.id]

            log(member.name,"Join-Voice-Channel",f"{member.guild.name} / {after.channel.name}")

            if not db.isServerExist(member.guild.id):
                db.createServer(member.guild)
            if not db.isUserExist(member.id):
                db.createUser(member)
            if not db.isServerProfileExist(member):
                db.createServerProfile(member)

            db.newVocalSession(member)


            if not server.isRandomJoinActive:
                if server.isRandomJoinDisable and server.lastActualisation <= getTime():
                    server.isRandomJoinDisable = False

                if not server.isRandomJoinDisable:
                    if db.checkCanJoinVoc(server.id):
                        server.isRandomJoinActive = True
                        await server.randomJoin(self.bot,member.guild)
                    else:
                        server.isRandomJoinDisable = True
                        server.lastActualisation = getTime()+10800
                

        #verifie si le membre a quitte le canal
        elif before.channel is not None and after.channel is None and not member.bot:
            log(member.name,"Left-Voice-Channel",f"{member.guild.name} / {before.channel.name}")
            db.closeVocalSession(member)

        # mute
        elif not before.self_mute and after.self_mute:
            setMute(member.id)

        # unmute
        elif before.self_mute and not after.self_mute:
            setUnMute(member.id)
            

async def setup(bot):
    await bot.add_cog(Join_leave_voice_channel(bot))