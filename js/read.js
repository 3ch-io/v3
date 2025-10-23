	let readhtml = 'read.html ver 02 - 2023/07/12';
	let spcheck = '';
	if (isSmartPhone() == true) {
	 spcheck = 'checked';
	 if (localStorage.getItem('subback') === null) localStorage.setItem('subback', true);
	}else if (localStorage.getItem('subback') === null) localStorage.setItem('subback', false);
	let LINENUM,reloadbutton,getprev,preved;
	if (localStorage.getItem('treeView') === null) localStorage.setItem('treeView', false);
	if (localStorage.getItem('tshide') === null) localStorage.setItem('tshide', true);
	if (localStorage.getItem('ghide') === null) localStorage.setItem('ghide', 'auto');
	if (localStorage.getItem('areload') === null) localStorage.setItem('areload', false);
	if (localStorage.getItem('darkmode') === null) localStorage.setItem('darkmode', false);
	if (localStorage.getItem('autoscroll') === null) localStorage.setItem('autoscroll', false);
	localStorage.setItem('autoPost', true);
	localStorage.setItem('backlinkOpen', false);
	localStorage.setItem('ankfixed', true);
	if (localStorage.getItem('text2') === null) localStorage.setItem('text2', '');
	sessionStorage.removeItem('text');
	treeView = "false";
	subback = localStorage.getItem('subback');
	cgimode = localStorage.getItem('cgimode');
	tshide = localStorage.getItem('tshide');
	ghide = localStorage.getItem('ghide');
	areload = localStorage.getItem('areload');
	ankfixed = localStorage.getItem('ankfixed');
	darkmode = localStorage.getItem('darkmode');
	autoscroll = localStorage.getItem('autoscroll');
	let mutejson;
	let mutelist = [];
	mutejson = localStorage.getItem('mutelist');
	if (mutejson) {
	mutelist = JSON.parse(mutejson);
	mutelist = mutelist.filter(Boolean);
	}
	let ngjson;
	let nglist = [];
	ngjson = localStorage.getItem('nglist');
	if (ngjson) {
	nglist = JSON.parse(ngjson);
	nglist = nglist.filter(Boolean);
	}
	let ntjson;
	let ntlist = [];
	ntjson = localStorage.getItem('ngtitle');
	if (ntjson) {
	ntlist = JSON.parse(ntjson);
	ntlist = ntlist.filter(Boolean);
	}
	let thread = '';
	let path = location.pathname.split('/');
	let bbs = path[3];
	let key = path[4];
	const ls = new URLSearchParams(window.location.search);
	let res = [];
	let idlist = [];
	let imglist = [];
	let plist = [];
	let number = 0;
	let threaddata = document.getElementsByClassName('thread')[0];
	if (window.location.search && ls.has('ls') == false && ls.has('nofirst') == false) areload = false;
if (localStorage.getItem('subback') == "true") {
	document.getElementById("back").href = '/'+bbs+'/subback/';
	document.getElementById("bback").href = '/'+bbs+'/subback/';
}
document.getElementsByClassName('topmenu')[0].innerHTML += '<a class="menuitem" href="/find/">本文検索</a><a class="menuitem" href="/'+bbs+'/subject.html">過去ログ</a><a class="menuitem" href="javascript:MenuClick(\'popular\')">人気レス一覧</a><a class="menuitem" href="javascript:MenuClick(\'picture\')">画像一覧</a><hr>';
document.getElementsByClassName('bottommenu')[0].innerHTML += '<a class="menuitem" href="/find/">本文検索</a><a class="menuitem" href="/'+bbs+'/subject.html">過去ログ</a><a class="menuitem" href="javascript:MenuClick(\'popular\')">人気レス一覧</a><a class="menuitem" href="javascript:MenuClick(\'picture\')">画像一覧</a>';
let style = document.createElement('style');
let stylesheet = '';
if (treeView != "true") stylesheet += '.treeView{display:none !important;}';
if (ghide == "all") stylesheet += '.image{display:none;}';
style.innerHTML = stylesheet;
document.getElementById('body').appendChild(style);
document.getElementById('body').innerHTML += '<link href="https://delight.rentalbbs.net/css/lightbox.css" rel="stylesheet"><style id="mute"></style><style id="prev-hide"></style>';
if (isSmartPhone() == false) document.getElementById('body').innerHTML += '<style>body{color:rgb(87, 111, 118) !important;}a{color:#485269 !important;}.thread,.title,.pagestats{padding-left:15px;padding-right:15px}.post{padding:1em 0}.number,.name,.date,.ids,details{font-size:12px;color:rgb(87, 111, 118) !important;margin-right:5px;padding-left:0;margin-left:0}.thread{width: 75%;}.id{color:rgb(87, 111, 118) !important;}.message{padding:10px 0;font-size:16px}.side{display: block;border: .5px solid #DCDCDC; position: fixed; right: 0em; top: 0em; bottom: auto; width: 25%; height: 100%; z-index:  1; margin: 0; padding: 0; color: #333; padding-top: 10em; overflow: auto;scrollbar-width: none;}.side::-webkit-scrollbar{display: none;}#headline{height: auto;overflow-y: auto;}</style>';
ver = document.createElement("div");
ver.style.color = "#000";
ver.className = "footer push";
ver.appendChild(document.createTextNode(readhtml));
document.getElementById('body').appendChild(ver);
if (document.getElementsByTagName('form')[0]) document.getElementsByTagName('form')[0].id = 'postForm';
if (document.getElementsByTagName('textarea')[0]) {
	document.getElementsByTagName('textarea')[0].id = 'bbs-textarea';
	document.getElementsByTagName('textarea')[0].setAttribute('onchange', 'MSG()');
}
 if (localStorage.getItem('formfixed') == "true") {
     document.getElementById('postForm').style.backgroundColor = '#fff';
     document.getElementById('postForm').style.border = '1px outset #000';
     document.getElementById('postForm').style.position = 'fixed';
     document.getElementById('postForm').style.zIndex = '1';
     document.getElementById('postForm').style.bottom = '5px';
     document.getElementById('postForm').style.left = '10px';
     document.getElementById('postForm').style.padding = '5px';
     document.getElementById('postForm').innerHTML += '<label><input type="checkbox" id="isFixedForm" onchange="FixedForm();" checked>入力フォーム位置固定</label>';
 }else document.getElementById('postForm').innerHTML += '<label><input type="checkbox" id="isFixedForm" onchange="FixedForm();">入力フォーム位置固定</label>';
