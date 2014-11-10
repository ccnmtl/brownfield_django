jQuery(function() {
	
    // handle hash tag navigation
    var hash = window.location.hash;
    hash && jQuery('.instructor-nav a[href="' + hash + '"]').tab('show');
  
    // when the nav item is selected update the page hash
    jQuery('.instructor-nav a').on('shown', function (e) {
        window.location.hash = e.target.hash;
        scrollTo(0,0);
    });	
	
});

function openPopWin(theURL,w,h,resizing,scrolling,winname,closeOnLogout) {
	
	var str = theURL;
	var res = str.replace("{{STATIC_URL}}", window.location.hostname + ':8000/media/'); 
	console.log("res");
	console.log(res);
	var winl = (screen.width - w) / 2;
	var wint = (screen.height - h) / 2;
    winprops = 'height='+h+',width='+w+',top='+wint+',left='+winl+',resizable='+resizing+',scrollbars='+scrolling+',location=no,status=no,menubar=no,directories=no,toolbar=no';
    console.log("res before window.open - seems to be adding %3");
    console.log(res);
    console.log("Try explicitly casting to string");
    console.log(String(res));
    //popwin = window.open(String(res), winname, winprops);
    
    popwin = window.open(str.replace("{{STATIC_URL}}", window.location.hostname + ':8000/media/'), winname, winprops);
    
    if (/\.jpg$/.test(res)) {
	popwin.document.write(
			'<a href="javascript:void(0)" onclick="window.print()">print article</a><br />' + 
			'<img src="' + res + '" alt="news article"/>');
	//popwin.document.write('<img src="'+res+'" alt="news article"/>');
	popwin.document.close();
    }
    if (closeOnLogout) {
	windows_to_close_on_logout.push(popwin);
    }
    if (parseInt(navigator.appVersion) >= 4) { popwin.window.focus(); }
    if (popwin.opener == null) { popwin.opener = self; }
}