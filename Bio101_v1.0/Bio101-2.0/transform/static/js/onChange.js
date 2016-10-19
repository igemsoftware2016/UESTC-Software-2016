$(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {event.preventDefault(); $(this).ekkoLightbox();}); 
new WOW().init();
$(document).ready(function() {
	$("#fakeUpload").click(function(event) {
		$("#readUpload").click()
	});
	$("#fakeUpload2").click(function(event) {
		$("#readUpload2").click()
	});
	// $("#fakeUpload3").click(function(event) {
	// 	$("#readUpload3").click()
	// });
	// $("#a").click(function(event) {
	// 	$("#up").click()
	// });
});
$(document).ready(function() {
	$('.fullscreen').height($(window).height() -80)
	$(window).resize(function() {
		$('.fullscreen').height($(window).height() - 80)
	})
$("#readUpload2").change(function(event) {
	var file = $("#readUpload2").val();
	var fileName = getFileName(file);
	$("#alertPath2").text(fileName)
});
});
function getFileName(o){
    var pos=o.lastIndexOf("\\");
    return o.substring(pos+1);
}
function checkSize(target){
	var isIE = /msie/i.test(navigator.userAgent) && !window.opera;
	var fileSize = 0;
	if(isIE && !target.files){
		var fileParh = target.value;
		var fielSystem = new ActiveXObject("Scripting.FileSystemObject");
		var file = fileSystem.GetFile(filePath);
		fileSize = file.Size;
	}
	else{
		fileSize = target.files[0].size;
		}
	var size = fileSize/1000/1000;
	if(size>200){
		alert("Worning: file is bigger than 200MB!");
		var obj = document.getElementById('readUpload');
		obj.outerHTML = obj.outerHTML;
	}
	else{
		var file = $("#readUpload").val();
		var fileName = getFileName(file);
		document.getElementById('alertPath').innerText = fileName;
	}
}
function isVaild(){
	var file = document.getElementById("readUpload").value;
	var token = document.getElementById("token1").value;
	if(file && token){
		alert("It will take minutes, please don't close or refresh your browser. Click 'OK' to start encoding.")
		return true;
	}
	if(!token && !file){
		alert("Please choose a file and input a code!");
		return false;
	}
	if(!file){
		alert("Please choose a file!");
		return false;
	}
	if(!token){
		alert("Please input a code!");
		return false;
	}
	else{
		alert("Please choose a file and input a code!");
		return false;
	}
}
function isVaild2(){
	var file = document.getElementById("readUpload2").value;
	var token = document.getElementById("token2").value;
	if(file && token){
		alert("It will take minutes, please don't close or refresh your browser. Click 'OK' to start decoding.")
		return true;
	}
	if(!token && !file){
		alert("Please choose a file and input a code!");
		return false;
	}
	if(!file){
		alert("Please choose a file!");
		return false;
	}
	if(!token){
		alert("Please input a code!");
		return false;
	}
	else{
		alert("Please choose a file and input a code!");
		return false;
	}
}
