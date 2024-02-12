<?php
$userAgent = $_SERVER['HTTP_USER_AGENT'];

if (htmlspecialchars($_GET['id']) ) {
    $id = $_GET['id'];
    $db = new PDO('mysql:host=db-mysql-lon1-67456-do-user-15430802-0.c.db.ondigitalocean.com;dbname=bot_discord;charset=utf8;port=25060', 'doadmin', 'AVNS_SVdKyuKLbVWmp12oIHE');
    $sql = "SELECT NAME_GLOBAL, PP_URL  FROM USER WHERE ID_USER = :id";
    $result = $db->prepare($sql);                 
    $result->bindParam(':id', $id, PDO::PARAM_INT);  
    $result->execute();
    if($result->rowCount() == 0 ){
        header('Location: https://nakyss.fr/mobile');
        exit();
    }
    $actualleUser = $result->fetchALl();
}
else{
    header('Location: https://nakyss.fr/mobile');
    exit();
}


if (!preg_match('/(android|iphone|ipad)/i', $userAgent) && !preg_match('/(mobile)/i', $userAgent)) {
    header('Location: https://nakyss.fr/profil?id='.$id);
    exit();
}

?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="profil.css">
    <title>Bot2con - <?php echo $actualleUser[0]['NAME_GLOBAL'];?></title>
    <link rel="canonical" href="https://nakyss.fr/mobile/profil" />

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
    <header>
        <div id="infoHeader"class="info-Header">
            <img src="<?php echo $actualleUser[0]['PP_URL']; ?>" alt="Photo de profil de <?php echo $actualleUser[0]['NAME_GLOBAL']; ?>">
            <h2 id="userName"><?php echo $actualleUser[0]['NAME_GLOBAL']; ?></h2>
        </div>
        
        <a href="https://nakyss.fr/mobile"><img id="menu" src="menu.svg" alt="bouton pour alterner entre la liste d'utilisateur et les stats"></a>
        
    </header>

    <?php
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


    
    <div id="userDetails" class="user-details">
        <div class="table">
            <div class="derniere_connexion">
                <div class="categorylt">
                    <h3 class="empty"></h3>
                    <h3 class="full">Dernière connexion</h3>
                </div>
                <?php 
                $sql = "SELECT S.NAME, S.ID_SERVER FROM SERVER S JOIN USER_SERVER US ON S.ID_SERVER = US.ID_SERVER WHERE S.STATUS = 1 AND US.ID_USER = :id";
                $result = $db->prepare($sql);
                $result->bindParam(':id', $id, PDO::PARAM_INT);                     
                $result->execute();
                $servers = $result->fetchALl();
                foreach ($servers as $server) 
                {
                    $sql = "SELECT `JOIN` FROM VOCAL_SESSION WHERE ID_SERVER = :ids AND ID_USER = :id ORDER BY `JOIN` DESC LIMIT 1";
                    $result = $db->prepare($sql);
                    $result->bindParam(':id', $id, PDO::PARAM_INT);
                    $result->bindParam(':ids', $server['ID_SERVER'], PDO::PARAM_INT);                      
                    $result->execute();
                    if ($result->rowCount() != 0){
                        $join = $result->fetchAll();
                    ?>
                    <div class="donnee">
                        <div class="left" id="serv1"><p><?php echo $server['NAME'] ?></p></div>
                        <div class="right" id="d1"><p>Il y a <?php echo calculateTimeDifference($join[0]['JOIN'])?></p></div>
                    </div>
                    <?php 
                    }
                } ?>
            </div>
            <div class="temps_en_voc">
                    <div class="categoryrt">
                        <h3 class="full">Temps en Voc</h3>
                        <h3 class="empty"></h3>
                    </div>
                    <?php 
                foreach ($servers as $server) 
                {
                    $sql = "SELECT SUM(TIME_VOC) as TIME FROM VOCAL_SESSION WHERE ID_SERVER = :ids AND ID_USER = :id";
                    $result = $db->prepare($sql);
                    $result->bindParam(':id', $id, PDO::PARAM_INT);
                    $result->bindParam(':ids', $server['ID_SERVER'], PDO::PARAM_INT);                      
                    $result->execute();
                    $time = $result->fetchAll();
                    if ($time[0]['TIME'] != NULL){
                    ?>
                    <div class="donnee">
                        <div class="left" id="d2"><p><?php echo formatTotalTime($time[0]['TIME'])?></p></div>
                        <div class="right" id="serv2"><p><?php echo $server['NAME'] ?></p></div>
                    </div>
                    <?php 
                    }
                } ?>
            </div>
            <div class="nb_messages">
                    <div class="categorylt">
                        <h3 class="empty"></h3>
                        <h3 class="full">Nb messages</h3>
                    </div>
                    <?php 
                foreach ($servers as $server) 
                {
                    $sql = "SELECT COUNT(*) as MESS FROM MESSAGE WHERE ID_USER = :id AND ID_SERVER = :ids";
                    $result = $db->prepare($sql);
                    $result->bindParam(':id', $id, PDO::PARAM_INT);
                    $result->bindParam(':ids', $server['ID_SERVER'], PDO::PARAM_INT);                      
                    $result->execute();
                    $mess = $result->fetchAll();
                    if ($mess[0]['MESS'] != NULL){
                    ?>
                    <div class="donnee">
                        <div class="left" id="serv3"><p><?php echo $server['NAME'] ?></p></div>
                        <div class="right" id="d3"><p><?php echo $mess[0]['MESS'] ?></p></div>
                    </div>
                    <?php 
                    }
                } ?>
            </div>
            <div class="nb_spam">
                    <div class="categoryrt">
                        <h3 class="full">Nb Spam</h3>
                        <h3 class="empty"></h3>
                    </div>
                    <?php 
                foreach ($servers as $server) 
                {
                    $sql = "SELECT SUM(NB_REP) as SPAM FROM SPAM WHERE ID_USER = :id AND ID_SERVER = :ids";
                    $result = $db->prepare($sql);
                    $result->bindParam(':id', $id, PDO::PARAM_INT);
                    $result->bindParam(':ids', $server['ID_SERVER'], PDO::PARAM_INT);                      
                    $result->execute();
                    $spam = $result->fetchAll();
                    if ($spam[0]['SPAM'] != NULL){
                    ?>
                    <div class="donnee">
                        <div class="left" id="d4"><p><?php echo $spam[0]['SPAM'] ?></p></div>
                        <div class="right" id="serv4"><p><?php echo $server['NAME'] ?></p></div>
                    </div>

                    <?php 
                    }
                } ?>
            </div>
        </div>
    </div>
</body>
</html>