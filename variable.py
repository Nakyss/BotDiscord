#info connexion base de données
mydb = {
  'host' : "host",
  'user': "user",
  'password':"Password",
  'port':3306,
  'database':"bot_discord"
}

#possibilité de reponse au message finissant comme suivant:
possibilites = {
    "quoi": ["feur", "chi", "driceps","quoicoubeh"],
    "oui": ["stiti", "ghours"],
    "mere": ["méditérannée", "rie"],
    "mère": ["méditérannée", "rie"],
    "qoi": ["feur", "chi", "driceps","quoicoubeh"],
    "quois": ["feur", "chi", "driceps","quoicoubeh"],
    "koi": ["feur", "chi", "driceps","quoicoubeh"],
    "kois": ["feur", "chi", "driceps","quoicoubeh"],
    "qoa": ["feur", "chi", "driceps","quoicoubeh"],
    "kwoi": ["feur", "chi", "driceps","quoicoubeh"],
    "kwa": ["feur", "chi", "driceps","quoicoubeh"]
}

#tableau des messages à envoyé en message pv si on envoie un message au bot
pv_mess_possibilities = [
    "Ahoy! Les messages privés sont comme une boîte de chocolats, on sait jamais sur quoi on va tomber.",
    "Oh, un aventurier des messages privés! Quelle quête t'amène par ici?",
    "Hey toi! Les messages privés sont réservés aux VIP. T'as le laissez-passer?",
    "Ah, un explorateur des contrées secrètes! Que puis-je faire pour toi aujourd'hui?",
    "Hé ho, c'est un vol privé ici! Quelle est la destination de ton message?",
    "Bienvenue à bord du train des messages privés! Prochain arrêt : une conversation intéressante. Prêt à embarquer?",
    "Ah, la voie secrète des messages privés s'ouvre devant toi! Quel est ton mot de passe?"]


#liste des fonctionnalité du bot
helpmessage = '''
- Le bot peut spam un message dans un channel. Il suffit d'envoyer spam 10 messages pour qu'il envoie 10x "message"
- Enregistrement de certaines données pour avoir des stats, retrouvable sur https://nakyss.fr/
- Le bot peut joué des sons/ musiques 
- Le bot peut rejoindre à des moment aleatoire un channel vocal dans votre serveur et y jouer des sons choisis parmit une liste que vous gerer.
  - /enable_voc_join  Pour activer la fonctions
  - /disable_voc_join  Pour desactiver la fonctions
  - /list_sound  Affiche tout les sons disponible pour votre serveur
  - /add_sound   Ajouter un sons à la liste
  - /del_sound   supprime un son
  - /play  Joue un son, au choix parmit ceux proposé ou avec un lien youtube ou un titre de video, possibilité d'entrée le volume du média
  - /skip  Passe au son suivant dans le liste
  - /stop  Arrete la musique et deconnecte le bot
  - /display_queue  Affiche la musique actuellement joué et les suivante
'''

#definie le statue d'un channel pour empecher de spam 2 fois en même temps dans un channel
channel_status = {}

#definie le statue d'un serveur pour savoir si le random join à été declanché
guild_status = []

#definie la liste des music joué et leur serveur
musicQueue = {}

voiceClient = {}

#Liste des serveur ou le bot ne peut pas rejoindre le voc(evite de faire une requette BD à chaque fois que quelqu'un rejoint un vocal)
cantJoin = {}