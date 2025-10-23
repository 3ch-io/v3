if (localStorage.getItem('cgimode') === null) localStorage.setItem('cgimode', false);
if (localStorage.getItem('cgimode') == "true") {
 var newUrl;
 if (location.href.indexOf('read.html') != -1) {
  newUrl = location.href.replace('read.html', 'read.cgi');
  location.replace(newUrl);
 }
}
function isSmartPhone() {
let v = false;
  if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
    v = true;
  } else {
    v = false;
  }
 if (localStorage.getItem('viewer') == 'sp') v = true;
 else if (localStorage.getItem('viewer') == 'pc') v = false;
 if (location.search.indexOf('v=sp') != -1) v = true;
 if (location.search.indexOf('v=pc') != -1) v = false;
	return v;
}
function setCookie(key, value, maxAge) {
    document.cookie = key + "=\"" + encodeURIComponent(value) + "\"; path=/; max-age=" + maxAge;
}
function getCookie(key, tmp1, tmp2, xx1, xx2, xx3) {
 tmp1 = " " + document.cookie + ";";
 while(tmp1.match(/\+/)) {tmp1 = tmp1.replace("+", " ");};
 xx1 = xx2 = 0;
 len = tmp1.length;
 while (xx1 < len) {
  xx2 = tmp1.indexOf(";", xx1);
  tmp2 = tmp1.substring(xx1 + 1, xx2);
  xx3 = tmp2.indexOf("=");
  if (tmp2.substring(0, xx3) == key) {return(unescape(tmp2.substring(xx3 + 1, xx2 - xx1 - 1)));}
  xx1 = xx2 + 1;
 }
}
function switchReadJsMode() {
  var newUrl;
  if (location.href.indexOf('read.cgi') != -1) {
   localStorage.setItem('cgimode', false);
   newUrl = location.href.replace('read.cgi', 'read.html');
  }else newUrl = location.href.replace('read.html', 'read.cgi');
  location.replace(newUrl);
}
function switchReadJsMode2() {
	if (getCookie("READJS")) {
	 if (confirm("read.html モードに切り替えますか？")) {
		setCookie("READJS","on",0);
		alert("新たなモードは次回以降の読み込みで有効になります。");
	 }
	}else {
	 if (confirm("read.cgi モードに切り替えますか？")) {
		setCookie("READJS","off",365*24*60*60);
		alert("新たなモードは次回以降の読み込みで有効になります。");
	 }
	}
}