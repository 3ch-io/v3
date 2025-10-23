<?php
header("Content-type: text/html; charset=UTF-8");
$NOWTIME = time();
$BBQSERV = "/virtual/oyster356s/public_html/rentalbbs/";	#格納鯖のパス
$r = explode('?',$_SERVER['REQUEST_URI']);
$a = explode('q=',$r[1]);
$q = $a[1];
$q = urldecode($q);
?>
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title><?=$q?> - 本文検索 / かきこ</title>
<link href="/bbs/st.css" rel="stylesheet" type="text/css"><link href="/bbs/milligram.css" rel="stylesheet" type="text/css">
<link href="/bbs/s.css" rel="stylesheet" type="text/css">
<link href="/bbs/read.css" rel="stylesheet" type="text/css">
<style>
@media only screen and (max-width: 670px) {
.search-right {margin-top:-60px !important;}
.search-logo {min-width:100px;}
}
</style>

<body><section class="section"><section id="body">
<form method="GET" action="" accept-charset="Shift_JIS"><div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="font-size:15px !important;"></div><div class="search-input"><input value="<?=$q?>" id="search-text" type="text" name="q" placeholder="キーワードを入力" style="height:25pt"><button id="search-button"><img src="https://rentalbbs.net/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><a href="https://rentalbbs.net/login.html"><div class="search-setting dropdown"><img class="dropBtnSetting settingDrop" src="https://rentalbbs.net/static/icon_login.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop"><span>ログイン</span></span></div></a></div><div class="search-clear"></div></div></form>
<script>
if (localStorage.getItem('darkmode') == "true") document.getElementById('body').innerHTML += '<link href="https://rentalbbs.net/css/dark.css" rel="stylesheet"><link href="https://rentalbbs.net/css/d.css" rel="stylesheet">';
if (localStorage.getItem('backimg')) {
	if (localStorage.getItem('darkmode') == "true") document.getElementById('body').innerHTML += '<style>#body{position: relative;background-color: rgba(38,38,38,0.75) !important}.section {position: relative;} .section:before { content: ""; display: block;  position: fixed;  top: 0;  left: 0;  width: 100%;  height: 100vh;  background: url('+localStorage.getItem('backimg')+') center top no-repeat;  background-size: 100% auto;}.asetting_4,.topmenu,.title,.thread,.cLength,.newposts,.bottommenu{background-color: transparent !important;}</style>';
	else document.getElementById('body').innerHTML += '<style>#body{position: relative;background-color: rgba(250,250,250,0.75) !important}.section {position: relative;} .section:before { content: ""; display: block;  position: fixed;  top: 0;  left: 0;  width: 100%;  height: 100vh;  background: url('+localStorage.getItem('backimg')+') center top no-repeat;  background-size: 100% auto;}.asetting_4,.topmenu,.title,.thread,.cLength,.newposts,.bottommenu{background-color: transparent !important;}</style>';
}
</script>
<div class="topmenu"><a class="menuitem" href="https://rentalbbs.net/">delight</a><a class="menuitem" href="/search/">スレタイ検索</a><a class="menuitem" href="#" onclick="window.history.go(-1);">前ページに戻る</a><a class="menuitem" href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a></div>
<hr><div class="thread">
<? if (!$q) { ?>
<div class="modal-content">
<div class="modal-header">
<h4 class="modal-title" id="helpModalLabel">本文検索ヘルプ</h4></div>
<div class="modal-body">
<p>・スペース → 両方を含む</p>
<p>・OR → どちらかを含む</p>
<p>・NOT → 含まない</p>
<p>・@○○ → 板名を部分一致で検索</p>
<p>・*○○ → スレッド名を部分一致で検索</p>
<p>・板名は板IDか板タイトルが検索対象になります</p>
<p>・スレッド名はスレッドkeyかスレッドタイトルが検索対象になります</p>
<p>・例: スマホアプリ板の板IDは「applism」、板タイトルが「スマホアプリ」のため、 @スマホ @アプリ @apliのどれでもヒットします</p>
<p>・NOTで特定の板・スレッドからの検索を除外できます</p>
<p>・最大300件まで表示されます</p>
<p>・例: "経済 NOT @ニュース" →ニュースを含む板以外からの検索</p>
<p>・例: "経済 *日本" →日本を含むスレッドからの検索</p>
</div>
</div>
<?
exit;
}
$file = $BBQSERV."find.txt";
$LOG = file($file);
krsort($LOG);
$s = 1;
$original = $q;
$q = str_replace('　', ' ', $q);
if (strpos($q, 'NOT ') !== false) list($q,$qn) = explode("NOT ",$q);
if (strpos($q, 'OR ') !== false) list($q,$qo) = explode("OR ",$q);
if (strpos($q, ' ') !== false) list($q,$qa) = explode(" ",$q);
$target = array('@', '*');
$qi = str_replace($target, '', $q);
$qj = str_replace($target, '', $qa);
$qk = str_replace($target, '', $qn);
$ql = str_replace($target, '', $qo);
foreach($LOG as $tmp){
	list($bbs,$key,$title,$board,$d,$msg,$time) = explode("<>",$tmp);
	if (!$d) $d = $_SERVER[HTTP_HOST];
	$found = false;
	if (stristr($msg, $q) !== false) $found = true;
	if (strpos($q, '@') !== false and (stristr($bbs, $qi) !== false or stristr($board, $qi) !== false)) $found = true;
	if (strpos($q, '*') !== false and (stristr($key, $qi) !== false or stristr($title, $qi) !== false)) $found = true;
	if ($qo) {
	 if (stristr($msg, $qo) !== false) $found = true;
	 if (strpos($qo, '@') !== false and (stristr($bbs, $ql) !== false or stristr($board, $ql) !== false)) $found = true;
	 if (strpos($qo, '*') !== false and (stristr($key, $ql) !== false or stristr($title, $ql) !== false)) $found = true;
	}
	if ($qa) {
	 if (strpos($qa, '@') !== false) {
	  if (stristr($bbs, $qj) === false and stristr($board, $qj) === false) $found = false;
	 }elseif (strpos($qa, '*') !== false) {
	  if (stristr($key, $qj) === false and stristr($title, $qj) === false) $found = false;
	 }elseif (stristr($msg, $qa) === false) $found = false;
	}
	if ($qn) {
	 if (strpos($qn, '@') !== false) {
	  if (stristr($bbs, $qk) === false and stristr($board, $qk) === false) $found = false;
	 }elseif (strpos($qn, '*') !== false) {
	  if (stristr($key, $qk) === false and stristr($title, $qk) === false) $found = false;
	 }elseif (stristr($msg, $qn) === false) $found = false;
	}
	if (!$found) continue;
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
	echo '<div class="post"><span class="number">'.$s.'</span><span class="name"><a href="https://'.$d.'/test/read.html/'.$bbs.'/'.$key.'/l10/?ls=10">'.$title.'</a> - <a href="https://'.$d.'/'.$bbs.'/">'.$board.'</a></span><div class="message">'.$msg.'</div><div class="date">'.$DATE.'</div></div>';
	++$s;
	if ($s > 300) break;
}
if ($s == 1) { ?>
<div class="notfound"><b class="notfound_word"><?=$original?></b>に一致する投稿は見つかりませんでした。
<div class="notfound_hint">検索のヒント:</div>
<ul>
<li>キーワードに誤字・脱字がないか確認します。</li>
<li>別のキーワードを試してみます。</li>
<li>もっと一般的なキーワードに変えてみます。</li>
</ul>
</div>
<? } ?>
</div>
<script src="https://rentalbbs.net/js/lightbox.js"></script>
<div class="bottommenu"><a class="menuitem" href="https://rentalbbs.net/">delight</a><a class="menuitem" href="/search/">スレタイ検索</a><a class="menuitem" href="#" onclick="window.history.go(-1);">前ページに戻る</a><a class="menuitem" href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a></div>
<div class="footer push">Ver.20230531</div><?=$bh?>
</section></section>
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
if (isSmartPhone() == true) document.body.innerHTML += '<link href="https://rentalbbs.net/css/sp.css" rel="stylesheet" type="text/css">';
</script></body></html><? exit;
?>