$(function() {
    $("#add-post").click(function() {
        location.href = "/post";
    });
    $("#send-reply").click(function() {
        var text = $('#comment-text')[0].value;
        var parent_id = top.current_post_id;
        requestWithData('/api/comment', {
            'text': text,
            'parent_id': parent_id,
        }, function(success, data) {
            if (success) {
                console.log(data);
                location.href = '/';
            }
        });
    });
});

function request(url, form_id, callback) {
	var formData = new FormData($(form_id)[0]);
    return requestWithData(url, formData, callback);
}
function requestWithData(url, data, callback) {
    console.log(data);
	$.ajax({
        url: url,
        type: 'POST',
        data: data,
    }).done(function(data, status) {
    	if (data['status_code'] == 200) {
  			//top.session_key = data['session_key']
  			if (callback)
  				callback(true, data);
  		} else {
  			if (callback)
  				callback(false, data);
  		}
    });
}

function togglePostGet(callback) {
	top.postGetCallback = callback;
	navigator.geolocation.getCurrentPosition(onPositionUpdateForGet);
}

function onPositionUpdateForGet(position)
{
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    // alert("Current position: " + lat + " " + lng);
    postGet(lat, lng);
}

function postGet(lat, lng) {
	$.ajax({
    	type: "GET",
    	data: "lat="+lat+"&lng="+lng,
    	url: "/api/post"
	}).done(function(data){
		if (data['status_code'] == 200) {
      console.log(data);
			top.postGetCallback(true, data['result']);
		} else {
			top.postGetCallback(false, []);
		}
	});
}


function togglePostPost(form_id, callback) {
  top.postPostCallback = callback;
  top.postPostFormId = form_id;
  
  navigator.geolocation.getCurrentPosition(onPositionUpdateForPost);
}

function onPositionUpdateForPost(position) {
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    // alert("Current position: " + lat + " " + lng);
    postPost(lat, lng);
}

function postPost(lat, lng) {
  var formData = new FormData($(top.postPostFormId)[0]);
  formData.append('lat', lat);
  formData.append('lng', lng);
  $.ajax({
        url: '/api/post',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false
    }).done(function(data, status) {
      if (data['status_code'] == 200) {
        //top.session_key = data['session_key']
        if (top.postPostCallback)
          top.postPostCallback(true, data);
      } else {
        if (top.postPostCallback)
          top.postPostCallback(false, data);
      }
    });

}
// function post(form_id) {
// 	var formData = new FormData($(form_id)[0]);
// 	$.ajax({"api/post",
// 			type: 'POST',
// 			data: formData,
//             contentType: false,
//             processData: false
//     }).done(function( data ) {

//     });
// }


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
