<?php
require_once('common.inc.php');
$offset = 0;
$count = 10000;
set_time_limit(0);
$messages = array();

$sql = 'SELECT messages.* FROM messages WHERE JSON_CONTAINS_PATH(message_data, \'one\', \'$.attributes\') LIMIT '.$offset.','.$count;
$res = $link->query($sql) or die('Query error: '.$link->errno.' '.$link->error.'<br>');
if($res->num_rows>0){
    while($dat = $res->fetch_assoc()){
        $dat['message_data'] = json_decode($dat['message_data'],true);
        $messages[$dat['message_id']] = $dat;
    }
}

function findfirst($needle,$haystack,$offset=0){
    foreach($haystack as $k=>$v){
        if($k<=$offset){
            continue;
        }
        if($needle == $v['message_data']['attributes']['message']){
            return $k;
        }
    }
    return false;
}

$jsondata = file_get_contents("migrationdata.json");
$data = json_decode($jsondata,true);
$lastid = 0;
foreach($data as $k=>$v){
    $message_id = findfirst($v['message'],$messages,$lastid);

    if($message_id!==false){
        $lastid = $message_id;
        //echo 'Found ID: '.$message_id.' for ('.$k.') &quot;'.$v['message'].'&quot;<br>';
        $messages[$message_id]['new']=$v;
    } else {
        echo '<span style="color:red; font-weight:bold;">Could not find ID for ('.$k.') &quot;'.$v['message'].'&quot;</span><br>';
    }
}

$i = 0;
$max = 100;
foreach($messages as $k=>$v){
    if($i>$max)
        break;
    if(isset($v['new'])){
        echo '<strong>';
    }
    echo $v['message_data']['attributes']['from'] .': '. $v['message_data']['attributes']['message'];
    if(isset($v['new'])){
        echo ' -> '. $v['new']['message'].'</strong>';
    }
    echo '<br>';
    $i++;

}

echo '<hr>';

foreach($messages as $k=>$v){
    if(isset($v['new'])){
        $sql = 'UPDATE messages SET message_data = \''.$link->real_escape_string(json_encode($v['new'])).'\' WHERE message_id = \''.$k.'\'';
        $res = $link->query($sql) or die('Query error: '.$link->errno.' '.$link->error.'<br>');
        if($res){
            echo 'Updated data for: '.$k.'<br>';
        } else {
            echo '<span style="color:red; font-weight:bold;">Could not update data for: '.$k.'</span><br>';
        }
    }
}

?>