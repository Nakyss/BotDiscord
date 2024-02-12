<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];


if (htmlspecialchars($_GET['id']) ) {
    $id = $_GET['id'];
    $db = new PDO('mysql:host=db-mysql-lon1-67456-do-user-15430802-0.c.db.ondigitalocean.com;dbname=bot_discord;charset=utf8;port=25060', 'doadmin', 'AVNS_SVdKyuKLbVWmp12oIHE');
    $sql = "SELECT NAME_GLOBAL FROM USER WHERE ID_USER = :id";
    $result = $db->prepare($sql);
    $result->bindParam(':id', $id, PDO::PARAM_INT);                   
    $result->execute();
    if($result->rowCount() == 0 ){
        header('Location: https://nakyss.fr/');
        exit();
    }
    $name = $result->fetchAll();
}
else{
    header('Location: https://nakyss.fr/');
    exit();
}

if (preg_match('/(android|iphone|ipad)/i', $userAgent)) {
    header('Location: https://nakyss.fr/mobile/profil?id='.$id);
    exit();
}

function formatTotalTime($totalTime) {
    $days = floor($totalTime / (3600 * 24));
    $hours = floor(($totalTime % (3600 * 24)) / 3600);
    $minutes = floor(($totalTime % 3600) / 60);
    $seconds = $totalTime % 60;

    $result = '';
    if ($days > 0) {
        $result .= $days . 'j ';
    }
    if ($hours > 0) {
        $result .= $hours . 'h ';
    }
    if ($minutes > 0) {
        $result .= $minutes . 'm ';
    }
    if ($seconds > 0) {
        $result .= $seconds . 's';
    }

    return trim($result);
}

function calculateTimeDifference($timestamp) {
    if ($timestamp == NULL){
        return '';
    }
    $now = time();
    $difference = $now - $timestamp;
    $seconds = $difference % 60;
    $minutes = floor($difference / 60) % 60;
    $hours = floor($difference / 3600) % 24;
    $days = floor($difference / (3600 * 24));

    if ($days > 0) {
        return $days . ' jours';
    } elseif ($hours > 0) {
        return $hours . ' heures';
    } elseif ($minutes > 0) {
        return $minutes . ' minutes';
    } else {
        return $seconds . ' secondes';
    }
}


?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot2con - <?php echo $name[0]['NAME_GLOBAL'];?></title>
    <link rel="stylesheet" href="profilStyle.css">
    <link rel="alternate" media="only screen and (max-width: 640px)"  href="https://nakyss.fr/mobile/profil">
    <link rel="canonical" href="https://nakyss.fr/profil" />

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
        $sql = "SELECT U.ID_USER, U.NAME_GLOBAL, U.PP_URL, COUNT(M.ID_MESSAGE) AS NbMessage FROM USER U JOIN MESSAGE M ON U.ID_USER = M.ID_USER JOIN SERVER S ON M.ID_SERVER = S.ID_SERVER WHERE S.STATUS = 1 GROUP BY U.ID_USER, U.NAME_GLOBAL, U.PP_URL ORDER BY NbMessage DESC";
        $result = $db->prepare($sql);                 
        $result->execute();
        $users = $result->fetchALl();
        foreach ($users as $user) 
        {?>
        
            <li>
                <img src="<?php echo $user['PP_URL']; ?>" alt="Photo de profil de <?php echo $user['NAME_GLOBAL']; ?>">
                <a href="profil?id=<?php echo $user['ID_USER']; ?>"><?php echo $user['NAME_GLOBAL']; ?></a>
            </li>

            <?php
        }?>
        </ul>
    </nav>
    
    <?php
        $sql = "SELECT NAME_GLOBAL, PP_URL  FROM USER WHERE ID_USER = :id";
        $result = $db->prepare($sql);                 
        $result->bindParam(':id', $id, PDO::PARAM_INT);  
        $result->execute();
        $actualleUser = $result->fetchALl();
    ?>

    <div id="userDetails" class="user-details">
        <div class="top">
            <h2 id="userName"><?php echo $actualleUser[0]['NAME_GLOBAL']; ?> </h2>
            <img src="<?php echo $actualleUser[0]['PP_URL']; ?>" alt="Photo de profil de <?php echo $actualleUser[0]['NAME_GLOBAL']; ?>">
        </div>
                
        <div class="table">
            <div class="headtab">
                <div class ="serveur"><h3>Serveur</h3></div>
                <div class ="derniere_connexion"><h3>Dernière connexion</h3></div>
                <div class ="temps_en_voc" id="voctime"><h3>Temps en Voc</h3></div>
                <div class ="nb_messages"><h3>Nb messages</h3></div>
                <div class="nb_spam"><h3>Nb Spam</h3></div>
            </div>
            <?php
            $sql = "SELECT S.NAME, S.ID_SERVER, SUM(VC.TIME_VOC) AS TIME FROM USER_SERVER U JOIN SERVER S ON U.ID_SERVER = S.ID_SERVER LEFT JOIN VOCAL_SESSION VC ON U.ID_SERVER = VC.ID_SERVER AND U.ID_USER = VC.ID_USER WHERE U.ID_USER = :id AND S.STATUS = 1 GROUP BY S.NAME, S.ID_SERVER ORDER BY TIME DESC;";
            $result = $db->prepare($sql);
            $result->bindParam(':id', $id, PDO::PARAM_INT);                 
            $result->execute();
            $servers = $result->fetchALl();
            foreach ($servers as $server) 
            {
                $sql = "SELECT (SELECT SUM(TIME_VOC) FROM VOCAL_SESSION WHERE ID_USER = :id AND ID_SERVER = :ids) as TIME, (SELECT COUNT(*) FROM MESSAGE WHERE ID_USER = :id AND ID_SERVER = :ids) as MESSAGE_COUNT, (SELECT SUM(NB_REP) FROM SPAM WHERE ID_USER = :id AND ID_SERVER = :ids) as NB_REP_SUM, (SELECT `JOIN` FROM VOCAL_SESSION WHERE ID_USER = :id AND ID_SERVER = :ids ORDER BY `JOIN` DESC LIMIT 1) as LATEST_JOIN ORDER BY TIME DESC";
                $result = $db->prepare($sql);
                $result->bindParam(':id', $id, PDO::PARAM_INT);
                $result->bindParam(':ids', $server['ID_SERVER'], PDO::PARAM_INT);                    
                $result->execute();
                $info = $result->fetchALl();?>
            
            <div class="maintab">
                <div class ="serveur"><p><?php echo $server['NAME'] ?></p></div>
                <div class ="derniere_connexion"><p><?php echo calculateTimeDifference($info[0]['LATEST_JOIN'])?></p></div>
                <div class ="temps_en_voc"><p><?php echo formatTotalTime($info[0]['TIME'])?></p></div>
                <div class ="nb_messages"><p><?php echo $info[0]['MESSAGE_COUNT'] ?></p></div>
                <div class="nb_spam"><p><?php echo $info[0]['NB_REP_SUM'] ?></p></div>
            </div>
            
            <?php
            }?>
            
        </div>
    </div>

    
</body>
</html>