let mutes = '';
			//スレッド描画
	let request = new XMLHttpRequest();
	request.open('GET', '/' + bbs + '/dat/' + key + '.dat');
	request.send();
	request.onreadystatechange = () => {
		if(request.readyState === 4 && request.status === 200) {
			let data = request.responseText.split('\n');
			if (ls.has('ls')) start = data.length - ls.get('ls');
			else if (ls.has('st')) start = ls.get('st');
			else start = 1;
			if (ls.has('to')) end = ls.get('to');
			else end = data.length;
			document.getElementById('thread').innerHTML = '';
			data.forEach(function(value) {
			if (value.indexOf('<>') == -1) return;
			let dat = value.split('<>');
			let name = dat[0];
			let mail = dat[1];
			let dateid = dat[2];
			let message = dat[3];
			number++;
			if (ls.get('nofirst') == "true" && number == 1) return;
			if (number != 1) {
			 if (number < start || number > end) return;
			}
			let numtext = '<a href="javascript:Menu('+number+')" class="number" id="number-'+number+'">'+number+'</a>';
			let NG;
			let names;
			names = name.split('</b>');
			name = names[0];
			name = name.replace('<b>', '');
			if (isSmartPhone() == false) name = '<b>'+name+'</b>';
			let id2 = names[1];
			let id3 = names[2];
			let id4 = names[3];
			if (id2) {
			if (!NG) NG = MuteCheck(id2);
			id2 = nameid(id2,2,number);
			}
			if (id3) {
			if (!NG) NG = MuteCheck(id3);
			id3 = nameid(id3,3,number);
			}
			if (id4) {
			if (!NG) NG = MuteCheck(id4);
			id4 = nameid(id4,4,number);
			}
			if (id2) name += ' '+id2;
			if (id3) name += ' '+id3;
			if (id4) name += ' '+id4;
			if (mail) name += ' ['+mail+']';
			let nametext = '<span class="name" id="name-'+number+'">'+name+'</span>';
			let dateids;
			if (dateid) dateids = dateid.split(' ');
			if (!dateids) return;
			let date = dateids[0]+' '+dateids[1];
			let id = [];
			if (dateids[2]) {
			if (!NG) NG = MuteCheck(dateids[2]);
			id[0] = ID(dateids[2],0,number);
			}
			if (dateids[3]) {
			if (!NG) NG = MuteCheck(dateids[3]);
			id[1] = ID(dateids[3],1,number);
			}
			if (dateids[4]) {
			if (!NG) NG = MuteCheck(dateids[4]);
			id[2] = ID(dateids[4],2,number);
			}
			if (dateids[5]) {
			if (!NG) NG = MuteCheck(dateids[5]);
			id[3] = ID(dateids[5],3,number);
			}
			let ids = '<span class="ids" id="ids-'+number+'">';
			if (id[0]) ids += ' '+id[0];
			if (id[1]) ids += ' '+id[1];
			if (id[2]) ids += ' '+id[2];
			if (id[3]) ids += ' '+id[3];
			ids += '</span>';
			date = date.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			let datetext;
			if (isSmartPhone() == true) datetext = '<span class="date" id="date-'+number+'">'+ids+date+'</span>';
			else datetext = '<span class="date" id="date-'+number+'">'+date+ids+'</span>';
			datetext = datetext.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			if (!message) return;
			let rnum = message.match(/&gt;&gt;([0-9]+)(?![-\d])/);
			if (rnum) rnum = rnum[1];
			if (ghide == "auto") {
			 if (message.indexOf('グロ') != -1 || message.indexOf('死ね') != -1) {
			  if (rnum) imghide(rnum);
			  imghide(number);
			 }
			}
			if (document.getElementById('back-'+rnum)) {
			if (treeView != "true") document.getElementById('back-'+rnum).innerHTML += '<a class="back-link" href="javascript:void(0);">&gt;&gt;'+number+'</a>';
			else document.getElementById('back-'+rnum).innerHTML += '<a></a>';
			let replycount = $('#back-'+rnum).children().length;
			if (replycount < 3) document.getElementById('number-'+rnum).style.color = '#518dc9';
			else if (replycount < 5) document.getElementById('number-'+rnum).style.color = '#a551c9';
			else if (replycount < 10) document.getElementById('number-'+rnum).style.color = 'darkred';
			else document.getElementById('number-'+rnum).style.color = 'darkgoldenrod';
			document.getElementById('rcount-'+rnum).innerHTML = replycount;
			if (treeView != "true") document.getElementById('replys-'+rnum).style.display = "block";
			if (replycount == 3) plist.push(rnum);
			}
			let wiki = message.match(/.*(\[\[.+\]\]).*/);
			if (wiki) message = message.replace(wiki[1],          
                        function(){
			let a;
			   a = arguments[0].replace('[[','');
			   a = a.replace(']]','');
                            return '<a href="https://ja.wikipedia.org/wiki/'+a+'" title="'+a+'" target="_blank">'+a+'</a>';
                        });
			let newpost = document.createElement("div");
			newpost.className = 'post';
			newpost.id = number;
			newpost.dataset.date = 'NG';
			newpost.dataset.userid = dateids[2];
			newpost.dataset.id = number;
			if (rnum != number && rnum != 1 && rnum < 1000 && document.getElementById(rnum) && treeView != "false") {
			 if (tshide != "false") newpost.style.display = 'none';
			 message = message.replace('&gt;&gt;', '');
			}
			let msgtext = '<div class="message" id="msg-'+number+'">'+message+'</div>';
			if (isSmartPhone() == true) newpost.innerHTML = numtext+nametext+msgtext+datetext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			else newpost.innerHTML = numtext+nametext+datetext+msgtext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			document.getElementById('thread').appendChild(newpost);
			message = message.replace(/<b> \*/g,'<b> ');
			message = message.replace(/<i> _/g,'<i> ');
			message = message.replace(/<s> -/g,'<s> ');
			message = message.replace(/<font color="gray"> \&gt;/g,'<font color="gray"> ');
			message = message.replace(/<font color="green"> @/g,'<font color="green"> ');
			message = message.replace(/<small style="opacity: 0\.7;"> \^/g,'<small style="opacity: 0.7;"> ');
			message = message.replace(/<span class="_mfm_blur_"> ~/g,'<span class="_mfm_blur_"> ');
			message = message.replace(/<center> \\/g,'<center> ');
			if (message.indexOf('<span class="AA">') != -1) {
			message = message.replace('<span class="AA">','');
			message = message.replace('</span>','');
			document.getElementById('msg-'+number).className += " AA";
			}
			if (message.indexOf('data-lightbox="image"') != -1) imglist.push(number);
			document.getElementById('msg-'+number).innerHTML = message;
			if (!NG) NG = WordCheck(name+mail+message);
			if (NG) {
			Muten(number);
			document.getElementById('msg-'+number).style.display = "none";
			document.getElementById('date-'+number).style.display = "none";
			document.getElementById('name-'+number).innerHTML = 'あぼーん['+NG+']';
			}
			if (number == localStorage.getItem(bbs+key)) {
			 let readline = document.createElement('div');
			 readline.innerHTML = 'ここまで読んだ';
			 if (darkmode == "true") readline.style.cssText = 'background-color: #333333;color: #fff;text-align: center;font-size: 80%;';
			 else readline.style.cssText = 'background-color: #f0f0f0;color: #666666;text-align: center;font-size: 80%;';
			 document.getElementById(number).after(readline);
			}
			LINENUM = number;
			if (areload != false && number > localStorage.getItem(bbs+key)) localStorage.setItem(bbs+key, LINENUM);
			});
		}
	};

function Post() {
 if (isSmartPhone() == true) fclose();
 document.getElementById('ntxt').innerHTML = '通信中';
 notice();
 setTimeout(Getresponse, 1500);
 let cookname = escape(document.getElementsByName("FROM")[0].value); 
 document.cookie = "NAME="+cookname+"; Max-Age=7776000; path=/";
 let cookmail = escape(document.getElementsByName("mail")[0].value);
 document.cookie = "MAIL="+cookmail+"; Max-Age=7776000; path=/";
}

function Getresponse() {
 let loggd = '';
 if (!getCookie("email")) loggd = '<br><a href="https://delight.rentalbbs.net/login.html">ログインして書くことができます</a>';
 if (getCookie("response")) {
	if (decodeURI(getCookie("response")) != "&#26360;&#12365;&#12371;&#12415;&#12414;&#12375;&#12383;") {
	 let html = '<div>ＥＲＲＯＲ！</div><font size="+1" color="#FF0000"><b>'+decodeURI(getCookie("response"))+loggd+'</b></font>';
	 html += '<hr><ul><font size=+1 color=#00AA00><b>エラーの原因が分からない？</b></font><ul style="line-height:1.5;">まず確認しよう！<br><b>《<a href="https://delight.rentalbbs.net/faq/">FAQ</a>》<br></b></ul><br><font size="+1" color="#DD00DD"><b>もしかしてアクセス規制ですか？</b></font><div style="line-height:1.5;"><b>各板の管理者さんが規制を解除するまで規制は続きます。</b><br>個別の対応・進展については、各板の管理者さんへお尋ねください。</div><br></ul><br><br><br><br><br><br><br><br>';
	 document.getElementById('modal_text').innerHTML = html;
	 document.getElementById('rModal').style.display = 'block';
	 if (sessionStorage.getItem('text')) document.getElementById('bbs-textarea').value = sessionStorage.getItem('text');
	}else {
	 sessionStorage.removeItem('text');
 	 if (areload != "true") reload();
	}
 }else {
	 sessionStorage.removeItem('text');
	 if (areload != "true") setTimeout(reload, 1500);
 }
}

function l(e){
 var N=getCookie("NAME"),M=getCookie("MAIL"),i;
 with(document) for(i=0;i<forms.length;i++)if(forms[i].FROM&&forms[i].mail)with(forms[i]){
  FROM.value=N;
  mail.value=M;
 }
}
onload=l;
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
 return("");
}

if (!getCookie("icon") && document.getElementById('seticon')) document.getElementById('seticon').style.display = 'none';

document.getElementById('hline').style.display = 'block';
morelist();
headline();
setInterval(headline, 5000);

if (areload == "true" && document.getElementById('postForm').style.display != "none") {
 setInterval(reload, 5000);
}

if (getprev) {
			let prevbutton = document.createElement('center');
			prevbutton.id = "prevbutton";
			prevbutton.innerHTML = '<a name="1"></a><a href="#1" onclick="prev('+getprev+')">前のレスを取得</a>';
			document.getElementById(getprev).before(prevbutton);
}

let modal = document.createElement('div');
modal.innerHTML = '<div id="Modal" style="background-color:#fafafa;margin:auto;padding:20px;border:1px solid #888;width:500px;max-width:95%;"><span style="color:#000;float:right;font-size:28px;font-weight:bold;cursor:pointer;" class="rclose" onclick="rclose()">×</span><div id="modal_text" style="width: 100%;color:#808080;font-family: arial,helvetica,sans-serif;font-size:10pt;margin: 2em 4px 0 0;">'+
'</div></div>';
modal.id = 'rModal';
modal.style.cssText = 'position: fixed; z-index: 20; left: 0px; top: 0px; width: 100%; height: 100%; overflow: auto; background-color: rgba(0, 0, 0, 0.4);';
modal.style.display = 'none';
document.getElementById('body').appendChild(modal);

