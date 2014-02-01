function FeedController() {
}

FeedController.prototype = {
	init : function() {
		$('.card-replies-link').click(function() {
			var id = $(this).attr('id');
			var divID = '#card' + id;
			var cardHeight = $(divID).height();

			var replies = top.repliesMap[id];
			cardHeight = cardHeight + replies.length * 50 ;
			$(divID).animate({
				height: cardHeight + "px",
			}, 500, function() {

				$("#" + id).css('display', 'none');
				// $(divID).scrollTop(cardHeight);
				// $(divID).scrollTop(cardHeight);
				// $('body').scrollTop(cardHeight);

				// $('#card' + id).append();
				$('#card-image' + id).css('margin-bottom', '0px');

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
				$('#card' + id).append('<div class="input-group input-group-reply" id="reply-input' + id + '">' +
          							   '<input type="text" class="form-control">' + 
          							   '<span class="input-group-addon" id="reply-input-button' + id + '">add</span>' + 
        							   '</div>');
			}.bind(this));
		});
	},
};