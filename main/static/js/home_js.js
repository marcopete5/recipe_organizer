$(document).ready(function(){
   $('.port').hover(function() {
    $(this).stop(true).fadeTo("slow", .5);
}, function() {
    $(this).stop(true).fadeTo("slow", 1);
});
 
  
var indexer = 0;
var animateInterval;

function animate(){
		if(indexer == 0 ){
			$("#background-slideshow > #watch-image").fadeOut(1500);
			$("#background-slideshow > #home-image").fadeIn(1500);
		}
		else if(indexer == 1 ){
			$("#background-slideshow > #home-image").fadeOut(1500);
			$("#background-slideshow > #shop-image").fadeIn(1500);
		}
		else if(indexer == 2 ){
			$("#background-slideshow > #shop-image").fadeOut(1500);
			$("#background-slideshow > #dine-image").fadeIn(1500);
		}
		else if(indexer == 3 ){
			$("#background-slideshow > #dine-image").fadeOut(1500);
			$("#background-slideshow > #watch-image").fadeIn(1500);
		}

		if(indexer == 3) indexer = 0;
		else indexer++;
	}

	animateInterval = setInterval(animate, 8000);
	animate();
  
});