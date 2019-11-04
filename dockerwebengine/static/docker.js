$(document).ready(function(){

	$('.refreshButton').on('click',function() {

		//var image_id = $(this).attr('refresh_image_id');
		//console.log(image_id);

		req = $.ajax({
			url : '/refresh',
			type : 'POST'
		});

		req.done(function(data){
			$('#Show_Image_Count').fadeOut(1000);
			$('#Show_Image_Count').text(data.imagerefresh).fadeIn(1000);

			$('#Show_Container_Count').fadeOut(1000);
			$('#Show_Container_Count').text(data.containerrefresh).fadeIn(1000);
			

			$('#Show_Volume_Count').fadeOut(1000);
			$('#Show_Volume_Count').text(data.volumerefresh).fadeIn(1000);

			$('#Show_Network_Count').fadeOut(1000);
			$('#Show_Network_Count').text(data.networkrefresh).fadeIn(1000);
		});

	});
});