$(document).ready(function(){
$.get('127.0.0.1:8000/recipe_list_API_view', function(data, status){
	console.log(status)
	console.log(data)
	display_name(data)

});

var display_name = function(stuff){
	$('#name').html('<h1>'+stuff.name+'</h1>');
}
});