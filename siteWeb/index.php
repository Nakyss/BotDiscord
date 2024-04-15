<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];

if (preg_match('/(android|iphone|ipad)/i', $userAgent)) {
    header('Location: https://nakyss.fr/mobile');
    exit();
}
?>
<?php
$db = new PDO('mysql:host=host;dbname=bot_discord;charset=utf8;port=3600', 'user', 'passwd');
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot2con</title>
    <link rel="stylesheet" href="style.css">
    <link rel="alternate" media="only screen and (max-width: 640px)"  href="https://nakyss.fr/mobile/">
    <link rel="canonical" href="https://nakyss.fr/" />

    <link rel="apple-touch-icon" sizes="57x57" href="https://nakyss.fr/icon/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="https://nakyss.fr/icon/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="https://nakyss.fr/icon/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="https://nakyss.fr/icon/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="https://nakyss.fr/icon/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="https://nakyss.fr/icon/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="https://nakyss.fr/icon/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="https://nakyss.fr/icon/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="https://nakyss.fr/icon/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="https://nakyss.fr/icon/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://nakyss.fr/icon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="https://nakyss.fr/icon/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://nakyss.fr/icon/favicon-16x16.png">
    <link rel="manifest" href="https://nakyss.fr/icon/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="https://nakyss.fr/icon/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">

</head>
<body>
    <nav id="list">
        <div id="header">
            <h1>Stats Utilisateurs Discord</h1>
            <a target="_blank" href="https://discord.com/api/oauth2/authorize?client_id=1185657302603280395&permissions=2181164096&scope=bot">Cliquer ici pour ajouter le bot a votre serveur</a>
        </div>
        <ul id="userList">
        <?php
        $sql = 'SELECT U.ID_USER, U.NAME_GLOBAL, U.PP_URL,
        ((SELECT COALESCE(COUNT(*), 0) FROM MESSAGE M JOIN SERVER S ON M.ID_SERVER = S.ID_SERVER WHERE M.ID_USER = U.ID_USER AND S.STATUS = 1)*350+
        (SELECT COALESCE(SUM(VC.TIME_VOC), 0) FROM VOCAL_SESSION VC JOIN SERVER S ON VC.ID_SERVER = S.ID_SERVER WHERE VC.ID_USER = U.ID_USER AND S.STATUS = 1)+
        (SELECT COALESCE(SUM(S.NB_REP), 0) FROM SPAM S JOIN SERVER SE ON SE.ID_SERVER = S.ID_SERVER WHERE S.ID_USER = U.ID_USER AND SE.STATUS = 1)*3) as result
        FROM USER U 
        ORDER BY result DESC;';
        $result = $db->prepare($sql);                 
        $result->execute();
        $users = $result->fetchALl();
        foreach ($users as $user) 
        {?>
        
            <li>
                <img src="<?php echo $user['PP_URL']; ?>" alt="Photo de profil de <?php echo $user['NAME_GLOBAL']; ?>">
                <a href="https://nakyss.fr/profil?id=<?php echo $user['ID_USER']; ?>"><?php echo $user['NAME_GLOBAL']; ?></a>
            </li>

            <?php
        }?>
        </ul>
    </nav>

    <div id="textHere">
        <h2>Cliquer sur un profil <br> pour avoir les stats</h2>
    </div>
    
</body>
</html>
