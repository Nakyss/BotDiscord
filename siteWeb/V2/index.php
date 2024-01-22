<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];

if (preg_match('/(android|iphone|ipad)/i', $userAgent)) {
    header('Location: mobile');
    exit();
}
?>
<?php
$db = new PDO('mysql:host=host;dbname=bot_discord;charset=utf8;port=3306', 'username', 'password');
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
        <ul id="userList">
        <?php
        $sql = "SELECT U.ID_USER, U.NAME_GLOBAL, U.PP_URL, COUNT(M.ID_MESSAGE) AS NbMessage FROM USER U JOIN MESSAGE M ON U.ID_USER = M.ID_USER GROUP BY U.ID_USER, U.NAME_GLOBAL, U.PP_URL ORDER BY NbMessage DESC";
        $result = $db->prepare($sql);                 
        $result->execute();
        $users = $result->fetchALl();
        foreach ($users as $user) 
        {
            ?>
                <li>
                    <img src="<?php echo $user['PP_URL']; ?>" alt="Photo de profil de <?php echo $user['NAME_GLOBAL']; ?>">
                    <a href="profil?id=<?php echo $user['ID_USER']; ?>"><?php echo $user['NAME_GLOBAL']; ?></a>
                </li>
            <?php
        }
        ?>
        </ul>
    </nav>

    <div id="textHere">
        <h2>Cliquer sur un profil <br> pour avoir les stats</h2>
    </div>
    
</body>
</html>
