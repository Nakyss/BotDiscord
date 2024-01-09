<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];

if (preg_match('/(android|iphone|ipad)/i', $userAgent)) {
    header('Location: mobile.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot2con</title>
    <link rel="icon" href="favicon.ico">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav id="list">
        <div id="header">
            <h1>Stats Utilisateurs Discord</h1>
            <a target="_blank" href="https://discord.com/api/oauth2/authorize?client_id=1185657302603280395&permissions=2181164096&scope=bot">Cliquer ici pour ajouter le bot a votre serveur</a>
        </div>
        <ul id="userList"></ul>
    </nav>

    <div id="textHere">
        <h2>Cliquer sur un profil <br> pour avoir les stats</h2>
    </div>
    <div id="userDetails" class="user-details"></div>

    <script>
        const userListElement = document.getElementById("userList");
        const userDetailsElement = document.getElementById("userDetails");

        // Fonction pour afficher les détails de l'utilisateur
        function showUserDetails(user) {

            userDetailsElement.innerHTML = `
             <p id="id">id : ${user.id}</p>
                <div class="top">
                    <h2 id="userName">${user.name} </h2>
                    <img src="${user.urlPP}" alt="photo de profil de ${user.name}">
                </div>
                
                <div class="table">
                    <div class="headtab">
                        <div class ="serveur"><h3>Serveur</h3></div>
                        <div class ="derniere_connexion"><h3>Dernière connexion</h3></div>
                        <div class ="temps_en_voc" id="voctime"><h3>Temps en Voc</h3>
                            ${user.lastQuitAll && user.lastQuitAll.length > 0 && user.lastQuitAll[0].lastQuit < user.lastJoinAll[0].lastJoin?
                                `<p id="lastMaj">Dernière mise à jour il y a : ${calculateTimeDifference(user.lastJoinAll[0].lastJoin)}</p></div>` :
                                `</div>`}
                        <div class ="nb_messages"><h3>Nb messages</h3></div>
                        <div class="nb_spam"><h3>Nb Spam</h3></div>
                    </div>
                    ${user.server && Array.isArray(user.server) ? user.server.map((server) => `
                        <div class="maintab">
                            <div class ="serveur"><p>${server.nameServ}</p></div>
                            <div class ="derniere_connexion"><p>${user.lastJoinAll.find(last => last.idServ === server.idServ) ? calculateTimeDifference(user.lastJoinAll.find(last => last.idServ === server.idServ).lastJoin) : ''}</p></div>
                            <div class ="temps_en_voc"><p>${user.totalTimeAll.find(total => total.idServ === server.idServ) ? formatTotalTime(user.totalTimeAll.find(total => total.idServ === server.idServ).totalTime) : ''}</p></div>
                            <div class ="nb_messages"><p>${user.nbMessage.find(message => message.idServ === server.idServ) ? user.nbMessage.find(message => message.idServ === server.idServ).nbMessage : ''}</p></div>
                            <div class="nb_spam"><p>${user.nbSpamAll.find(spam => spam.idServ === server.idServ) ? user.nbSpamAll.find(spam => spam.idServ === server.idServ).nbSpam : ''}</p></div>
                        </div>
                    `).join('') : ''}
                </div>
                
            `;
        }

        // Fonction pour calculer la différence de temps
        function calculateTimeDifference(timestamp) {
            const now = Math.floor(Date.now() / 1000);
            const difference = now - timestamp;
            const seconds = difference % 60;
            const minutes = Math.floor(difference / 60) % 60;
            const hours = Math.floor(difference / 3600) % 24;
            const days = Math.floor(difference / (3600 * 24));

            if (days > 0) {
                return `${days} jours`;
            } else if (hours > 0) {
                return `${hours} heures`;
            } else if (minutes > 0) {
                return `${minutes} minutes`;
            } else {
                return `${seconds} secondes`;
            }
        }

        // Fonction pour formater le temps total en jours, heures, minutes et secondes
        function formatTotalTime(totalTime) {
            const days = Math.floor(totalTime / (3600 * 24));
            const hours = Math.floor((totalTime % (3600 * 24)) / 3600);
            const minutes = Math.floor((totalTime % 3600) / 60);
            const seconds = totalTime % 60;

            let result = '';
            if (days > 0) {
                result += `${days}j `;
            }
            if (hours > 0) {
                result += `${hours}h `;
            }
            if (minutes > 0) {
                result += `${minutes}m `;
            }
            if (seconds > 0) {
                result += `${seconds}s`;
            }

            return result.trim();
        }

        fetch("../userTime.json")
            .then(response => response.json())
            .then((users) => {
                for (const user of users['users']) {
                    const liElement = document.createElement("li");
                    liElement.innerHTML = `<img src="${user.urlPP}" alt="photo de profil de ${user.name}">${user.name}`;

                    
                    let userDetails = document.getElementById("userDetails");
                    let textHere = document.getElementById("textHere");
                    let list = document.getElementById("list");
                    const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
                    // Ajoute un événement de clic pour afficher les détails lorsqu'un utilisateur est sélectionné
                    liElement.addEventListener("click", () => {
                        if(getComputedStyle(userDetails).display != "flex"){
                           userDetails.style.display = "flex";
                           textHere.style.display = "none";
                           if (width <= 850){
                            list.style.display = "none";
                        }
                        }
                        
                        showUserDetails(user);
                        let userName = document.getElementById("userName");
                        userName.addEventListener("click", () => {
                            if(getComputedStyle(list).display != "block"){
                                list.style.display ="block";
                                userDetails.style.display = "none";
                            }
                        });
                    });

                    userListElement.appendChild(liElement);
                }
            });
    </script>
</body>
</html>
