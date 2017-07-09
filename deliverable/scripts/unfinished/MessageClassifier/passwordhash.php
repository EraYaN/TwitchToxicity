<?php
session_start();
?>
<!doctype html>
<html>
<head>
	<title>Message Classification Twitch Toxicity - Password Gen</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous" />
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
</head>
<body>

	<div class="row">
		<?php
		if(!empty($_POST['password'])){
			echo '<div class="col-md-6"><h2>Password hash</h2><p>'.password_hash($_POST['password'],PASSWORD_DEFAULT).'</p></div>';
		}
        ?>
		</div>
	<div class="row">
		<div class="col-md-6">
			<form class="form-horizontal" method="post">

				<div class="form-group">
					<label for="password" class="col-sm-3 control-label">Password</label>
					<div class="col-sm-9">
						<input type="password" class="form-control" name="password" id="password" placeholder="Password" />
					</div>
				</div>
				<div class="form-group">
					<div class="col-sm-9 col-sm-offset-3">
						<button type="submit" class="btn btn-primary pull-right">Generate</button>
					</div>
				</div>
			</form>
		</div>

	</div>
</body>
</html>