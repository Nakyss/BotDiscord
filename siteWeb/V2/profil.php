<?php
if (htmlspecialchars($_GET['id']) ) {
    $id = $_GET['id'];
    $db = new PDO('mysql:host=host;dbname=bot_discord;charset=utf8;port=3306', 'username', 'password');
    $sql = "SELECT NAME_GLOBAL FROM USER WHERE ID_USER = :id";
    $result = $db->prepare($sql);
    $result->bindParam(':id', $id, PDO::PARAM_INT);                   
    $result->execute();
    $name = $result->fetchAll();

    $sql = "SELECT SUM(TIME_VOC) as TIME FROM `VOCAL_SESSION` WHERE ID_USER = :id";
    $result = $db->prepare($sql);
    $result->bindParam(':id', $id, PDO::PARAM_INT);                 
    $result->execute();
    $totalTime = $result->fetchAll();

    $sql = "SELECT COUNT(*) FROM `MESSAGE` WHERE ID_USER = :id";
    $result = $db->prepare($sql);
    $result->bindParam(':id', $id, PDO::PARAM_INT);
    $result->execute();
    $nbMessages = $result->fetch(PDO::FETCH_COLUMN);

    $sql = "SELECT SUM(NB_REP) FROM `SPAM` WHERE ID_USER = :id";
    $result = $db->prepare($sql);
    $result->bindParam(':id', $id, PDO::PARAM_INT);
    $result->execute();
    $nbSpam = $result->fetch(PDO::FETCH_COLUMN);
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


?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot2con - <?php echo $name[0]['NAME_GLOBAL'];?></title>
    <link rel="icon" href="favicon.ico">
    <link rel="stylesheet" href="profilStyle.css">
</head>
<body>
    <h1><?php echo $name[0]['NAME_GLOBAL'];?></h1>
    <h2>temps total en voc : <?php echo formatTotalTime($totalTime[0]['TIME'])?></h2>
    <h2>Nb total de messages envoyés : <?php echo $nbMessages?></h2>
    <h2>Nb de spam envoyés : <?php echo $nbSpam?></h2>
</body>
</html>