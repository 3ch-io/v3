<?php
header("Content-type: text/html; charset=Shift_JIS");
$NOWTIME = time();
$BBQSERV = "/virtual/oyster356s/public_html/rentalbbs/";	#格納鯖のパス
$subject = mb_convert_encoding(urldecode($subbbs), 'SJIS-win', 'UTF-8');
$hashtag = mb_convert_encoding($subject, 'HTML-ENTITIES', 'SJIS-win');
#==================================================
#　おすすめ２ちゃんねる
#==================================================
#-------------------------------板毎	
	if (!file_exists($BBSSERV."/tmp/".$bbs.date('z'))) {
	#日付が変わった時の処理
    	@mkdir($BBSSERV."/tmp/".$bbs.date('z'), 0777, true);
	}
	#前日分を消去
	$maedz = date('z') - 1;
	if (file_exists($BBSSERV."/tmp/".$bbs.$maedz)) {
	$maedzs = $BBSSERV."/tmp/".$bbs.$maedz."/*.*";
    	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$bbs.$maedz);
	}
	if (date('z') != 364 and file_exists($BBSSERV."/tmp/".$bbs."364")) {
	$maedzs = $BBSSERV."/tmp/".$bbs."364/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$bbs."364");
	}
	if (date('z') != 365 and file_exists($BBSSERV."/tmp/".$bbs."365")) {
	$maedzs = $BBSSERV."/tmp/".$bbs."365/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$bbs."365");
	}
	if (date('z') != 366 and file_exists($BBSSERV."/tmp/".$bbs."366")) {
	$maedzs = $BBSSERV."/tmp/".$bbs."366/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$bbs."_366");
	}
	$b_file = $BBSSERV."/tmp/".$bbs.date('z')."/b_".$hashtag.".cgi";
	if (!is_file($b_file)) @touch($b_file);
	$b = file($b_file);
if ($_COOKIE['b']) {
list($bb,$bk,$bs,$bt,$be) = explode("<>",$_COOKIE['b']);
 if ($bb and $bk and $bs and $bt and $be) {
	if ($bk != $key) {
	 foreach($b as $tmp) {
	 list(,$bka,) = explode("<>",$tmp);
	 if ($bka == $bk) $already = true;
	 }
	if (!$already) array_unshift($b, $bb."<>".$bk."<>".$bs."<>".$bt."<>".$be."\n");
	}
	# 5 個以内に調整して保存
	while (count($b) > 5) array_pop($b);
	$RebuildL = array_unique($b);
 }
}
	if ($b[0]) $bh = "\n<hr>\n■ このスレを見ている人はこんなスレも見ています。<br>\n";
	$fp = '';
	foreach($b as $tmp) {
	list($bba,$bka,$bsa,$bta,$bea) = explode("<>",$tmp);
	$bh .= "<a href=\"https://$bea/test/read.html/$bba/$bka/l10/?ls=10\" title=\"$bsa\">$bsa</a> [$bta]<br>\n";
	$fp .= $tmp;
	}
