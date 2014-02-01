function signup(email, pw, name, callback) {
	$.post("api/signup",
	{
		'email': email,
    	'pw': pw,
    	'name': name
  	},
  	function(data, status){
  		if (data['status_code'] == 200) {
  			top.session_key = data['session_key']

  			callback(true);
  		} else {
  			callback(false)
  		}
    	// alert("Data: " + data['error'] + "\nStatus: " + status);
  	});
}

function signin(email, pw, callback) {
	$.post("api/signin",
	{
		'email': email,
    	'pw': pw,
  	},
  	function(data, status){
  		if (data['status_code'] == 200) {
  			top.session_key = data['session_key']
  			callback(true);
  		} else {
  			callback(false)
  		}
    	alert("Data: " + data + "\nStatus: " + status);
  	});	
}

