<?php
session_start();
if(empty($_SESSION['loggedin'])){
	$_SESSION['loggedin'] = false;
	$_SESSION['user'] = '';
}
if(!empty($_POST['logout'])){
	$_SESSION['loggedin'] = false;
	$_SESSION['user'] = '';
}
require_once('common.inc.php');

$users = array(
	'erwin'=>'$2y$10$KKDFVypg0MgAqbHWeKuoA.HeoFh4o0ADO.P5ckZEhux2sZLe1P/rq',
	'leon'=>'$2y$10$k.SxduzJp6e1VyFq5MlFMOw76vrY2PUV.h3EH9fXewRSd3Cf.FR7u',
	'nathan'=>'$2y$10$SelvreHhjrGVWMSvnSeQUOqhRp9IEZOPauh05ppoKWAzvW.6p38.y',
	'bart'=>'$2y$10$J5W/B0zMd/z48fEl9cd83OKA20q4LmfLR56LJvDbXThwVAAfT0crS',
	'roy'=>'$2y$10$HLXiEqLahOhelYVCnG7gUuTLw9XhK4xOLxHMziexDKE9RvxWbo8zi');
if(!empty($_POST['username']) && !empty($_POST['password'])){
    $sql = 'SELECT * FROM users WHERE username= \''.$link->real_escape_string($_POST['username']).'\'';
    $res = $link->query($sql) or die('Query error '.$link->errno.': '.$link->error.'.');
	if($res->num_rows==1){
        $dat = $res->fetch_assoc();
		if(password_verify($_POST['password'],$dat['passwordhash'])){
			$_SESSION['loggedin'] = true;
			$_SESSION['user'] = $dat['username'];
            $_SESSION['user_id'] = $dat['user_id'];
		} else {
			die('Password is not correct.');
		}
	} else {
		die('User does not exist.');
	}
}

?>
<!doctype html>
<html>
<head>
    <title>Message Classification Twitch Toxicity</title>
    <script
        src="https://code.jquery.com/jquery-3.2.1.min.js"
        integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
        crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous" />
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jsdiff/3.2.0/diff.min.js" type="text/javascript"></script>
    <script src="js/alerts.js" type="text/javascript"></script>
    <script src="js/app.js" type="text/javascript"></script>
    <script src="js/jquery.scrollTo.min.js" type="text/javascript"></script>
    <script src="js/helpers.js" type="text/javascript"></script>
    <script src="js/handlebars.runtime-v4.0.4.js" type="text/javascript"></script>
    <script src="js/handlebars-v4.0.4.js" type="text/javascript"></script>

    <link rel="stylesheet" href="css/app.css" type="text/css" />

</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="bs-component" id="alerts">
                    <div id="dangerdiv" class="alert alert-dismissable alert-danger" style="display: none;">
                        <button type="button" class="close" data-hide="alert">&times;</button>
                        <h4>Error</h4>
                        <span id="dangerdivcontent"></span>
                    </div>
                    <div id="infodiv" class="alert alert-dismissable alert-info" style="display: none;">
                        <button type="button" class="close" data-hide="alert">&times;</button>
                        <h4>Info</h4>
                        <span id="infodivcontent"></span>
                    </div>
                    <div id="successdiv" class="alert alert-dismissable alert-success" style="display: none;">
                        <button type="button" class="close" data-hide="alert">&times;</button>
                        <h4>Success</h4>
                        <span id="successdivcontent"></span>
                    </div>
                    <div id="warningdiv" class="alert alert-dismissable alert-warning" style="display: none;">
                        <button type="button" class="close" data-hide="alert">&times;</button>
                        <h4>Warning</h4>
                        <span id="warningdivcontent"></span>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <h1>Message Classifier</h1>
            </div>
        </div>

        <?php

        if(!$_SESSION['loggedin']){
        ?>
        <div class="
			row">
            <div class="col-md-6">
                <form class="form-horizontal" method="post">
                    <div class="form-group">
                        <label for="username" class="col-sm-3 control-label">Username</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" id="username" name="username" placeholder="Username" />
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="password" class="col-sm-3 control-label">Password</label>
                        <div class="col-sm-9">
                            <input type="password" class="form-control" name="password" id="password" placeholder="Password" />
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-sm-9 col-sm-offset-3">
                            <a href="passwordhash.php" class="btn btn-secondary float-left">Generate password hash</a>
                            <button type="submit" class="btn btn-primary float-right">Login</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <?php
        } else {
        ?>
        <div class="row">
            <div class="col-md-12">
                <form method="post">
                    <div class="form-group">
                        <div class="col-sm-12">

                            <button type="submit" name="logout" value="1" class="btn btn-md btn-danger float-right">Logout</button>
                            <div class="float-right hidden-print ajaxloader" id="ajaxbusy">
                                <img src="img/ajax-loader-arrows-black.gif" alt="..." />
                                Busy...
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <?php
            include_once('classifierpage.php');
        }
        ?>
    </div>
</body>
</html>