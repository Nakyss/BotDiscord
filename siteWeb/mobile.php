<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];

if (!preg_match('/(android|iphone|ipad)/i', $userAgent) && !preg_match('/(mobile)/i', $userAgent)) {
    header('Location: http://nakyss.fr/');
    exit();
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="mstyle.css">
    <title>Bot2con</title>
</head>
<body>
    <header>
        <div id="infoHeader"class="info-Header">
            <div id="divHess">
                <h1>Bot 2 Con - Stats</h1>
                <a target="_blank" href="https://discord.com/api/oauth2/authorize?client_id=1185657302603280395&permissions=2181164096&scope=bot">Cliquer ici pour ajouter le bot a votre serveur</a>
            </div>
        </div>
        
        <img id="menu" src="img/menu.svg" alt="bouton pour alterner entre la liste d'utilisateur et les stats">
        
    </header>
    
    <ul id="userList"></ul>

    
    <div id="textHere">
        <h2>Cliquer sur un profil pour voir les stats</h2>
    </div>
    

    <div id="userDetails" class="user-details"></div>

    <script>
        const userListElement = document.getElementById("userList");
        const userDetailsElement = document.getElementById("userDetails");
        const infoHeaderElement = document.getElementById("infoHeader");

        // Fonction pour afficher les détails de l'utilisateur
        function editHeader(user){

            if (user == 0){
                infoHeaderElement.innerHTML = `
                <div id="divHess">
                    <h1>Bot 2 Con - Stats</h1>
                    <a target="_blank" href="https://discord.com/api/oauth2/authorize?client_id=1185657302603280395&permissions=2181164096&scope=bot">Cliquer ici pour ajouter le bot a votre serveur</a>
                </div>
                `;
            }
            else{
                infoHeaderElement.innerHTML = `
                <img src="${user.urlPP}" alt="photo de profil de ${user.name}">
                <h2 id="userName">${user.name} </h2>
                `;
            }
        }


        function showUserDetails(user) {


            userDetailsElement.innerHTML = `
            <div class="table">
                <div class="derniere_connexion">
                    <div class="categorylt">
                        <h3 class="empty"></h3>
                        <h3 class="full">Dernière connexion</h3>
                    </div>
                
                ${user.lastJoinAll && Array.isArray(user.lastJoinAll) ? user.lastJoinAll.map((lastJoin) => `
                    <div class="donnee">
                        <div class="left" id="serv1"><p>${user.server.find(server => server.idServ === lastJoin.idServ) ? user.server.find(server => server.idServ === lastJoin.idServ).nameServ : ''}</p></div>
                        <div class="right" id="d1"><p>${calculateTimeDifference(lastJoin.lastJoin)}</p></div>
                    </div>
                `).join('') : ''}
                </div>

                <div class="temps_en_voc">
                    <div class="categoryrt">
                        <h3 class="full">Temps en Voc</h3>
                        <h3 class="empty"></h3>
                    </div>
                
                ${user.totalTimeAll && Array.isArray(user.totalTimeAll) ? user.totalTimeAll.map((totalTime) => `
                    <div class="donnee">
                        <div class="left" id="d2"><p>${formatTotalTime(totalTime.totalTime)}</p></div>
                        <div class="right" id="serv2"><p>${user.server.find(server => server.idServ === totalTime.idServ) ? user.server.find(server => server.idServ === totalTime.idServ).nameServ : ''}</p></div>
                    </div>
                `).join('') : ''}
                </div>

                <div class="nb_messages">
                    <div class="categorylt">
                        <h3 class="empty"></h3>
                        <h3 class="full">Nb messages</h3>
                    </div>
                    
                
                ${user.nbMessage && Array.isArray(user.nbMessage) ? user.nbMessage.map((nbMessage) => `
                    <div class="donnee">
                        <div class="left" id="serv3"><p>${user.server.find(server => server.idServ === nbMessage.idServ) ? user.server.find(server => server.idServ === nbMessage.idServ).nameServ : ''}</p></div>
                        <div class="right" id="d3"><p>${nbMessage.nbMessage}</p></div>
                    </div>
                `).join('') : ''}
                </div>

                <div class="nb_spam">
                    <div class="categoryrt">
                        <h3 class="full">Nb Spam</h3>
                        <h3 class="empty"></h3>
                    </div>
                
                ${user.nbSpamAll && Array.isArray(user.nbSpamAll) ? user.nbSpamAll.map((nbSpam) => `
                    <div class="donnee">
                        <div class="left" id="d4"><p>${nbSpam.nbSpam}</p></div>
                        <div class="right" id="serv4"><p>${user.server.find(server => server.idServ === nbSpam.idServ) ? user.server.find(server => server.idServ === nbSpam.idServ).nameServ : ''}</p></div>
                    </div>
                `).join('') : ''}
                </div>
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
                    let menu = document.getElementById("menu");
                    
                    // Ajoute un événement de clic pour afficher les détails lorsqu'un utilisateur est sélectionné
                    liElement.addEventListener("click", () => {
                        menu.style.display ="block"
                        userDetails.style.display = "block";
                        userListElement.style.display = "none";
                        
                        showUserDetails(user);
                        editHeader(user);
                        
                        menu.addEventListener("click", () => {
                            menu.style.display ="none"
                            userDetails.style.display ="none";
                            editHeader(0);
                            userListElement.style.display = "block";
                        });
                    });

                    userListElement.appendChild(liElement);
                }
            });
    </script>
</body>
</html>