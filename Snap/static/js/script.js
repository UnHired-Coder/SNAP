


$(document).ready(function(){
	$('.likeB').on('click',(function(){
		var post_id= $(this).attr("post_id")
		var action = $(this).attr("action")
	req=    $.ajax({
			url: '/liked',
			data:{ post_id : post_id, action:action },
			type: 'POST'
			},
			error: function(error){
				console.log(error);
			}
		});
           
                         
                    req.done(function(data){

                $('likeBt').text('hoooo');
});


	});
});

