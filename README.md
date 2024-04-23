# **Bot2Con**

Il s'agit d'un bot discord avec plusieurs options.

## Features
- **Spam**:
  - Envoyer un message sous la forme `spam 12 Hello World!`.
  - Le bot envera 12 fois `Hello Wordl!`.
  - Fonctionne tant que le message à envoyer ne depasse pas les 2000 caractères autorisé par Discord.
- **Stats**:
  -  Le bot enregistre quelle que infos tel que:
     - Le temps passé en vocal
     - La dernière connexion
     - Le nombres de messages envoyés
     - Le nombres de spam envoyés
  - Les stats sont accesibles sur le site web http://nakyss.fr/
- **Random Join**:
  - Le bot rejoint un canal vocal à des moment aleatoire si il y'a au moins une personnes connectée.
  - Il joue un son au hasard parmis les son du dossier `\botSound`, puis se deconnecte.
- **Play**:
  - Commande play pour lire un fichier audio du bot ou une le son du video youtube via un URL ou en tapant directement la recherche.
- **Say To**
  - Commande qui permet d'envoyer un message anonyme à quelqu'un via le bot, il a la possibilité de répondre mais ne sait pas a qui il parle.

## Language
- Python `bot`
- HTML, CSS, JS, PHP `Site Web`
- SQL `base de donnée`

## Installer le Bot

### Creation Base de données :
Nous utilisons une base de donnée MySql   

 - Crée une base de données avec un nom au choix
 - Exécutée le fichier `bd/bot_discord.sql` ou son contenue dans votre base de données



### Installation des librairies python
Nous utilisont plusieurs librairies installez les avec les commandes suivantes  
```
pip install discord.py
pip install python-dotenv
pip install pytz
pip install mutagen
python -m pip install mysql-connector-python
pip install yt-dlp
pip install youtube-search-python
````

### Configuration
Ouvrez le fichier `.env` et remplisser les variables avec les donnée pour votre bot

```
DISCORD_BOT_TOKEN=your_token
DISCORD_DB_HOST=your_db_host
DISCORD_DB_USER=your_db_username
DISCORD_DB_PASSWORD=your_db_password
DISCORD_DB_PORT=your_db_port
DISCORD_DB_DATABASE=your_database
```