let notific = document.createElement('div');
notific.innerHTML = '<div id="ntxt" style="font-size:13px;background-color:#404040;width:18%;margin:0 auto;text-align:center;border-radius:3px;padding:4px">'+'</div>';
notific.id = 'notific';
notific.style.cssText = 'display:none;opacity:0;bottom:5%;color:#fff;position:fixed;width:100%;z-index:20';
document.getElementById('body').appendChild(notific);

var t2 = document.createElement("script");
t2.src = "https://delight.rentalbbs.net/js/t2.js";
document.getElementById('body').appendChild(t2);

var lightbox = document.createElement("script");
lightbox.src = "https://delight.rentalbbs.net/js/lightbox.js";
document.getElementById('body').appendChild(lightbox);

var inactive = document.createElement("script");
inactive.src = "https://delight.rentalbbs.net/js/inactive.js";
document.getElementById('body').appendChild(inactive);

$(document).on("mouseover", ".ank",function(e){
	var timer = setTimeout(function(_this){
		let anknum = $(_this).text().replace('>>', '');
		let repnum = $(_this).attr('class').replace('ank rep-', '');
		if (anknum != "1" && getprev > anknum) prev(getprev,true);
		//ResAnchor(anknum,repnum);
	},0,$(this));
});
$(document).on("mouseover", ".ank2",function(e){
let repnum,anks;
	var t = setTimeout(function(_this){
		let anknum = $(_this).text().replace('>>', '');
		repnum = $(_this).attr('class').replace('ank2 rep-', '');
		anks = anknum.split('-');
		if (getprev > anks[0] || getprev > anks[1]) prev(getprev,true);
		ResAnchor2(anks[0],anks[1],repnum);
	},500,$(this));
});

$(document).on("mouseover", ".id",function(e){
	var timer = setTimeout(function(_this){
		let i = $(_this).text().split('(');
		let c,f;
		if (i[1]) c = i[1].replace(')', '');
		else c = 1;
		let n;
		if ($(_this).parent().attr('id')) n = $(_this).parent().attr('id').replace('ids-', '');
		if (!$(_this).attr('id')) {
		$(_this).attr('id', 'id-'+i[0]+'-'+n);
		f = 'id-'+i[0]+'-'+n;
		}
		else f = false;
		HighLightId(i[0],c,f);
	},500,$(this));
});

document.getElementById('body').onclick = function (event) {
	let x = event.clientX;
	let y = event.clientY;
	let e = document.elementsFromPoint(x, y);
	let repid,menid,rt,ri;
	e.forEach(function(el) {
		if (el.className == "rep-comment") {
		repid = el.id;
		}
		else if (el.id == "Modal") {
		menid = el.id;
		}
		if (el.className == "number" || el.className == "menuitem") rt = true;
		if (el.className == "id" || el.className == "ank2" || el.className == "id id2") ri = true;
	});
	let reps = document.querySelectorAll(".rep-comment");
	if (!reps) return;
	reps.forEach(function(v) {
	 var timer = setTimeout(function(){
	  if (v.id == repid) return;
	   v.style.display = 'none';
	 },100);
	});
	let mens = document.querySelectorAll("#Modal");
	if (!mens) return;
	mens.forEach(function(v) {
	 var timer = setTimeout(function(){
	  if (v.id == menid || rt || ri) return;
	   document.getElementById('rModal').style.display = 'none';
	 },100);
	});
}

$(document).ready(function(){
	$('#linkToTop').on('click',function(e){
		e.preventDefault();
		$('html,body').scrollTop(0);
	});

	$(document).on("click",".up",function(e){
		$("html,body").animate({scrollTop:$("h1").scrollTop()},{duration:500});
		e.preventDefault();
	});

	$(document).on("click",".down",function(e){
		$("html,body").animate({scrollTop:$(".footer").position().top},{duration:500});
		e.preventDefault();
	});

	$("body").append(
		'<div class="up_down_div" style="z-index:10000;position: fixed; bottom: 220px; right: 10px; top: 333px;">'+
		'<div style="position:relative">'+
		'<div style="font-size:16px;position:absolute;top:-30px;right:0px">'+
		'<a href="#" class="up" style="color: rgba(0, 0, 0, 0.3) !important; "><div class="fas fa-chevron-circle-up">▲</div></a>'+
		'</div>'+
		'<div style="font-size:16px;position:absolute;top:+30px;right:0px">'+
		'<a href="#" class="down" style="color: rgba(0, 0, 0, 0.3) !important; "><div class="fas fa-chevron-circle-down">▼</div></a>'+
		'</div>'+
		'</div>'+
		'</div>'
	);
});

function morelist() {
    $.ajax({
        type: "GET",
 
        url: "/test/morelist.php?bbs="+bbs,
 
        cache: true,

        success: function (data) {
        	document.getElementById('more').innerHTML = data;
        },

        error: function () {
		return;
        }
    });
 
}

function headline() {
    $.ajax({
        type: "GET",
 
        url: "/test/headline.php?bbs="+bbs,
 
        cache: true,

        success: function (data) {
        	document.getElementById('headline').innerHTML = data;
        },

        error: function () {
		return;
        }
    });
 
}

function Num(n) {
document.getElementById('rModal').style.display = 'none';
if (!document.getElementById('postForm')) return;
if (n) document.getElementById('bbs-textarea').value += '>>'+n+'\n';
if (isSmartPhone() == true) {
 fopen();
 return;
}
 if (ankfixed == "true") {
     document.getElementById("isFixedForm").checked = true; 
     document.getElementById('postForm').style.backgroundColor = '#fff';
     document.getElementById('postForm').style.border = '1px outset #000';
     document.getElementById('postForm').style.position = 'fixed';
     document.getElementById('postForm').style.zIndex = '1';
     document.getElementById('postForm').style.bottom = '5px';
     document.getElementById('postForm').style.left = '10px';
 }
}

function Menu(n) {
document.getElementById('modal_text').innerHTML = '<a class="menulink" href="javascript:Num(\'\')">書き込み欄を開く</a>&emsp;<a class="menulink" href="javascript:Num(\''+n+'\')">&gt;&gt;'+n+' へ返信</a>&emsp;<div style="font-weight:bold;">NG設定</div><a class="menulink" href="javascript:mute(\'list\')">ID</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'ngword\')">Word</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'ngtitle\')">タイトル</a><div style="font-weight:bold;">レス情報コピー</div><a class="menulink" href="javascript:MenuClick(\'Copyr-'+n+'\')">レス</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'Copyur-'+n+'\')">URL+レス</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'Copytur-'+n+'\')">タイトル+URL+レス</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'Copyu-'+n+'\')">URL</a><div style="font-weight:bold;">スレッド</div><a class="menulink" href="/search/?q='+encodeURI(document.title.replace(/(★+.*|part+.*|Part+.*|\s[0-9０-９]+.*)/, ''))+'" target="search">関連スレ検索</a>&emsp;<a class="menulink" href="javascript:MenuClick(\'CreateThread\')">次スレッド作成</a><br><a class="menulink" href="javascript:MenuClick(\'CopyThreadLink\')">タイトルとスレッドURLをコピー</a><br><a class="menulink" href="javascript:MenuClick(\'CopyLink\')">スレッドURLをコピー</a><br><div style="font-weight:bold;">その他</div><a class="menulink" href="javascript:MenuClick(\'setting\')">閲覧設定</a>&emsp;<a class="menulink" href="/test/backimg.cgi">背景画像</a>&emsp;<a class="menulink" href="javascript:setclear()">全ログを削除</a><br><a class="menulink" href="//delight.rentalbbs.net/login.html">Googleでログイン</a>';
document.getElementById('rModal').style.display = 'block';
}

function ResAnchor(n,r) {
if (!document.getElementById('msg-'+r)) return;
if (!document.getElementById(n)) prev(getprev);
if (!document.getElementById('reply-'+r+'-'+n)) document.getElementById('msg-'+r).innerHTML = '<dl class="rep-comment" id="reply-'+r+'-'+n+'">'+document.getElementById(n).innerHTML+'</dl>'+document.getElementById('msg-'+r).innerHTML;
else document.getElementById('reply-'+r+'-'+n).style.display = 'block';
}

function ResAnchor2(a,b) {
if (!document.getElementById(a) || !document.getElementById(b)) return;
let d = b;
++d;
document.getElementById('modal_text').innerHTML = '';
 for (let c = a; c < d; c++) {
  if (document.getElementById(c) === null) break;
  if (document.getElementById(c)) document.getElementById('modal_text').innerHTML += document.getElementById(c).innerHTML;
 }
document.getElementById('rModal').style.display = 'block';
}

