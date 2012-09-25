$(document).ready(function(){
    if ( $.browser.msie ) {
        var msg = document.createElement("div");
		msg.id = "errorMsg";
		msg.innerHTML = "<div align='center'><h1><br>   神马,你居然用IE??这么土?! <br><br>推荐Chrome/Safari</h1></div>";

		document.body.appendChild(msg);
		$("#navbar").css("display", "none")
		$("#navbar").css("display", "none")
		$("#navbar").css("display", "none")
		$(".container").css("display", "none")
	    document.execCommand("stop");
     }

});
$(document).ready(function(){
	// hide #back-top first
	$("#back-top").hide();
	// fade in #back-top
	$(function () {
		$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
				$('#back-top').fadeIn();
			} else {
				$('#back-top').fadeOut();
			}
		});
		// scroll body to 0px on click
		$('#back-top a').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 800);
			return false;
		});
	});

});
