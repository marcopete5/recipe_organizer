$('.recipe_filter').click(function(){
	console.log($(this).text())
})

$('#add-ing').click(function(){
	$.get('search/?q=beef', function(data){
		console.log(data)
	})
})