function HighLightId(ID,count,e) {
if (!document.getElementById(e) || !e) return;
			let idr = idlist[ID];
			let idcount;
			if (idr) idcount = idr.length;
			if (idcount > 1) document.getElementById(e).innerHTML = ID+'('+count+'/'+idcount+')';
}

function IdClick(ID,n) {
			let idr = idlist[ID];
			let idcount = idr.length;
			let ins = '<div><span style="font-weight:bold;">'+ID+'</span> '+idcount+'レス</div><div><a class="mbutton" href="javascript:mute(\''+ID+'\')" style="color:black;">ミュートする</a></div>'
			idr.forEach(function(value) {
			ins += '<div>'+document.getElementById(value).innerHTML+'</div>';
			});
			document.getElementById('modal_text').innerHTML = ins;
			document.getElementById('rModal').style.display = 'block';
}

function Iclose(a) {document.getElementById(a).style.display = 'none';}

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

function reload(st) {
	if (time() - localStorage.getItem('rtime') < 4) return;
	if (!st) st = LINENUM;
	let rscont = LINENUM;
	let newcount = 0;
	let request = new XMLHttpRequest();
	request.open('GET', '/test/get_res.cgi/' + bbs + '/' + key + '/' + st + '-n');
	request.timeout = 30 * 1000;
	request.send();
	request.onreadystatechange = () => {
		if(request.readyState === 4 && request.status === 200) {
			if (!document.getElementById('a-'+rscont)) {
			let a1 = document.createElement("a");
			a1.id = 'a-'+rscont;
			let mae = rscont;
			mae--;
			if (document.getElementById(mae)) document.getElementById(mae).after(a1);
			if (document.getElementById('a-'+rscont)) document.getElementById('a-'+rscont).setAttribute('name',rscont);
			}
			let data = request.responseText.split('\n');
			data.forEach(function(value) {
			if (value.indexOf('class="post"') == -1) return;
			let number = value.match(/<div class="post" id="([0-9]+)" data-date="NG"/);
			if (!number) return;
			number = number[1];
			if (rscont == number) return;
			let numtext = '<a href="javascript:Menu('+number+')" class="number" id="number-'+number+'">'+number+'</a>';
			let NG;
			let from,names;
			from = value.match(/<b>(.*)<\/b>/);
			if (from) names = from[1].split('</b>');
			let name = names[0];
			name = name.replace('<b>', '');
			if (isSmartPhone() == false) name = '<b>'+name+'</b>';
			let id2 = names[1];
			let id3 = names[2];
			let id4 = names[3];
			if (id2) {
			if (!NG) NG = MuteCheck(id2);
			id2 = nameid(id2,2,number);
			}
			if (id3) {
			if (!NG) NG = MuteCheck(id3);
			id3 = nameid(id3,3,number);
			}
			if (id4) {
			if (!NG) NG = MuteCheck(id4);
			id4 = nameid(id4,4,number);
			}
			let mailto = value.match(/<a href="mailto:(.+)"><b>/);
			let mail;
			if (value.indexOf('mailto:') != -1) mail = mailto[1];
			if (id2) name += ' '+id2;
			if (id3) name += ' '+id3;
			if (id4) name += ' '+id4;
			if (mail) name += ' ['+mail+']';
			let namecs = value.match(/<div id="name-[0-9]+" style="(.+)"><b>/);
			let namecss = '';
			if (namecs) namecss = namecs[1];
			if (namecss.indexOf('mailto:') != -1) namecss = namecss.match(/(.+)"><a href="mailto:/)[1];
			let nametext = '<span class="name" id="name-'+number+'" style="'+namecss+'">'+name+'</span>';
			let dateid = value.match(/id="date-[0-9]+">(.+)<\/div><div class="message"/);
			let dateids;
			if (dateid) dateids = dateid[1].split(' ');
			if (!dateids) return;
			let date = dateids[0]+' '+dateids[1];
			let id = [];
			if (dateids[2]) {
			if (!NG) NG = MuteCheck(dateids[2]);
			id[0] = ID(dateids[2],0,number);
			}
			if (dateids[3]) {
			if (!NG) NG = MuteCheck(dateids[3]);
			id[1] = ID(dateids[3],1,number);
			}
			if (dateids[4]) {
			if (!NG) NG = MuteCheck(dateids[4]);
			id[2] = ID(dateids[4],2,number);
			}
			if (dateids[5]) {
			if (!NG) NG = MuteCheck(dateids[5]);
			id[3] = ID(dateids[5],3,number);
			}
			let ids = '<span class="ids" id="ids-'+number+'">';
			if (id[0]) ids += ' '+id[0];
			if (id[1]) ids += ' '+id[1];
			if (id[2]) ids += ' '+id[2];
			if (id[3]) ids += ' '+id[3];
			ids += '</span>';
			date = date.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			let datetext;
			if (isSmartPhone() == true) datetext = '<span class="date" id="date-'+number+'">'+ids+date+'</span>';
			else datetext = '<span class="date" id="date-'+number+'">'+date+ids+'</span>';
			datetext = datetext.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			let mes = value.match(/<div class="message" id="msg-[0-9]+"> (.+) <\/div>/);
			let message;
			if (mes) message = mes[1];
			if (!message) return;
			let rnum = message.match(/&gt;&gt;([0-9]+)(?![-\d])/);
			if (rnum) rnum = rnum[1];
			if (ghide == "auto") {
			 if (message.indexOf('グロ') != -1 || message.indexOf('死ね') != -1) {
			  if (rnum) imghide(rnum);
			  imghide(number);
			 }
			}
			if (document.getElementById('back-'+rnum)) {
			document.getElementById('back-'+rnum).innerHTML += '<a class="back-link" href="javascript:void(0);">&gt;&gt;'+number+'</a>';
			let replycount = $('#back-'+rnum).children().length;
			if (replycount < 3) document.getElementById('number-'+rnum).style.color = '#518dc9';
			else if (replycount < 5) document.getElementById('number-'+rnum).style.color = '#a551c9';
			else if (replycount < 10) document.getElementById('number-'+rnum).style.color = 'darkred';
			else document.getElementById('number-'+rnum).style.color = 'darkgoldenrod';
			document.getElementById('rcount-'+rnum).innerHTML = replycount;
			document.getElementById('replys-'+rnum).style.display = "block";
			if (replycount == 3) plist.push(rnum);
			}
			let wiki = message.match(/.*(\[\[.+\]\]).*/);
			if (wiki) message = message.replace(wiki[1],          
                        function(){
			let a;
			   a = arguments[0].replace('[[','');
			   a = a.replace(']]','');
                            return '<a href="https://ja.wikipedia.org/wiki/'+a+'" title="'+a+'" target="_blank">'+a+'</a>';
                        });
			let msgtext = '<div class="message" id="msg-'+number+'">'+message+'</div>';
			let newpost = document.createElement("div");
			newpost.className = 'post';
			newpost.id = number;
			newpost.dataset.date = 'NG';
			newpost.dataset.userid = dateids[2];
			newpost.dataset.id = number;
			if (isSmartPhone() == true) newpost.innerHTML = numtext+nametext+msgtext+datetext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			else newpost.innerHTML = numtext+nametext+datetext+msgtext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			let mae = number;
			mae--;
			if (document.getElementById(mae)) document.getElementById(mae).after(newpost);
			else threaddata.appendChild(newpost);
			message = message.replace(/<b> \*/g,'<b> ');
			message = message.replace(/<i> _/g,'<i> ');
			message = message.replace(/<s> -/g,'<s> ');
			message = message.replace(/<font color="gray"> \&gt;/g,'<font color="gray"> ');
			message = message.replace(/<font color="green"> @/g,'<font color="green"> ');
			message = message.replace(/<small style="opacity: 0\.7;"> \^/g,'<small style="opacity: 0.7;"> ');
			message = message.replace(/<span class="_mfm_blur_"> ~/g,'<span class="_mfm_blur_"> ');
			message = message.replace(/<center> \\/g,'<center> ');
			if (message.indexOf('<span class="AA">') != -1) {
			message = message.replace('<span class="AA">','');
			message = message.replace('</span>','');
			document.getElementById('msg-'+number).className += " AA";
			}
			if (message.indexOf('data-lightbox="image"') != -1) imglist.push(number);
			document.getElementById('msg-'+number).innerHTML = message;
			if (!NG) NG = WordCheck(name+mail+message);
			if (NG) {
			Muten(number);
			document.getElementById('msg-'+number).style.display = "none";
			document.getElementById('date-'+number).style.display = "none";
			document.getElementById('name-'+number).innerHTML = 'あぼーん['+NG+']';
			}
			LINENUM = number;
			localStorage.setItem(bbs+key, LINENUM);
			newcount++;
			});
			if (newcount > 0) {
			 document.getElementById('ntxt').innerHTML = '新着 '+newcount+'件';
			 notice();
			 if (autoscroll == "true") $("html,body").animate({scrollTop:$('#'+rscont).position().top},{duration:500});
			}else if (areload != "true") {
			 document.getElementById('ntxt').innerHTML = '新着なし';
			 notice();
			}
			if (document.getElementById('reloadbutton')) {
			 document.getElementById('reloadbutton').setAttribute('onclick', 'reload('+LINENUM+')');
			 reloadbutton.href = '#'+LINENUM;
			}
			if (areload != "true") localStorage.setItem('rtime', time());
		}
	};
}

