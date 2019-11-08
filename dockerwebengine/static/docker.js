//Refresh Docker Summary
$(document).ready(function(){

	$('.refreshButton').on('click',function() {
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


//Refresh Docker Image
$(document).ready(function(){

	$('.refreshButton-image').on('click',function() {
		req = $.ajax({
			url : '/refresh',
			type : 'POST'
		});

		req.done(function(data){
			$('#Show_Image_Count').fadeOut(1000);
			$('#Show_Image_Count').text(data.imagerefresh).fadeIn(1000);

		});

	});
});


//Refresh Docker Container
$(document).ready(function(){

	$('.refreshButton-container').on('click',function() {
		req = $.ajax({
			url : '/refresh',
			type : 'POST'
		});

		req.done(function(data){

			$('#Show_Container_Count').fadeOut(1000);
			$('#Show_Container_Count').text(data.containerrefresh).fadeIn(1000);
			
		});

	});
});

//Refresh Docker Volume
$(document).ready(function(){

	$('.refreshButton-volume').on('click',function() {
		req = $.ajax({
			url : '/refresh',
			type : 'POST'
		});

		req.done(function(data){
			
			$('#Show_Volume_Count').fadeOut(1000);
			$('#Show_Volume_Count').text(data.volumerefresh).fadeIn(1000);

			
		});

	});
});


//Refresh Docker Network
$(document).ready(function(){

	$('.refreshButton-network').on('click',function() {
		req = $.ajax({
			url : '/refresh',
			type : 'POST'
		});

		req.done(function(data){
			
			$('#Show_Network_Count').fadeOut(1000);
			$('#Show_Network_Count').text(data.networkrefresh).fadeIn(1000);
		});

	});
});

//Delete the Selected Image
$(document).ready(function(){

	$('.delete-image').on('click',function(){

		var Row = document.getElementById("ImageRow");
		var Cell = Row.getElementsByTagName("td");
		id = Cell[0].innerText;

		req = $.ajax({
			url : '/delete_image/'+ id,
			type : 'POST'
		});

		req.done(function(data){

			//Check if any error is occured
			if (data.result == "fail")
			{
				alert(data.msg);
			}
			else{

				//Update Image count
				$('.imgcount').text(data.imagerefresh)
				console.log(data.result);
				//Remove selected table row
				document.getElementById("ImageRow").remove();

			}

			
			
			
		});

	});
});