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

## Language
- Python `bot`
- HTML, CSS, JS, PHP `Site Web`

##Info

Les donnée son actuellement stockées dans un fichier JSON pour des raison douteuse
Migration vers un systeme de base de données quand j'aurais le temps et la deter

Peut être des amelioration pour que le code soit plus "flexible" et facilement adaptable 

Ajout de commentaire 

Optimisation