function prev(to,h) {
			if (!h) {
			 document.getElementById('prevbutton').style.display = 'none';
			 document.getElementById('prev-hide').innerHTML = '';
			}else {
			 document.getElementById('prev-hide').innerHTML = '.prev{display:none !important;}';
			}
if (preved) {
	if (!h) {
	document.getElementById('ntxt').innerHTML = '通信中';
	notice();
	}
return;
}
	preved = true;
	to--;
	document.getElementById('ntxt').innerHTML = '通信中';
	notice();
	let request = new XMLHttpRequest();
	request.open('GET', '/test/get_res.cgi/' + bbs + '/' + key + '/2-'+to+'n');
	request.timeout = 30 * 1000;
	request.send();
	request.onreadystatechange = () => {
		if(request.readyState === 4 && request.status === 200) {
			let data = request.responseText.split('\n');
			data.forEach(function(value) {
			if (value.indexOf('class="post"') == -1) return;
			let number = value.match(/<div class="post" id="([0-9]+)" data-date="NG"/);
			if (!number) return;
			number = number[1];
			if (to < number) return;
			let numtext = '<a href="javascript:Menu('+number+')" class="number" id="number-'+number+'">'+number+'</a>';
			let NG;
			let from,names;
			from = value.match(/<b>(.*)<\/b>/);
			if (from) names = from[1].split('</b>');
			let name = names[0];
			if (!name) return;
			name = name.replace('<b>', '');
			if (isSmartPhone() == false) name = '<b>'+name+'</b>';
			let id2 = names[1];
			let id3 = names[2];
			let id4 = names[3];
			if (id2) {
			if (!NG) NG = MuteCheck(id2);
			id2 = nameid(id2,2,number);
			}
			if (id3) {
			if (!NG) NG = MuteCheck(id3);
			id3 = nameid(id3,3,number);
			}
			if (id4) {
			if (!NG) NG = MuteCheck(id4);
			id4 = nameid(id4,4,number);
			}
			let mailto = value.match(/<a href="mailto:(.+)"><b>/);
			let mail;
			if (value.indexOf('mailto:') != -1) mail = mailto[1];
			if (id2) name += ' '+id2;
			if (id3) name += ' '+id3;
			if (id4) name += ' '+id4;
			if (mail) name += ' ['+mail+']';
			let namecs = value.match(/<div id="name-[0-9]+" style="(.+)"><b>/);
			let namecss = '';
			if (namecs) namecss = namecs[1];
			if (namecss.indexOf('mailto:') != -1) namecss = namecss.match(/(.+)"><a href="mailto:/)[1];
			let nametext = '<span class="name" id="name-'+number+'" style="'+namecss+'">'+name+'</span>';
			let dateid = value.match(/id="date-[0-9]+">(.+)<\/div><div class="message"/);
			let dateids;
			if (dateid) dateids = dateid[1].split(' ');
			if (!dateids) return;
			let date = dateids[0]+' '+dateids[1];
			let id = [];
			if (dateids[2]) {
			if (!NG) NG = MuteCheck(dateids[2]);
			id[0] = ID(dateids[2],0,number);
			}
			if (dateids[3]) {
			if (!NG) NG = MuteCheck(dateids[3]);
			id[1] = ID(dateids[3],1,number);
			}
			if (dateids[4]) {
			if (!NG) NG = MuteCheck(dateids[4]);
			id[2] = ID(dateids[4],2,number);
			}
			if (dateids[5]) {
			if (!NG) NG = MuteCheck(dateids[5]);
			id[3] = ID(dateids[5],3,number);
			}
			let ids = '<span class="ids" id="ids-'+number+'">';
			if (id[0]) ids += ' '+id[0];
			if (id[1]) ids += ' '+id[1];
			if (id[2]) ids += ' '+id[2];
			if (id[3]) ids += ' '+id[3];
			ids += '</span>';
			date = date.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			let datetext;
			if (isSmartPhone() == true) datetext = '<span class="date" id="date-'+number+'">'+ids+date+'</span>';
			else datetext = '<span class="date" id="date-'+number+'">'+date+ids+'</span>';
			datetext = datetext.replace('(日)', '(<span style="color:#C00;background:transparent;">日</span>)');
			let mes = value.match(/<div class="message" id="msg-[0-9]+"> (.+) <\/div>/);
			let message;
			if (mes) message = mes[1];
			if (!message) return;
			let rnum = message.match(/&gt;&gt;([0-9]+)(?![-\d])/);
			if (rnum) rnum = rnum[1];
			if (ghide == "auto") {
			 if (message.indexOf('グロ') != -1 || message.indexOf('死ね') != -1) {
			  if (rnum) imghide(rnum);
			  imghide(number);
			 }
			}
			if (document.getElementById('back-'+rnum)) {
			document.getElementById('back-'+rnum).innerHTML += '<a class="back-link" href="javascript:void(0);">&gt;&gt;'+number+'</a>';
			let replycount = $('#back-'+rnum).children().length;
			if (replycount < 3) document.getElementById('number-'+rnum).style.color = '#518dc9';
			else if (replycount < 5) document.getElementById('number-'+rnum).style.color = '#a551c9';
			else if (replycount < 10) document.getElementById('number-'+rnum).style.color = 'darkred';
			else document.getElementById('number-'+rnum).style.color = 'darkgoldenrod';
			document.getElementById('rcount-'+rnum).innerHTML = replycount;
			document.getElementById('replys-'+rnum).style.display = "block";
			if (replycount == 3) plist.push(rnum);
			}
			let wiki = message.match(/.*(\[\[.+\]\]).*/);
			if (wiki) message = message.replace(wiki[1],          
                        function(){
			let a;
			   a = arguments[0].replace('[[','');
			   a = a.replace(']]','');
                            return '<a href="https://ja.wikipedia.org/wiki/'+a+'" title="'+a+'" target="_blank">'+a+'</a>';
                        });
			let msgtext = '<div class="message" id="msg-'+number+'">'+message+'</div>';
			let newpost = document.createElement("div");
			newpost.className = 'post prev';
			newpost.id = number;
			newpost.dataset.date = 'NG';
			newpost.dataset.userid = dateids[2];
			newpost.dataset.id = number;
			if (isSmartPhone() == true) newpost.innerHTML = numtext+nametext+msgtext+datetext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			else newpost.innerHTML = numtext+nametext+datetext+msgtext+'<div id="replys-'+number+'" style="display:none;"><img class="aresicon" src="//delight.rentalbbs.net/static/ares.svg" width="12" height="12"><small id="rcount-'+number+'" class="rcount"></small> :<span id="back-'+number+'"></span></div>';
			let mae = number;
			mae--;
			if (document.getElementById(mae)) document.getElementById(mae).after(newpost);
			else document.getElementById('prevbutton').after(newpost);
			message = message.replace(/<b> \*/g,'<b> ');
			message = message.replace(/<i> _/g,'<i> ');
			message = message.replace(/<s> -/g,'<s> ');
			message = message.replace(/<font color="gray"> \&gt;/g,'<font color="gray"> ');
			message = message.replace(/<font color="green"> @/g,'<font color="green"> ');
			message = message.replace(/<small style="opacity: 0\.7;"> \^/g,'<small style="opacity: 0.7;"> ');
			message = message.replace(/<span class="_mfm_blur_"> ~/g,'<span class="_mfm_blur_"> ');
			message = message.replace(/<center> \\/g,'<center> ');
			if (message.indexOf('<span class="AA">') != -1) {
			message = message.replace('<span class="AA">','');
			message = message.replace('</span>','');
			document.getElementById('msg-'+number).className += " AA";
			}
			if (message.indexOf('data-lightbox="image"') != -1) imglist.push(number);
			document.getElementById('msg-'+number).innerHTML = message;
			if (!NG) NG = WordCheck(name+mail+message);
			if (NG) {
			Muten(number);
			document.getElementById('msg-'+number).style.display = "none";
			document.getElementById('date-'+number).style.display = "none";
			document.getElementById('name-'+number).innerHTML = 'あぼーん['+NG+']';
			}
			});
			getprev = false;
			if (!h) {
			 document.getElementById('prevbutton').style.display = 'none';
			 document.getElementById('prev-hide').innerHTML = '';
			}else {
			 document.getElementById('prev-hide').innerHTML = '.prev{display:none !important;}';
			}
		}
	};
}
function ID(d, n, num) {
			did = d.replace('ID:', '@');
			let idr = idlist[did];
			let idcount;
			if (idr) idcount = idr.length + 1;
			else {
			idcount = 1;
			idr = [];
			}
			if (idcount == 1) id = '<a class="id" href="javascript:IdClick(\''+did+'\','+num+')">'+did+'</a>';
			else if (idcount < 3) id = '<a class="id" href="javascript:IdClick(\''+did+'\','+num+')" style="color: #518dc9 !important;">'+did+'('+idcount+')</a>';
			else if (idcount < 5) id = '<a class="id" href="javascript:IdClick(\''+did+'\','+num+')" style="color: #a551c9 !important;">'+did+'('+idcount+')</a>';
			else if (idcount < 10) id = '<a class="id" href="javascript:IdClick(\''+did+'\','+num+')" style="color: darkred !important;">'+did+'('+idcount+')</a>';
			else id = '<a class="id" href="javascript:IdClick(\''+did+'\','+num+')" style="color: darkgoldenrod !important;">'+did+'('+idcount+')</a>';
			idr[idcount-1] = num;
			idlist[did] = idr;
			return id;
}

