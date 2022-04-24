const username_help = document.getElementById("Username");
const password = document.getElementById("Password");
const password_conf = document.getElementById("Password confirmation");

username_help.onclick = function(){
	document.getElementById("Username_help").classList.toggle('active_user_help');
	document.getElementById("Password_help").classList.remove('active_password_help');
	document.getElementById("Password confirmation_help").classList.remove('active_password_conf_help');
}

password.onclick = function(){
    document.getElementById("Username_help").classList.remove('active_user_help');
	document.getElementById("Password_help").classList.toggle('active_password_help');
	document.getElementById("Password confirmation_help").classList.remove('active_password_conf_help');
}

password_conf.onclick = function(){
	document.getElementById("Username_help").classList.remove('active_user_help');
	document.getElementById("Password_help").classList.remove('active_password_help');
	document.getElementById("Password confirmation_help").classList.toggle('active_password_conf_help');
}