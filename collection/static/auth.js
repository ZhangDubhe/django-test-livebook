function check_login() {
	if(!session.uuid){
		location.href = API_PATH + "account/login"
	}
}

function login(uuid) {
	session.setItem('uuid',uuid);
}

function register() {
	$()
}