function nameid(nameid, a, num) {
			let slip, slip_name, slip_ip, slip_ua, ip, ncolor;
			if (isSmartPhone() == true) ncolor = 'color: #4d4d4d;';
			else ncolor = 'color: #0e0e6e;';
			nameid = nameid.replace('<b> ', '');
			nameid = nameid.replace('<b>', '');
			nameid = nameid.replace(')', '');
			nameid = nameid.replace('(', '');
			nameid = nameid.replace('[', '');
			nameid = nameid.replace(']', '');
			if (nameid.indexOf(' ') != -1) {
			let bbs_slip = nameid.split(' ');
			slip_name = bbs_slip[0];
			if (bbs_slip[1].indexOf('-') != -1) {
			slip = true;
			let slip_sub = bbs_slip[1].split('-');
			slip_ip = slip_sub[0];
			slip_ua = slip_sub[1];
			}
			else ip = bbs_slip[1];
			if (!ip) ip = bbs_slip[2];
			}
			if (!slip_name) {
			let idr = idlist[nameid];
			let idcount;
			if (idr) idcount = idr.length + 1;
			else {
			idcount = 1;
			idr = [];
			}
			idr[idcount-1] = num;
			idlist[nameid] = idr;
			if (idcount == 1) nameid = '(<a class="id id2" href="javascript:IdClick(\''+nameid+'\','+num+')" style="'+ncolor+'">'+nameid+'</a>)';
			else nameid = '(<a class="id id2" href="javascript:IdClick(\''+nameid+'\','+num+')" style="'+ncolor+'">'+nameid+'('+idcount+')</a>)';
			}
			else if (slip_name && ip && slip_ip) {
			let idr1 = idlist[ip];
			let idcount1, idcount2;
			if (idr1) idcount1 = idr1.length + 1;
			else {
			idcount1 = 1;
			idr1 = [];
			}
			idr1[idcount1-1] = num;
			idlist[ip] = idr1;
			let idr2 = idlist[slip_ip+'-'+slip_ua];
			if (idr2) idcount2 = idr2.length + 1;
			else {
			idcount2 = 1;
			idr2 = [];
			}
			idr2[idcount2-1] = num;
			idlist[slip_ip+'-'+slip_ua] = idr2;
			if (idcount1 == 1 && idcount2 == 1) nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'</a> <a class="id" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'</a>)';
			else if (idcount2 == 1) nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'</a> <a class="id" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'('+idcount1+')</a>)';
			else if (idcount1 == 1) nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'('+idcount2+')</a> <a class="id" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'</a>)';
			else nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'('+idcount2+')</a> <a class="id" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'('+idcount1+')</a>)';
			}
			else if (slip_name && ip) {
			let idr = idlist[ip];
			let idcount;
			if (idr) idcount = idr.length + 1;
			else {
			idcount = 1;
			idr = [];
			}
			if (idcount == 1) nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'</a>)';
			else nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+ip+'\','+num+')" style="'+ncolor+'">'+ip+'('+idcount+')</a>)';
			idr[idcount-1] = num;
			idlist[ip] = idr;
			}
			else if (slip_name && slip_ip) {
			let idr = idlist[slip_ip+'-'+slip_ua];
			let idcount;
			if (idr) idcount = idr.length + 1;
			else {
			idcount = 1;
			idr = [];
			}
			idr[idcount-1] = num;
			idlist[slip_ip+'-'+slip_ua] = idr;
			if (idcount == 1) nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'</a>)';
			else nameid = '('+slip_name+' <a class="id id2" href="javascript:IdClick(\''+slip_ip+'-'+slip_ua+'\','+num+')" style="'+ncolor+'">'+slip_ip+'-'+slip_ua+'('+idcount+')</a>)';
			}
			else {
			let idr = idlist[slip_name];
			let idcount;
			if (idr) idcount = idr.length + 1;
			else {
			idcount = 1;
			idr = [];
			}
			idr[idcount-1] = num;
			idlist[slip_name] = idr;
			if (idcount == 1) nameid = '(<a class="id id2" href="javascript:IdClick(\''+slip_name+'\','+num+')" style="'+ncolor+'">'+slip_name+'</a>)';
			else nameid = '(<a class="id id2" href="javascript:IdClick(\''+slip_name+'\','+num+')">'+slip_name+'('+idcount+')</a>)';
			}
			return nameid;
}

function mute(target) {
	if (target == 'list') {
	let mlisthtml = '<div style="font-weight:bold;">NGID</div><input type="text" id="addmute"><button onclick="AddM()">追加</button>&emsp;<button onclick="mute(\'reset\')">リセット</button><br>※クリックすると解除されます<br>';
			for (let i = 0; i < mutelist.length; i++) {
			mlisthtml += '<a class="menulink" href="javascript:unmute(\''+mutelist[i]+'\')">'+mutelist[i]+'</a>&emsp;';
			}
	document.getElementById('modal_text').innerHTML = mlisthtml;
	document.getElementById('rModal').style.display = 'block';
	return;
	}
	if (target == 'reset') {
			mutelist = [];
			mutejson = JSON.stringify(mutelist, undefined, 1);
			localStorage.setItem('mutelist', mutejson);
			document.getElementById('ntxt').innerHTML = 'リセットしました';
			notice();
	return;
	}
			let a;
			for (let i = 0; i < mutelist.length; i++) {
			if (target == mutelist[i]) {
			a = true;
			break;
			}
			}
			if (a == true) return;
			let mutecount = mutelist.length + 1;
			mutelist[mutecount-1] = target;
			mutejson = JSON.stringify(mutelist, undefined, 1);
			localStorage.setItem('mutelist', mutejson);
			document.getElementById('ntxt').innerHTML = 'ミュートしました';
			notice();
}

function AddM() {
			let target = document.getElementById('addmute').value;
			let a;
			for (let i = 0; i < mutelist.length; i++) {
			if (target == mutelist[i]) {
			a = true;
			break;
			}
			}
			if (a == true) return;
			let mutecount = mutelist.length + 1;
			mutelist[mutecount-1] = target;
			mutejson = JSON.stringify(mutelist, undefined, 1);
			localStorage.setItem('mutelist', mutejson);
			document.getElementById('ntxt').innerHTML = '追加しました';
			notice();
}

function unmute(target) {
			let a;
			for (let i = 0; i < mutelist.length; i++) {
			if (target == mutelist[i]) {
			mutelist[i] = '';
			break;
			}
			}
			mutejson = JSON.stringify(mutelist, undefined, 1);
			localStorage.setItem('mutelist', mutejson);
			document.getElementById('ntxt').innerHTML = 'ミュートを解除しました';
			notice();
}

function MuteCheck(target) {
			let N;
			for (let i = 0; i < mutelist.length; i++) {
			if (!mutelist[i]) continue;
			let NG = target.match(mutelist[i]);
			if (NG) {
			 N = mutelist[i];
			 break;
			}
			}
			if (N) return N;
}

function WordCheck(target) {
			let N;
			for (let i = 0; i < nglist.length; i++) {
			if (!nglist[i]) continue;
			let NG = target.match(nglist[i]);
			if (NG) {
			 N = nglist[i];
			 break;
			}
			}
			if (N) return 'Word:'+N;
}

function rclose() {
	document.getElementById('rModal').style.display = 'none';
	document.getElementById('modal_text').innerHTML = '';
}

