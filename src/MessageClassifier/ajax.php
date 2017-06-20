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
	if($count>0){
		//TODO context?
		$sql = 'SELECT * FROM (SELECT messages.*,
				(SELECT count(*) FROM classifications WHERE classifications.user = \''.$_SESSION['user'].'\' AND classifications.message_id = messages.message_id) as self_classifications,
				(SELECT count(*) FROM classifications WHERE classifications.user <> \''.$_SESSION['user'].'\' AND classifications.message_id = messages.message_id) as other_classifications
				FROM messages LIMIT '.BLOCK_OFFSET.','.BLOCK_SIZE.') as t
				WHERE self_classifications = 0 AND other_classifications < '.RATES_LIMIT.' LIMIT '.$count.';';
		$res = $link->query($sql) or print('Query error: '.$link->errno.' '.$link->error);
		if($res->num_rows>0){
			while($dat = $res->fetch_assoc()){
				$response['data'][$dat['message_id']] = $dat;
				$response['data'][$dat['message_id']]['message_data'] = json_decode($response['data'][$dat['message_id']]['message_data']);
			}
		}
		$response['result'] = $res;
	} else {
		$response['result'] = false;
		$response['danger'] .= 'Count should be bigger than zero.<br>\n';
	}
} elseif(!empty($_GET['submit_classification'])){
	$message_id = intval($_POST['message_id']);
	$classification = intval($_POST['classification']);
	if($message_id>0){
		$sql = 'INSERT INTO classifications (`message_id`,`classification`,`user`) VALUES (\''.$message_id.'\',\''.$classification.'\',\''.$_SESSION['user'].'\')';
		$res = $link->query($sql);
		$response['result'] = $res;
		if(!$res){
			$response['danger'] .= 'MySQL Error '.$link->errno.': '.$link->error.'.<br>\n';
		} else {
			$response['success'] .= 'Classification submission successful.<br>\n';
		}
	} else {
		$response['result'] = false;
		$response['danger'] .= 'Message ID should be bigger than zero.<br>\n';
	}
}
echo json_encode($response);
?>