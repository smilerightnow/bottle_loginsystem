<html>
<head>
  <title>{{title or 'No title'}} - Bniwen</title>
  <style>
	#alert {
		position: relative;
		padding: 0.75rem 1.25rem;
		margin-bottom: 1rem;
		border: 1px solid transparent;
		border-radius: 0.25rem;
	}
	.alert-info {
		color: #004085;
		background-color: #cce5ff;
		border-color: #b8daff;
	}
	.alert-error {
		color: #721c24;
		background-color: #f8d7da;
		border-color: #f5c6cb;
	}
	.alert-success {
		color: #155724;
		background-color: #d4edda;
		border-color: #c3e6cb;
	}
  </style>
</head>
<body>
	<script>
		const getCookie = (name) => (
		  document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ""
		)
		function eraseCookie(name) {   
			document.cookie = name+'=; Max-Age=-99999999;';  
		}
		let notif = getCookie("notification").replace(/"/g,"").split(":::");
		if (notif.length > 1){
			var alert = document.createElement("DIV");
			alert.id = "alert";
			alert.className = "alert-" + notif[0];
			alert.innerHTML = notif[1].replace(/\\054/g, ",") + '<span style="cursor: pointer;color: black;float: right;user-select: none;padding: 0.5em;margin: -0.5em;" onclick="this.parentElement.remove()">X</span>';
			document.body.appendChild(alert)
			eraseCookie("notification");
		}
	</script>
	<div id="header">
		
			<a href="/logout">Logout</a>
			<a href="/login">Login</a>
			<a href="/signup">Signup</a>

	</div>
	<div id="container">{{!base}}</div>
	<div id="footer"></div>
</body>
</html>
