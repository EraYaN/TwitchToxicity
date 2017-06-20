<?php
session_start();
if(empty($_SESSION['loggedin'])){
	$_SESSION['loggedin'] = false;
}
if(!$_SESSION['loggedin']){
	header('HTTP/1.0 403 Forbidden');
	die("{'msg':'Forbidden'}");
}

require_once('common.inc.php');
$response = array(
	'danger'=>'',
	'warning'=>'',
	'success'=>'',
	'info'=>'',
	'result'=>false,
	'data' => array()
	);
if(!empty($_GET['get_messages'])){
	$count = intval($_POST['count']);
    $context = intval($_POST['context']);
	if($count>0){
		//TODO context?

        $sql = 'SELECT message_id FROM messages WHERE not exists (select null from classifications where classifications.message_id = messages.message_id) LIMIT 1;';
        $res = $link->query($sql) or $response['danger'] .= 'Query error: '.$link->errno.' '.$link->error.'<br>';
		if($res->num_rows>0){
            $dat = $res->fetch_assoc();
            $starting_id = $dat['message_id'];

            $sql = 'SELECT messages.*,
            COUNT(classification_id) as num_classifications,
            GROUP_CONCAT(SUBSTR(users.username,1,1) separator \',\') as users,
            (SELECT classification FROM classifications WHERE classifications.message_id = messages.message_id AND user_id = '.$_SESSION['user_id'].' LIMIT 1) as classification
            FROM messages
            LEFT JOIN (classifications
                LEFT JOIN (users) USING (user_id)
            ) USING (message_id)
            WHERE message_id >= '.max(1,$starting_id-$context).'
            GROUP BY message_id
            LIMIT '.$count;
            $res = $link->query($sql) or  $response['danger'] .= 'Query error: '.$link->errno.' '.$link->error.'<br>';
            if($res->num_rows>0){
                while($dat = $res->fetch_assoc()){
                    $response['data'][$dat['message_id']] = $dat;
                    $response['data'][$dat['message_id']]['message_data'] = json_decode($response['data'][$dat['message_id']]['message_data']);
                }
            }
            $response['result'] = $res;
        } else {
            $response['danger'] .= 'Could not find starting ID.<br>';
        }
	} else {
		$response['result'] = false;
		$response['danger'] .= 'Count should be bigger than zero.<br>';
	}
} elseif(!empty($_GET['submit_classification'])){
	$message_id = intval($_POST['message_id']);
	$classification = intval($_POST['classification']);
	if($message_id>0){
		$sql = 'INSERT INTO classifications (`message_id`,`classification`,`user_id`) VALUES (\''.$message_id.'\',\''.$classification.'\',\''.$_SESSION['user_id'].'\') ON DUPLICATE KEY UPDATE classification = \''.$classification.'\';';
		$res = $link->query($sql) or $response['danger'] .= 'Query error: '.$link->errno.' '.$link->error.'<br>';
		$response['result'] = $res;
		if(!$res){
			$response['danger'] .= 'Classification submission failed.<br>';
		} else {
			$response['success'] .= 'Classification submission successful.<br>';
            $sql = 'SELECT messages.*,
            COUNT(classification_id) as num_classifications,
            GROUP_CONCAT(SUBSTR(users.username,1,1) separator \',\') as users,
            (SELECT classification FROM classifications WHERE classifications.message_id = messages.message_id AND user_id = '.$_SESSION['user_id'].' LIMIT 1) as classification
            FROM messages
            LEFT JOIN (classifications
                LEFT JOIN (users) USING (user_id)
            ) USING (message_id)
            WHERE message_id = '.$message_id.'
            GROUP BY message_id';
            $res = $link->query($sql) or  $response['danger'] .= 'Query error: '.$link->errno.' '.$link->error.'<br>';
            if($res->num_rows>0){
                while($dat = $res->fetch_assoc()){
                    $response['data'] = $dat;
                    $response['data']['message_data'] = json_decode($response['data']['message_data']);
                }
            }
		}
	} else {
		$response['result'] = false;
		$response['danger'] .= 'Message ID should be bigger than zero.<br>\n';
	}
}
echo json_encode($response);
?>