function MenuClick(val) {
if (val.indexOf('Copyr-') != -1) {
	   document.getElementById('rModal').style.display = 'none';
	let n = val.replace('Copyr-', '');
  if (navigator.clipboard) {
	let dg = document.getElementById('date-'+n).innerText;
	let id = document.getElementById('ids-'+n).innerText;
	let d1 = dg.replace(id, '');
	let d2;
	if (id.length > 5) d2 = d1.replace(/\([0-9]+.*\)/, '');
	else d2 = d1;
	let date = d2.replace(/\n/, '');
	let d = date.trim()+' '+id.trim();
	let text = n+' '+document.getElementById('name-'+n).innerText+' '+d+'\n'+document.getElementById('msg-'+n).innerText;
   navigator.clipboard.writeText(text).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}

if (val.indexOf('Copyur-') != -1) {
	   document.getElementById('rModal').style.display = 'none';
	let n = val.replace('Copyur-', '');
  if (navigator.clipboard) {
	let dg = document.getElementById('date-'+n).innerText;
	let id = document.getElementById('ids-'+n).innerText;
	let d1 = dg.replace(id, '');
	let d2;
	if (id.length > 5) d2 = d1.replace(/\([0-9]+.*\)/, '');
	else d2 = d1;
	let date = d2.replace(/\n/, '');
	let d = date.trim()+' '+id.trim();
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/'+n;
	let text = url+'\n'+n+' '+document.getElementById('name-'+n).innerText+' '+d+'\n'+document.getElementById('msg-'+n).innerText;
   navigator.clipboard.writeText(text).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}

if (val.indexOf('Copy4-') != -1) {
	   document.getElementById('rModal').style.display = 'none';
	let n = val.replace('Copy4-', '');
  if (navigator.clipboard) {
	let dg = document.getElementById('date-'+n).innerText;
	let id = document.getElementById('ids-'+n).innerText;
	let d1 = dg.replace(id, '');
	let d2;
	if (id.length > 5) d2 = d1.replace(/\([0-9]+.*\)/, '');
	else d2 = d1;
	let date = d2.replace(/\n/, '');
	let d = date.trim()+' '+id.trim();
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/'+n;
	let text = url+' '+d;
   navigator.clipboard.writeText(text).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}

if (val.indexOf('Copytur-') != -1) {
	   document.getElementById('rModal').style.display = 'none';
	let n = val.replace('Copytur-', '');
  if (navigator.clipboard) {
	let dg = document.getElementById('date-'+n).innerText;
	let id = document.getElementById('ids-'+n).innerText;
	let d1 = dg.replace(id, '');
	let d2;
	if (id.length > 5) d2 = d1.replace(/\([0-9]+.*\)/, '');
	else d2 = d1;
	let date = d2.replace(/\n/, '');
	let d = date.trim()+' '+id.trim();
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/'+n;
	let text = document.title+'\n'+url+'\n'+n+' '+document.getElementById('name-'+n).innerText+' '+d+'\n'+document.getElementById('msg-'+n).innerText;
   navigator.clipboard.writeText(text).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}

if (val.indexOf('Copyu-') != -1) {
	   document.getElementById('rModal').style.display = 'none';
	let n = val.replace('Copyu-', '');
  if (navigator.clipboard) {
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/'+n;
   navigator.clipboard.writeText(url).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}

if (val == "CreateThread") {
if (!document.getElementById('msg-1')) {
			document.getElementById('ntxt').innerHTML = '次スレッド作成は>>1が表示されている場合のみ使用できます';
			notice();
}
let nextsubject = document.title;
if (nextsubject.match(/(\d+)/)) nextsubject = nextsubject.replace(/(\d+)/,           
                        function(){
                            return ++arguments[1];
                        });
else nextsubject += ' Part2';
document.getElementById('modal_text').innerHTML = '<div style="font-weight:bold;">次スレッド作成</div><form method="POST" id="create-post" action="/test/bbs.cgi?captcha=true"><input type="submit" value="新規スレッド作成" name="submit"><br>スレッドタイトル：<input type="text" name="subject" style="min-width: 35em;" value="'+nextsubject+'"><br>名前：<input type="text" name="FROM" style="width: 10em;" value="'+getCookie("NAME")+'"> E-mail：<input type="text" name="mail" style="width: 10em;" value="'+getCookie("MAIL")+'"> <label class="noselect" title="スレをsageで作成"><input value="sage" type="checkbox" name="mail">sage</label><br><textarea style="min-width: 30em; height: 10.0em; word-wrap: break-word;" rows="4" cols="12" name="MESSAGE">'+document.getElementById('msg-1').innerText+'\n\n'+document.title+'\nhttps://'+location.host+'/test/read.html/'+bbs+'/'+key+'/</textarea><input type="hidden" name="bbs" value="'+bbs+'"><input type="hidden" name="time" value="'+time()+'"></form>';
document.getElementById('rModal').style.display = 'block';
return;
}
if (val == "CopyThreadLink") {
	   document.getElementById('rModal').style.display = 'none';
  if (navigator.clipboard) {
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/';
	let text = document.title+'\n'+url;
   navigator.clipboard.writeText(text).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}
if (val == "CopyLink") {
	   document.getElementById('rModal').style.display = 'none';
  if (navigator.clipboard) {
	let url = 'https://'+location.host+'/test/read.html/'+bbs+'/'+key+'/';
   navigator.clipboard.writeText(url).then(function () {
  			document.getElementById('ntxt').innerHTML = 'コピーしました';
			notice();
   })
  }else {
			document.getElementById('ntxt').innerHTML = 'コピーできません';
			notice();
  }
return;
}
if (val == "picture") {
			let imgcount = imglist.length;
			let html = '';
			html += '<div><span style="font-weight:bold;">画像レス</span> '+imgcount+'件</div>'
			imglist.forEach(function(value) {
			html += document.getElementById(value).innerHTML;
			});
document.getElementById('modal_text').innerHTML = html;
document.getElementById('rModal').style.display = 'block';
return;
}
if (val == "popular") {
			let pcount = plist.length;
			let html = '';
			html += '<div><span style="font-weight:bold;">人気レス</span> '+pcount+'件</div>'
			plist.forEach(function(value) {
			html += document.getElementById(value).innerHTML;
			});
document.getElementById('modal_text').innerHTML = html;
document.getElementById('rModal').style.display = 'block';
return;
}
if (val == "setting") {
let sbcheck,arecheck,gurocheck,autocheck,gcheck,rcheck,darkcheck;
if (subback == "true") sbcheck = 'checked';
if (areload == "true") arecheck = 'checked';
if (autoscroll == "true") autocheck = 'checked';
if (ghide == "all") gcheck = 'checked';
if (ghide == "auto") gurocheck = 'checked';
if (cgimode == "true") rcheck = 'checked';
if (darkmode == "true") darkcheck = 'checked';
document.getElementById('modal_text').innerHTML = '<div class="option_style_2">閲覧設定</div><div class="option_style_3">&emsp;</div><div class="option_style_4"><div class="option_style_5"><input class="option_style_6" '+spcheck+' id="spmode" type="checkbox">スマホ版スレッド表示</div><div class="option_style_5"><input class="option_style_6" '+sbcheck+' id="sbmode" type="checkbox">スマホ版スレッド一覧</div><div class="option_style_5"><input class="option_style_6" '+darkcheck+' id="darkmode" type="checkbox">ダークモード</div><div class="option_style_5"><input class="option_style_6" '+arecheck+' id="arecheck" type="checkbox">5秒間隔で自動更新する</div><div class="option_style_5"><input class="option_style_6" '+autocheck+' id="autoscroll" type="checkbox">新着投稿の位置まで自動スクロール</div><div class="option_style_5"><input class="option_style_6" '+gurocheck+' id="g_hide" type="checkbox">注意のある画像を自動的に非表示</div><div class="option_style_5"><input class="option_style_6" '+gcheck+' id="a_hide" type="checkbox">画像のサムネイル表示をオフにする</div><div class="option_style_5"><input class="option_style_6" '+rcheck+' id="usereadcgi" type="checkbox">常にread.cgiで表示(クラシック版)</div></div><div class="option_style_11"><button id="saveOptions" class="option_style_12" onclick="setoption()">変更を保存</button><button id="cancelOptions" class="option_style_13" onclick="rclose()">キャンセル</button></div>';
document.getElementById('rModal').style.display = 'block';
return;
}
if (val == "ngword") {
	let nlisthtml = '<div style="font-weight:bold;">NGワード</div>※クリックすると解除されます<br>';
	nlisthtml += '<input type="text" id="addngword"><button onclick="NGWORD()">追加</button>&emsp;<button onclick="unngword(\'reset\')">リセット</button><br>'
			for (let i = 0; i < nglist.length; i++) {
			nlisthtml += '<a class="menulink" href="javascript:unngword(\''+nglist[i]+'\')">'+nglist[i]+'</a>&emsp;';
			}
	document.getElementById('modal_text').innerHTML = nlisthtml;
	document.getElementById('rModal').style.display = 'block';
return;
}
if (val == "ngtitle") {
	let nlisthtml = '<div style="font-weight:bold;">NGタイトル</div>※クリックすると解除されます<br>';
	nlisthtml += '<input type="text" id="addngtitle"><button onclick="NGTITLE()">追加</button>&emsp;<button onclick="unngtitle(\'reset\')">リセット</button><br>'
			for (let i = 0; i < ntlist.length; i++) {
			nlisthtml += '<a class="menulink" href="javascript:unngtitle(\''+ntlist[i]+'\')">'+ntlist[i]+'</a>&emsp;';
			}
	document.getElementById('modal_text').innerHTML = nlisthtml;
	document.getElementById('rModal').style.display = 'block';
return;
}
}

function setoption() {
	let ghide,readcgi,ngword;
	if (document.getElementById('g_hide').checked == true) ghide = 'auto';
	if (document.getElementById('a_hide').checked == true) ghide = 'all';
	localStorage.setItem('ghide', ghide);
	if (document.getElementById('usereadcgi').checked == true) readcgi = true;
	else readcgi = false;
	localStorage.setItem('cgimode', readcgi);
	if (document.getElementById('arecheck').checked == true) areload = true;
	else areload = false;
	localStorage.setItem('areload', areload);
	if (document.getElementById('darkmode').checked == true) darkmode = true;
	else darkmode = false;
	localStorage.setItem('darkmode', darkmode);
	if (document.getElementById('spmode').checked == true) viewer = 'sp';
	else viewer = 'pc';
	localStorage.setItem('viewer', viewer);
	if (document.getElementById('sbmode').checked == true) subback = true;
	else subback = false;
	localStorage.setItem('subback', subback);
	if (document.getElementById('autoscroll').checked == true) autoscroll = true;
	else autoscroll = false;
	localStorage.setItem('autoscroll', autoscroll);
	rclose();
}

function NGWORD() {
			let target = document.getElementById('addngword').value;
			let a;
			for (let i = 0; i < nglist.length; i++) {
			if (target == nglist[i]) {
			a = true;
			break;
			}
			}
			if (a == true) return;
			let ngcount = nglist.length + 1;
			nglist[ngcount-1] = target;
			ngjson = JSON.stringify(nglist, undefined, 1);
			localStorage.setItem('nglist', ngjson);
			document.getElementById('ntxt').innerHTML = '追加しました';
			notice();
}

function NGTITLE() {
			let target = document.getElementById('addngtitle').value;
			let a;
			for (let i = 0; i < ntlist.length; i++) {
			if (target == ntlist[i]) {
			a = true;
			break;
			}
			}
			if (a == true) return;
			let ntcount = ntlist.length + 1;
			ntlist[ntcount-1] = target;
			ntjson = JSON.stringify(ntlist, undefined, 1);
			localStorage.setItem('ngtitle', ntjson);
			document.getElementById('ntxt').innerHTML = '追加しました';
			notice();
}

function unngword(target) {
	if (target == 'reset') {
			nglist = [];
			ngjson = JSON.stringify(nglist, undefined, 1);
			localStorage.setItem('nglist', ngjson);
			document.getElementById('ntxt').innerHTML = 'リセットしました';
			notice();
	return;
	}
			let a;
			for (let i = 0; i < nglist.length; i++) {
			if (target == nglist[i]) {
			nglist[i] = '';
			break;
			}
			}
			ngjson = JSON.stringify(nglist, undefined, 1);
			localStorage.setItem('nglist', ngjson);
			document.getElementById('ntxt').innerHTML = '解除しました';
			notice();
}

function unngtitle(target) {
	if (target == 'reset') {
			ntlist = [];
			ntjson = JSON.stringify(ntlist, undefined, 1);
			localStorage.setItem('ngtitle', ntjson);
			document.getElementById('ntxt').innerHTML = 'リセットしました';
			notice();
	return;
	}
			let a;
			for (let i = 0; i < ntlist.length; i++) {
			if (target == ntlist[i]) {
			ntlist[i] = '';
			break;
			}
			}
			ntjson = JSON.stringify(ntlist, undefined, 1);
			localStorage.setItem('ntlist', ngjson);
			document.getElementById('ntxt').innerHTML = '解除しました';
			notice();
}

function Muten(number) {
document.getElementById('mute').innerHTML += '.tv-'+number+'{display:none !important;}';
}

function imghide(n) {
document.getElementById('mute').innerHTML += '.img-'+n+'{display:none !important;}';
}

function Report(val) {
let url = 'https://'+location.host+'/test/read.cgi/'+bbs+'/'+key+'/';
if (val != "thread") {
url += val;
val = '&gt;&gt;'+val;
}
else val = 'スレッド';
document.getElementById('modal_text').innerHTML = '<div style="font-weight:bold;">通報('+val+')</div><form method="POST" id="report-post" action="/test/bbs.cgi?captcha=true"><div style="display:table-cell;padding:5px;margin:5px;">理由：<select name="FROM" style="width: 100%;padding:10px;border-radius:5px;border: 1px solid #888888;"><option>荒らし・スパム</option><option>誹謗中傷</option><option>個人情報</option><option>宣伝・業者</option><option>掲示板・スレッドの趣旨とは違う投稿</option><option>連続投稿・重複</option><option>エログロ不快な画像</option><option>荒らし依頼</option><option>差別・蔑視</option><option>違法な情報</option><option>児童ポルノ</option><option>その他</option></select></div> E-mail：<input type="text" name="mail" style="min-width: 25em"> <br>タイトル・URL・備考：<textarea style="min-width: 30em; height: 10.0em; word-wrap: break-word;" rows="4" cols="12" name="MESSAGE">'+document.title+'\n'+url+'\n</textarea><input type="hidden" name="bbs" value="saku"><input type="hidden" name="key" value="9000000001"><br><input type="submit" value="書き込む" name="submit"></form>';
document.getElementById('rModal').style.display = 'block';
}

function notice() {
	if (document.getElementById('notific').style.display != "none") return;
			document.getElementById('notific').style.display = "block";
			document.getElementById('notific').style.opacity = 1;
			$("#notific").fadeTo(3000, 0, closenotice);
}
function closenotice() {
	document.getElementById('notific').style.display = "none";
}

function upload() {
  const preview = document.querySelector('img');
  const file = document.querySelector('input[type=file]').files[0];
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    base64Url = reader.result;
    base64 = base64Url.replace(new RegExp('data.*base64,'), '');
	imgur();
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
	/// APIに渡すときは先頭の data:~~~base64 を除外

function imgur() {
 document.getElementById('ntxt').innerHTML = '通信中';
 notice();
$.ajax({
  url: 'https://api.imgur.com/3/image',
  method: 'POST',
  headers: {
	"Authorization": 'Client-ID x'
  },
  data: {
    image: base64,
    type: 'base64'
  },
  success: function(r){
	imgurlink = r.data.link
	document.getElementById('bbs-textarea').value += '\n'+imgurlink; 
	document.getElementById('ntxt').innerHTML = '画像をアップロードしました';
	notice();
  },

  error: function () {
	document.getElementById('ntxt').innerHTML = 'アップロードできません';
	notice();
  }
});

}

}

function time() {
var date = new Date();
var a = date.getTime();
return Math.floor(a / 1000);
}

function FixedForm() {
    if (document.getElementById("isFixedForm").checked) {
     localStorage.setItem('formfixed', true);
     document.getElementById('postForm').style.backgroundColor = '#fff';
     document.getElementById('postForm').style.border = '1px outset #000';
     document.getElementById('postForm').style.position = 'fixed';
     document.getElementById('postForm').style.zIndex = '1';
     document.getElementById('postForm').style.padding = '5px';
	if (isSmartPhone() == true) {
     document.getElementById('postForm').style.bottom = '0';
     document.getElementById('postForm').style.left = '0';
	}else {
     document.getElementById('postForm').style.bottom = '5px';
     document.getElementById('postForm').style.left = '10px';
	}
    } else {
     localStorage.setItem('formfixed', false);
     document.getElementById('postForm').style.backgroundColor = '';
     document.getElementById('postForm').style.border = '';
     document.getElementById('postForm').style.bottom = '';
     document.getElementById('postForm').style.position = '';
     document.getElementById('postForm').style.zIndex = '';
     document.getElementById('postForm').style.right = '';
     document.getElementById('postForm').style.padding = '';
     document.getElementById('bbs-textarea').style.height = '';
  }
}

function MSG() {
 if (document.getElementById('bbs-textarea').value) {
  sessionStorage.setItem('text', document.getElementById('bbs-textarea').value);
  localStorage.setItem('text2', document.getElementById('bbs-textarea').value);
 }
}
function BackMSG() {
 document.getElementById('bbs-textarea').value = localStorage.getItem('text2');
}
function fopen() {
 document.getElementById('postForm').style.display = 'block';
}
function fclose() {
 document.getElementById('postForm').style.display = 'none';
}
function setclear() {
 localStorage.clear();
 sessionStorage.clear();
 document.getElementById('ntxt').innerHTML = '完了';
 notice();
}