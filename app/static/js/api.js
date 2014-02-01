function signup(form_id) {
	var formData = new FormData($(image_form_id)[0]);
	$.ajax({"api/signup",
			type: 'POST',
			data: formData,
            contentType: false,
            processData: false
    }).done(function(data, status) {
    	if (data['status_code'] == 200) {
  			top.session_key = data['session_key']
  			callback(true);
  		} else {
  			callback(false)
  		}
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

function post(form_id) {
	var formData = new FormData($(form_id)[0]);
	$.ajax({"api/post",
			type: 'POST',
			data: formData,
            contentType: false,
            processData: false
    }).done(function( data ) {

    });
}


	// $.post("api/signup",
	// {
	// 	'email': email,
 //    	'pw': pw,
 //    	'name': name
 //  	},
 //  	function(data, status){
 //  		if (data['status_code'] == 200) {
 //  			top.session_key = data['session_key']

 //  			callback(true);
 //  		} else {
 //  			callback(false)
 //  		}
 //    	// alert("Data: " + data['error'] + "\nStatus: " + status);
 //  	});