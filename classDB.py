import mysql.connector
from functions import getTime, getTimeV2,openJson,saveJson
import os 

class DB:
    db = None

    def connect(self):
        try:
            self.db = mysql.connector.connect(**self.mydb)
            print(f"DB Connected : {self.mydb['database']}")
        except mysql.connector.errors.ProgrammingError:
            print(f"*******************************************************\nImpossible de se connecter à la DB \n db : {self.mydb['database']} \n user : {self.mydb['user']}\n*******************************************************")

    def disconnect(self):
        self.db.close()
        print(f"DB Disconnected : {self.mydb['database']}")

    def select(self,request):
        try:
            with self.db.cursor() as c:
                c.execute(request)
                self.err_count = 0
                return c.fetchall()
        except mysql.connector.errors.OperationalError as err:
            self.err_count += 1
            if self.err_count <= 3:
                print("SQL Erreur :", err)
                self.disconnect()
                self.connect()
                return self.select(request)
            else:
                print("Impossible de se connecter à la db")
                return False
            
    def insert(self,request):
        try:
            with self.db.cursor() as c:
                c.execute(request)
                self.db.commit()
                self.err_count = 0
        except mysql.connector.errors.OperationalError as err:
            self.err_count += 1
            if self.err_count <= 3:
                print("SQL Erreur :", err)
                self.disconnect()
                self.connect()
                self.insert(request)
            else:
                print("Impossible de se connecter à la db")

    def __init__(self): 
        self.mydb = {
        'host' : os.environ.get('DISCORD_DB_HOST'),
        'user': os.environ.get('DISCORD_DB_USER'),
        'password':os.environ.get('DISCORD_DB_PASSWORD'),
        'port':os.environ.get('DISCORD_DB_PORT'),
        'database':os.environ.get('DISCORD_DB_DATABASE')
        }
        self.connect()
        self.err_count = 0

    def clearQuotes(self,message):
        """ajoute des backslash devant les ' pour eviter les probleme avec SQL"""
        return message.replace("'","\\'")

    def clearBackslashN(self,message):
        """ajoute un backslash devant les \n pour eviter les probleme avec SQL"""
        return message.replace("\n","\\n ")

    def isServerExist(self,guild_id):
        result = self.select(f"SELECT COUNT(*) FROM SERVER WHERE ID_SERVER = {guild_id}")
        return result[0][0]

    def createServer(self,guild):
        self.insert(f'''INSERT INTO `SERVER` (`ID_SERVER`, `NAME`, `ICON_URL`,`NB_USER`, `JOIN_DATE`, `CAN_JOIN_VOC`, `STATUS`) 
                        VALUES ({guild.id} ,'{self.clearQuotes(guild.name)}', '{guild.icon.with_size(128).url}',{guild.member_count}, CURDATE(), FALSE, TRUE)''')

    def updateServer(self, guild, status = 1):
        self.insert(f"UPDATE `SERVER` SET `NAME` = '{self.clearQuotes(guild.name)}', `ICON_URL` = '{guild.icon.with_size(128).url}', NB_USER = {guild.member_count}, STATUS = {status} WHERE `SERVER`.`ID_SERVER` = {guild.id}")

    def isUserExist(self,user_id):
        result = self.select(f"SELECT COUNT(*) FROM USER WHERE ID_USER = {user_id}")
        return (result[0][0] == 1)

    def updateUser(self,user):
        #garde le nom si le nom d'affichage n'existe pas 
        if user.global_name == None:
            globalName = user.name
        else:
            globalName = user.global_name

        #verifie si il a une pp ou pas
        if user.avatar == None :
            avatarUrl = user.default_avatar.with_size(128).url
        else:
            avatarUrl = user.avatar.with_size(128).url

        self.insert(f"UPDATE `USER` SET `NAME` = '{user.name}', `NAME_GLOBAL` = '{globalName}',`PP_URL` = '{avatarUrl}' WHERE `USER`.`ID_USER` = {user.id}")

    def createUser(self,user):
        #garde le nom si le nom d'affichage n'existe pas 
        if user.global_name == None:
            globalName = user.name
        else:
            globalName = user.global_name

        #verifie si il a une pp ou pas
        if user.avatar == None :
            avatarUrl = user.default_avatar.with_size(128).url
        else:
            avatarUrl = user.avatar.with_size(128).url

        self.insert(f"INSERT INTO `USER` (`ID_USER`, `NAME`, `NAME_GLOBAL`, `PP_URL`) VALUES ({user.id} ,'{self.clearQuotes(user.name)}','{self.clearQuotes(globalName)}', '{avatarUrl}')")

    def isServerProfileExist(self,user):
        result = self.select(f"SELECT COUNT(*) FROM USER_SERVER WHERE ID_USER = {user.id} AND ID_SERVER = {user.guild.id}")
        return (result[0][0] == 1)

    def updateServerProfile(self,user):
        #verifie si il a une pp ou pas
        if user.display_avatar != None:
            avatarUrl = user.display_avatar.with_size(128).url
        else:
            if user.avatar != None:
                avatarUrl = user.avatar.with_size(128).url
            else:
                avatarUrl = user.default_avatar.with_size(128).url

        self.insert(f"UPDATE `USER_SERVER` SET `NAME_SERVER` = '{self.clearQuotes(user.display_name)}', `PP_URL_SERVER` = '{avatarUrl}' WHERE `USER_SERVER`.`ID_USER` = {user.id} AND `USER_SERVER`.`ID_SERVER` = {user.guild.id}")

    def createServerProfile(self,user):
        if user.display_avatar != None:
            avatarUrl = user.display_avatar.with_size(128).url
        else:
            if user.avatar != None:
                avatarUrl = user.avatar.with_size(128).url
            else:
                avatarUrl = user.default_avatar.with_size(128).url
        
        self.insert(f"INSERT INTO `USER_SERVER` (`ID_USER`, `ID_SERVER`, `NAME_SERVER`,`PP_URL_SERVER`) VALUES ({user.id} ,{user.guild.id}, '{self.clearQuotes(user.display_name)}', '{avatarUrl}')")


    def newVocalSession(self,member):
        #---add the session to the db
        join = getTime()
        try :
            with self.db.cursor() as c:
                val = (join,member.id,member.guild.id)
                c.execute("INSERT INTO `VOCAL_SESSION` (`ID_VOC`, `JOIN`, `QUIT`, `ID_USER`, `ID_SERVER`, `TIME_VOC`) VALUES (NULL ,%s,NULL, %s, %s, NULL)",val)
                self.db.commit()
                id=c.lastrowid
                self.err_count = 0
        
            #--add the id of the session in a file
            data = openJson()
            data[member.id] = [id,join]
            saveJson(data)

        except mysql.connector.errors.OperationalError as err:
            self.err_count += 1
            if self.err_count <= 3:
                print("SQL Erreur :", err)
                self.disconnect()
                self.connect()
                self.newVocalSession(member)
            else:
                print("newVocalSession Stop")
                return False

    def closeVocalSession(self,member):
        data = openJson()

        #-check if the id exist else return bcs join wasn't save 
        if not f"{member.id}" in data:
            return 

        time = getTime()
        self.insert(f"UPDATE `VOCAL_SESSION` SET `QUIT` = {time}, `TIME_VOC` = {time-data[f'{member.id}'][1]} WHERE `VOCAL_SESSION`.`ID_VOC` = {data[f'{member.id}'][0]}")
        del data[f'{member.id}']
        saveJson(data)


    def newMessage(self,message):
        self.insert(f"""INSERT INTO `MESSAGE` (ID_MESSAGE, LENGTH, NB_ATTACHMEMTS, DATE, ID_USER, ID_SERVER)
                     VALUES ({message.id} , {len(message.content)}, {len(message.attachments)},STR_TO_DATE('{getTimeV2()}','%d-%m-%y %H:%i:%S'), {message.author.id}, {message.guild.id})""")

    def newSpam(self, message,nbrep,content):
        self.insert(f"""INSERT INTO `SPAM` (`ID_SPAM`, `NB_REP`, `CONTENT`, `DATE`, `ID_USER`, `ID_SERVER`)
                     VALUES ({message.id} , {nbrep}, '{self.clearQuotes(content)}', STR_TO_DATE('{getTimeV2()}','%d-%m-%y %H:%i:%S'), {message.author.id}, {message.guild.id})""")


    def checkCanJoinVoc(self,guild_id):
        result = self.select(f"SELECT CAN_JOIN_VOC FROM SERVER WHERE ID_SERVER = {guild_id}")
        return (result[0][0])

    def editCanJoinVoc(self,guild_id,statut):
        self.insert(f"UPDATE SERVER SET CAN_JOIN_VOC = {statut} WHERE ID_SERVER = {guild_id}")

    def deleteLastSpam(self, channel):
        self.insert(f"DELETE FROM LAST_SPAM WHERE ID_CHANNEL = {channel.id};")

    def saveSpamMessage(self,values):
        sql = "INSERT INTO LAST_SPAM (ID_SPAM, ID_CHANNEL, ID_MESSAGE) VALUES (%s ,%s, %s)"
        try:
            with self.db.cursor() as c:
                c.executemany(sql, values)
                self.db.commit()
            self.err_count = 0
        except mysql.connector.errors.OperationalError as err:
            self.err_count += 1
            if self.err_count <= 3:
                print("SQL Erreur :", err)
                self.disconnect()
                self.connect()
                self.saveSpamMessage(values)
            else:
                print("saveSpamMessage Stop")
                return False

    def getAllServer(self):
        if self.db != None:
            with self.db.cursor() as c:
                c.execute(f"SELECT ID_SERVER FROM SERVER")
                return c.fetchall()
        else:
            print("***** LA DB N'EST PAS CONNECTE *****\n"*3)
            return []

    def getLastSpam(self, channel):
        return self.select(f"SELECT LS.ID_SPAM ,LS.ID_MESSAGE, S.ID_USER FROM LAST_SPAM LS JOIN SPAM S ON LS.ID_SPAM = S.ID_SPAM WHERE LS.ID_CHANNEL = {channel.id};")
            
    def deleteUser_Server(self, guildID, userID):
        self.insert(f"DELETE FROM USER_SERVER WHERE ID_USER = {userID} AND ID_SERVER = {guildID}")

    def newSay_To(self,authorId,receiverId,message):
        self.insert(f"INSERT INTO `SAY_TO` (`AUTHOR`, `RECEIVER`, `DATE`, `MESSAGE`) VALUES ({authorId}, {receiverId}, STR_TO_DATE('{getTimeV2()}','%d-%m-%y %H:%i:%S'), '{message}')")
    
    def getSay_to(self,receiverId):
        result = self.select(f"SELECT AUTHOR FROM SAY_TO WHERE RECEIVER = {receiverId} ORDER BY DATE DESC LIMIT 1;")
        return result[0]

    def __del__(self):
        self.disconnect()
