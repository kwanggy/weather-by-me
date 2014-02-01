function FeedController() {
}

FeedController.prototype = {
	init : function() {
		$('.card-replies-link').click(function() {
			var id = $(this).attr('id');
			var divID = '#card' + id;
			var cardHeight = $(divID).height();

			var replies = top.commentsMap[id];
			// cardHeight = cardHeight + replies.length * 50 ;
			$(divID).animate({
				height: cardHeight + "px",
			}, 500, function() {
				$(this).unbind('click');	
				// $("#" + id).css('display', 'none');
				// $(divID).scrollTop(cardHeight);
				// $(divID).scrollTop(cardHeight);
				// $('body').scrollTop(cardHeight);

				// $('#card' + id).append();
				// $('#card-image' + id).css('margin-bottom', '0px');

				for (i = 0; i < replies.length; i++) {
					reply = replies[i];
					var replyDiv = 
					'<div class="horizontal-divider replies-divider"></div>' + 
					'<div class="reply-container" >' +
						'<img src="' + reply['profile_url'] + '" + class="img-circle card-reply-profile" />' + 
						'<div class="reply-name">' + reply['name'] + '</div>' +
						'<div class="reply-content">' + reply['reply'] + '</div>' + 
					'</div>'
					;

					$('#card' + id).append(replyDiv);
				}
				$('#card' + id).append('<div class="horizontal-divider replies-divider card-component"></div>');
				// $('#card' + id).append('<div class="input-group input-group-reply" id="reply-input' + id + '">' +
    //       							   '<input type="text" class="form-control">' + 
    //       							   '<span class="input-group-addon" id="reply-input-button' + id + '">add</span>' + 
    //     							   '</div>');
			}.bind(this));
		});

		$('.card-reply-link').click(function() {
			var id = $(this).attr('id');
			id = id.substr(id.length-1, 1);
			top.current_post_id = id;


		});
	},
	getCard: function(id, pic, title, name, image, commentsLength) {
		return
		  '<div class="row">' + 
		    '<div class="col-lg-6">' + 
		      '<div id="card' + id + '" class="card" >' + 
		        '<div class="card-component card-profile-container img-circle"></div>'
		        '<img src="' + pic + '" class="img-circle card-component card-profile" style=""/>' + 
		        '<div class="horizontal-divider card-component card-divider"></div>' + 
		        '<div class="card-component card-title">' + title '</div>' + 
		        '<div class="card-component card-time">2 hours ago</div>' +
		        '<img class="card-image" id="card-image' + id + '" src="' + image + '"/>' + 
		        '<div class="pull-left card-replies-link card-component" id="' + id + '">comments</div>' + 
		        '<div class="pull-right card-reply-link card-component" id="add-reply' + id + '" data-toggle="modal" data-target="#add-reply-modal">add comment</div>' + 
		      '</div>' + 
		    '</div>' + 
		  '</div>';
	},
};