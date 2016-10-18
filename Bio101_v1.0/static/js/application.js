// Demo Images - Slide Play Mode
$(document).ready(function() {
	$("#owl-demo").owlCarousel({
	autoPlay: 3000,
	lazyLoad   : true,
	navigation : true,
	slideSpeed : 300,
	paginationSpeed : 400,
	singleItem : true
	
	// "singleItem:true" is a shortcut for:
	// items : 1, 
	// itemsDesktop : false,
	// itemsDesktopSmall : false,
	// itemsTablet: false,
	// itemsMobile : false
	
	});
});

