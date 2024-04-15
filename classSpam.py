import re

class Spam:
    nbRep:int
    messageToSpam:str

    nbRepByMessage:int
    nbRepLastMessage:int
    nbMessageToSend:int = 5


    def strToInt(self,nbRep:str):
        """Transforme un str en chiffre en enlevant tout ce qui n'est pas un chiffre"""

        chiffre = re.sub(r'\D', '',nbRep)

        if (chiffre == ''):
            chiffre = '10'
        self.nbRep = int(chiffre)

    def cutMessage(self):
        """Coupe le message et renvoie un tableau avec le contenue et le nombre de repetition """

        #ajoute 2 espace apres les message dans le cas ou il n'y a pas d'espace pour que le split marche
        self.realMessage += '  '

        #coupe le message en 3 a chaque esapce 
        splited = self.realMessage.split(' ',2)

        self.messageToSpam = splited[2]
        self.strToInt(splited[1])

        #si le Message est vide
        if (self.messageToSpam == '' or self.messageToSpam.startswith(' ')):
            self.messageToSpam = "OUAIS OUAIS OUAIS"
        else:
            #enleve les suites d'espace 
            self.messageToSpam = self.messageToSpam.strip()

    def calculNbMess(self):
        """Calcul le nombre de messages à envoyé ainsi que le nombre de répétitions par message"""

        #Nombre de fois le message à spam par message envoyé
        self.nbRepByMessage = self.nbRep//5

        #Nombre de fois le message à spam pour le dernier message à envoyé
        self.nbRepLastMessage = self.nbRep%5

        #Nombre de caractères par message envoyé.
        nbChar = (len(self.messageToSpam)+1)*self.nbRepByMessage

        #ça je l'ai fait mais j'ai aucune idée comment ça marche 
        if (nbChar > 2000):
            self.nbRepByMessage = 2000 / int(len(self.messageToSpam)+1)
            self.nbRepByMessage=int(self.nbRepByMessage)
            totalRep = self.nbRepByMessage * 5

            while (self.nbRep - totalRep > self.nbRepByMessage):
                totalRep += self.nbRepByMessage
                self.nbMessageToSend += 1

            self.nbRepLastMessage = self.nbRep - totalRep

    def __init__(self,realMessage):
        self.realMessage = realMessage

        self.cutMessage()
        self.calculNbMess()