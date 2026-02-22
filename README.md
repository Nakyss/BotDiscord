# **Bot2Con**

Il s'agit d'un bot discord avec plusieurs options.
> [!WARNING]  
> Le bot fonctionne toujours mais ce repo n'est plus maintenu et si le bot cesse de fonctionner, il ne sera plus mis à jour.

## Features
- **Spam**:
  - Envoyer un message sous la forme `spam 12 Hello World!`.
  - Le bot enverra 12 fois `Hello World!`.
  - Fonctionne tant que le message à envoyer ne dépasse pas les 2000 caractères autorisés par Discord.
- **Stats**:
  -  Le bot enregistre quelques infos telles que:
     - Le temps passé en vocal
     - La dernière connexion
     - Le nombre de messages envoyés
     - Le nombre de spam envoyés
  - Les stats sont accessibles sur le site web https://nakyss.fr/
- **Random Join**:
  - Le bot rejoint un canal vocal à des moments aléatoires s'il y a au moins une personne connectée.
  - Il joue un son au hasard parmi les sons du dossier `\botSound`, puis se déconnecte.
- **Play**:
  - Commande play pour lire un fichier audio du bot ou le son de la vidéo youtube via un URL ou en tapant directement la recherche.
- **Say To**
  - Commande qui permet d'envoyer un message anonyme à quelqu'un via le bot, il a la possibilité de répondre mais ne sait pas a qui il parle.

## Language
- Python `bot`
- HTML, CSS, JS, PHP `Site Web`
- SQL `base de données`

## Installer le Bot

### Création Base de données :
Nous utilisons une base de données MySql   

 - Créez une base de données avec un nom au choix
 - Exécutez le fichier `bd/bot_discord.sql` ou son contenu dans votre base de données



### Installation des librairies python
Nous utilisons plusieurs librairies, installez-les avec la commande suivante  
```
pip install -r requirements.txt
````

### Configuration
Ouvrez le fichier `.env` et remplissez les variables avec les données pour votre bot

```
DISCORD_BOT_TOKEN=your_token
DISCORD_DB_HOST=your_db_host
DISCORD_DB_USER=your_db_username
DISCORD_DB_PASSWORD=your_db_password
DISCORD_DB_PORT=your_db_port
DISCORD_DB_DATABASE=your_database
#path to the bot pp
DISCORD_BOT_PP_PATH=pp/bot2con.jpg
```