if ($_COOKIE['b']) @file_put_contents($b_file, $fp, LOCK_EX);
?>
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><meta property="og:title" content="<?=$subject?> - レンタル掲示板delight"><meta name="og:description" content="スレッドフロート式高機能無料レンタル掲示板：delight。"><meta property="og:url" content="https://<?=$_SERVER['HTTP_HOST']?>/hashtag/<?=$subbbs?>/"><meta property="og:type" content="website"><meta property="og:site_name" content="レンタル掲示板delight"><link rel="apple-touch-icon" href="https://rentalbbs.net/icon.png"><link rel="icon" href="https://rentalbbs.net/favicon.ico"><script type="text/javascript" src="https://rentalbbs.net/js/jquery-1.11.3.min.js"></script><script type="text/javascript" src="https://rentalbbs.net/js/ad.js"></script>
<title>#<?=$subject?> | レンタル掲示板delight</title>
<link href="https://rentalbbs.net/css/st.css" rel="stylesheet" type="text/css"><link href="https://rentalbbs.net/css/milligram.css" rel="stylesheet" type="text/css">
<link href="https://rentalbbs.net/css/s.css" rel="stylesheet" type="text/css">
<link href="https://rentalbbs.net/css/read.css" rel="stylesheet" type="text/css">
<script>
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
if (isSmartPhone() == true) document.head.innerHTML += '<link href="https://rentalbbs.net/css/sp.css" rel="stylesheet" type="text/css">';
</script>
<style>
@media only screen and (max-width: 670px) {
.search-right {margin-top:-60px !important;}
.search-logo {min-width:100px;}
}
</style>
<script type="text/javascript" src="https://rentalbbs.net/js/t2.js"></script>
<link href="https://rentalbbs.net/css/lightbox.css" rel="stylesheet">
<script>
$(document).ready(function(){
	$('#linkToTop').on('click',function(e){
		e.preventDefault();
		$('html,body').scrollTop(0);
	});	

	$(document).on("click",".up",function(e){
		$("html,body").animate({scrollTop:$("#header").scrollTop()},{duration:500});
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
		'<a href="#" class="up" style="color: rgba(0, 0, 0, 0.3); "><div class="fas fa-chevron-circle-up">▲</div></a>'+
		'</div>'+
		'<div style="font-size:16px;position:absolute;top:+30px;right:0px">'+
		'<a href="#" class="down" style="color: rgba(0, 0, 0, 0.3); "><div class="fas fa-chevron-circle-down">▼</div></a>'+
		'</div>'+
		'</div>'+
		'</div>'
	);
});
</script>
<link href="https://rentalbbs.net/css/ad.css" rel="stylesheet" type="text/css"></head>
<body><section class="section"><section id="body">
<form method="GET" action="/search/" accept-charset="Shift_JIS"><div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="font-size:15px !important;"></div><div class="search-input"><input value="" id="search-text" type="text" name="q" placeholder="キーワードを入力" style="height:25pt"><button id="search-button"><img src="https://rentalbbs.net/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><a href="https://rentalbbs.net/login.html"><div class="search-setting dropdown"><img class="dropBtnSetting settingDrop" src="https://rentalbbs.net/static/icon_login.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop"><span>ログイン</span></span></div></a></div><div class="search-clear"></div></div></form>
<script>
if (localStorage.getItem('darkmode') == "true") document.getElementById('body').innerHTML += '<link href="https://rentalbbs.net/css/dark.css" rel="stylesheet"><link href="https://rentalbbs.net/css/d.css" rel="stylesheet">';
if (localStorage.getItem('backimg')) {
	if (localStorage.getItem('darkmode') == "true") document.getElementById('body').innerHTML += '<style>#body{position: relative;background-color: rgba(38,38,38,0.75) !important}.section {position: relative;} .section:before { content: ""; display: block;  position: fixed;  top: 0;  left: 0;  width: 100%;  height: 100vh;  background: url('+localStorage.getItem('backimg')+') center top no-repeat;  background-size: 100% auto;}.asetting_4,.topmenu,.title,.thread,.cLength,.newposts,.bottommenu{background-color: transparent !important;}</style>';
	else document.getElementById('body').innerHTML += '<style>#body{position: relative;background-color: rgba(250,250,250,0.75) !important}.section {position: relative;} .section:before { content: ""; display: block;  position: fixed;  top: 0;  left: 0;  width: 100%;  height: 100vh;  background: url('+localStorage.getItem('backimg')+') center top no-repeat;  background-size: 100% auto;}.asetting_4,.topmenu,.title,.thread,.cLength,.newposts,.bottommenu{background-color: transparent !important;}</style>';
}
</script>
<div class="topmenu"><a class="menuitem" href="https://rentalbbs.net/">delight</a><a class="menuitem" href="#" onclick="window.history.go(-1);">前ページに戻る</a><a class="menuitem" href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a></div>
<hr>
<h1 class="title">#<?=$subject?></h1><div class="thread">
<?
$file = $BBQSERV."/hashtag/".$hashtag.".txt";
$LOG = file($file);
krsort($LOG);
$s = 1;
$all = 1;
foreach($LOG as $tmp){
	++$all;
	list($time,$bbs,$key,$msg,$title,$host) = explode("<>",$tmp);
	$msg = str_replace('<b> *', '<b> ', $msg);
	$msg = str_replace('<i> _', '<i> ', $msg);
	$msg = str_replace('<s> -', '<s> ', $msg);
	$msg = str_replace('<font color="gray"> &gt;', '<font color="gray"> ', $msg);
	$msg = str_replace('<font color="green"> @', '<font color="green"> ', $msg);
	$msg = str_replace('<small style="opacity: 0.7;"> ^', '<small style="opacity: 0.7;"> ', $msg);
	$msg = str_replace('<center> \\', '<center> ', $msg);
	$msg = str_replace('<img src="https://', '<img src="//', $msg);
	$msg = str_replace('<img src="http://', '<img src="//', $msg);
	$msg = str_replace('<a href="https://', '<a href="//', $msg);
	$msg = str_replace('<a href="http://', '<a href="//', $msg);
	$msg = str_replace('align="left"', '', $msg);
	$msg = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $msg);
	$msg = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $s;
  	  $url = $m[0];
	$url = preg_replace("/(ttps?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
   	       if (preg_match('/https?:\S+(gif|jpg|jpeg|tiff|png|webp)/', $url)) {
   	     return "<a href=\"$url\" data-lightbox=\"image\">$url<br><img class=\"image img-$s\" src=\"$url\" width=\"65\" height=\"65\"></a>";
  	  }elseif(strpos($url, 'youtube.com/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "=")+1));	
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
  	  }elseif(strpos($url, 'm.youtube.com/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "=")+1));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
  	  }elseif(strpos($url, 'youtu.be/') !== false){
	$youtubeurl = substr($url, (strpos($url, "youtu.be/")+9));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'youtube.com/shorts') !== false){
	$youtubeurl = substr($url, (strpos($url, "shorts/")+7));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'youtube.com/live') !== false){
	$youtubeurl = substr($url, (strpos($url, "live/")+5));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'nicovideo.jp/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "watch/")+6));
	$youtubeurl = substr($youtubeurl, 0, 10);
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"560\" height=\"315\" src=\"https://embed.nicovideo.jp/watch/$youtubeurl?persistence=1&amp;oldScript=1&amp;referer=https%3A%2F%2F3chan.jp%2F&amp;from=0&amp;allowProgrammaticFullScreen=1\" style=\"max-width: 100%;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'nico.ms/') !== false){
	$youtubeurl = substr($url, (strpos($url, "nico.ms/")+8));	
	$youtubeurl = substr($youtubeurl, 0, 10);
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"560\" height=\"315\" src=\"https://embed.nicovideo.jp/watch/$youtubeurl?persistence=1&amp;oldScript=1&amp;referer=https%3A%2F%2F3chan.jp%2F&amp;from=0&amp;allowProgrammaticFullScreen=1\" style=\"max-width: 100%;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'twitcasting.tv/') !== false){
	$youtubeurl = substr($url, (strpos($url, "twitcasting.tv/")+15));
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"560\" height=\"315\" src=\"https://twitcasting.tv/$youtubeurl/embeddedplayer/live?auto_play=false&default_mute=false\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'www.tiktok.com/') !== false){
	$youtubeurl = substr($url, (strpos($url, "video/")+6));
	$youtubeurl = substr($youtubeurl, 0, 19);
  	      return "<iframe class=\"viewon\" width=\"320\" height=\"550\" src=\"https://www.tiktok.com/embed/$youtubeurl\" _src=\"https://www.tiktok.com/embed/$youtubeurl\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'www.instagram.com/p/') !== false){
  	      return "<iframe class=\"instagram-media instagram-media-rendered\" id=\"instagram-embed-12\" src=\"{$url}embed/?cr=1&amp;\" allowtransparency=\"true\" allowfullscreen=\"true\" frameborder=\"0\" height=\"500\" data-instgrm-payload-id=\"instagram-media-payload-12\" scrolling=\"no\" style=\"background-color: white; border-radius: 3px; border: 1px solid rgb(219, 219, 219); box-shadow: none; display: block; margin: 0px 0px 12px; min-width: 326px; padding: 0px;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'www.instagram.com/reel/') !== false){
		$youtubeurl = substr($url, (strpos($url, "reel/")+5));
	        $youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe class=\"instagram-media instagram-media-rendered\" id=\"instagram-embed-12\" src=\"https://www.instagram.com/p/".$youtubeurl."/embed/?cr=1&amp;\" allowtransparency=\"true\" allowfullscreen=\"true\" frameborder=\"0\" height=\"500\" data-instgrm-payload-id=\"instagram-media-payload-12\" scrolling=\"no\" style=\"background-color: white; border-radius: 3px; border: 1px solid rgb(219, 219, 219); box-shadow: none; display: block; margin: 0px 0px 12px; min-width: 326px; padding: 0px;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\">$url</a>";
	}elseif(strpos($url, 'twitter.com/') !== false and strpos($url, '/status/') !== false) {
	     $twitterurl = substr($url, (strpos($url, "status/")+7));
	     $twitterurl = substr($twitterurl, 0, 19);
	     $rurl = str_replace("/","%2F",$_SERVER[HTTP_HOST].$_SERVER[REQUEST_URI]);
   	     return '<div class="twitter-tweet twitter-tweet-rendered" style="display: flex; max-width: 550px; width: 100%; margin-bottom: 10px;"><iframe id="twitter-widget-0" scrolling="no" allowtransparency="true" allowfullscreen="true" class="" style="position: static; visibility: visible; width: 550px; min-height: 550px; display: block; flex-grow: 1;" title="Twitter Tweet" src="https://platform.twitter.com/embed/Tweet.html?dnt=false&amp;embedId=twitter-widget-0&amp;features=eyJ0ZndfdGltZWxpbmVfbGlzdCI6eyJidWNrZXQiOltdLCJ2ZXJzaW9uIjpudWxsfSwidGZ3X2ZvbGxvd2VyX2NvdW50X3N1bnNldCI6eyJidWNrZXQiOnRydWUsInZlcnNpb24iOm51bGx9LCJ0ZndfdHdlZXRfZWRpdF9iYWNrZW5kIjp7ImJ1Y2tldCI6Im9uIiwidmVyc2lvbiI6bnVsbH0sInRmd19yZWZzcmNfc2Vzc2lvbiI6eyJidWNrZXQiOiJvbiIsInZlcnNpb24iOm51bGx9LCJ0ZndfbWl4ZWRfbWVkaWFfMTU4OTciOnsiYnVja2V0IjoidHJlYXRtZW50IiwidmVyc2lvbiI6bnVsbH0sInRmd19leHBlcmltZW50c19jb29raWVfZXhwaXJhdGlvbiI6eyJidWNrZXQiOjEyMDk2MDAsInZlcnNpb24iOm51bGx9LCJ0ZndfZHVwbGljYXRlX3NjcmliZXNfdG9fc2V0dGluZ3MiOnsiYnVja2V0Ijoib24iLCJ2ZXJzaW9uIjpudWxsfSwidGZ3X3ZpZGVvX2hsc19keW5hbWljX21hbmlmZXN0c18xNTA4MiI6eyJidWNrZXQiOiJ0cnVlX2JpdHJhdGUiLCJ2ZXJzaW9uIjpudWxsfSwidGZ3X2xlZ2FjeV90aW1lbGluZV9zdW5zZXQiOnsiYnVja2V0Ijp0cnVlLCJ2ZXJzaW9uIjpudWxsfSwidGZ3X3R3ZWV0X2VkaXRfZnJvbnRlbmQiOnsiYnVja2V0Ijoib24iLCJ2ZXJzaW9uIjpudWxsfX0%3D&amp;frame=false&amp;hideCard=false&amp;hideThread=false&amp;id='.$twitterurl.'&amp;lang=en&amp;origin=https%3A%2F%2F'.$rurl.'&amp;sessionId=a9d4d113f56d7d35c5da4aa01b7ee15e6bdeb19a&amp;theme=light&amp;widgetsVersion=aaf4084522e3a%3A1674595607486&amp;width=550px" data-tweet-id="'.$twitterurl.'" frameborder="0"></iframe></div><a href="'.$url.'">'.$url.'</a>';
  	  }elseif(preg_match('/https?:\S+\.mp4/', $url)){
  	      return "<video src=\"$url\" width=\"560\" height=\"315\" playsinline=\"\" controls=\"\"></video><br><a href=\"$url\">$url</a>";
	}elseif(preg_match('/https?/', $url) and preg_match('/(2ch\.net|5ch\.net|bbspink\.com|rentalbbs\.net|pinktower\.com)/', $url)){
		$url = str_replace("2ch.net", "5ch.net", $url);
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"noopener noreferrer\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $msg);
	#日付
if ($time) {
$time = substr($time, 0, 10);	#unixtime
$today = getdate($time);
$JIKAN = $today['hours'];
$DATE = date("y/m/d H:i:s", $time);
}else $DATE = '';
	echo '<div class="post"><span class="number">'.$s.'</span><span class="name"><a href="https://'.$host.'/test/read.html/'.$bbs.'/'.$key.'/l10/?ls=10">'.$title.'</a></span><div class="message">'.$msg.'</div><div class="date">'.$DATE.'</div></div>';
	++$s;
}
?>
</div>
<hr>
<script src="https://rentalbbs.net/js/lightbox.js"></script>
<div class="bottommenu"><a class="menuitem" href="https://rentalbbs.net/">delight</a><a class="menuitem" href="#" onclick="window.history.go(-1);">前ページに戻る</a><a class="menuitem" href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a></div>
<div class="footer push">Ver.20230604</div><?=$bh?>
</section></section></body></html><? exit;
?>