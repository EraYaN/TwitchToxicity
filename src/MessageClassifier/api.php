<?php
require_once('common.inc.php');
$apikeys = array('jnWJc23aMvFfhoGtwHxFwRQMnhzRTKpUa04h');
if(!empty($_POST['apikey'])){
    if(!in_array($_POST['apikey'],$apikeys)){
        header('HTTP/1.0 403 Forbidden');
	    die("{'msg':'Forbidden'}");
    }
}

if(isset($_POST['d'])){
    if($_POST['d']=='classifications'){
        $response = array(
            'danger'=>'',
            'warning'=>'',
            'success'=>'',
            'info'=>'',
            'result'=>false,
            'data' => array()
        );
        $count = 50;
        if(!empty($_POST['count'])){
            $count = intval($_POST['count']);
        }
        $offset = 0;
        if(!empty($_POST['offset'])){
            $count = intval($_POST['offset']);
        }
        $minratings = 1;
        if(!empty($_POST['minratings'])){
            $minratings = intval($_POST['minratings']);
        }

        $sql = 'SELECT messages.*,
        AVG(classifications.classification) as compound_classifications,
        COUNT(classifications.classification_id) as num_classifications
        FROM messages
        LEFT JOIN (classifications) USING (message_id)
        GROUP BY message_id
        HAVING COUNT(classifications.classification_id) >= '.$minratings.'
        LIMIT '.$offset.','.$count;
        $res = $link->query($sql) or  $response['danger'] .= 'Query error: '.$link->errno.' '.$link->error.'<br>';
        if($res->num_rows>0){
            while($dat = $res->fetch_assoc()){

                $dat['message_data'] = json_decode($dat['message_data'],true);
                $response['data'][$dat['message_id']] = $dat;
            }
        }

        echo json_encode($response);
    } else {
        header('HTTP/1.0 404 Not Found');
        die("{'msg':'Not Found'}");
    }
} else {
    header('HTTP/1.0 404 Not Found');
    die("{'msg':'Not Found'}");
}
?>