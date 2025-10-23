<?php
header("Content-type: text/html; charset=Shift_JIS");
$NOWTIME = time();
$BBQSERV = "/virtual/oyster356s/public_html/rentalbbs/";	#格納鯖のパス
$r = explode('?',$_SERVER['REQUEST_URI']);
$a = explode('q=',$r[1]);
$q = $a[1];
$q = urldecode($q);
if (is_utf8($q) === true) $q = mb_convert_encoding($q, 'SJIS-win', 'UTF-8');
$q = str_replace("?","",$q);
$q = trim($q);
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="Shift_JIS" />
<meta content="レンタル掲示板delightスレタイ検索 <?=$q?>の検索結果 <?=$q?>とは" name="description" />
<meta name="keywords" content="スレタイ検索,無料レンタル掲示板,スレタイ,検索,2ch,delight">
<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport" />
<title><?=$q?> - スレタイ検索[無料レンタル掲示板 delight]</title>
<link href="https://kakiko.org/bbs/s.css" rel="stylesheet" type="text/css">
<style>
body {font-size: 14px}
.container {margin-right: auto;margin-left: auto;padding-left: 15px;padding-right: 15px}
.thread {word-wrap: break-word;overflow-wrap: break-word;margin-bottom: 20px}
.title{font-size:16px}
.meta{font-size:14px}
a{text-decoration:none;color:#1a98ff}
a:hover, a:focus {color: #23527c;text-decoration: underline}
a:visited{color:#9b4dca}
.ita{color:#070}
.time{color:#ababab}
.mae{color:#990900}
.ikioi{color:#d27b7a}
.orange {text-decoration: none;color: #fe642e;font-weight: 700}
.footer {
	padding-top: 200px;
}
@media (min-width: 768px){.container {
	width: 750px;
}}
@media (min-width: 992px){.container {
	width: 970px;
}}
</style>
</head>
<body>
<script>
	if (localStorage.getItem('darkmode') === null) localStorage.setItem('darkmode', false);
	darkmode = localStorage.getItem('darkmode');
	if (darkmode == "true") document.body.innerHTML += '<link href="https://rentalbbs.net/css/dark.css" rel="stylesheet"><link href="https://rentalbbs.net/css/d.css" rel="stylesheet">';
</script>
<form method="GET" action="./" accept-charset="Shift_JIS"><div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="width:200px !important;"><a href="https://rentalbbs.net/"><img src="https://rentalbbs.net/logo.png"></a></div><div class="search-input"><input value="<?=$q?>" id="search-text" type="text" name="q" placeholder="キーワードを入力"><button id="search-button"><img src="https://rentalbbs.net/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><a href="https://rentalbbs.net/login.html"><div class="search-setting dropdown"><img class="dropBtnSetting settingDrop" src="https://rentalbbs.net/static/icon_login.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop"><span>ログイン</span></span></div></a></div><div class="search-clear"></div></div></form>
<div class="container">
<? if (!$q) { ?>
<div class="modal-content">
<div class="modal-header">
<h4 class="modal-title" id="helpModalLabel">スレッドタイトル検索ヘルプ</h4></div>
<div class="modal-body">
<p>・スペース → 両方を含む</p>
<p>・OR → どちらかを含む</p>
<p>・NOT → 含まない</p>
<p>・@○○ → 板名を部分一致で検索</p>
<p>・板名は板IDか板タイトルが検索対象になります</p>
<p>・例: スマホアプリ板の板IDは「applism」、板タイトルが「スマホアプリ」のため、 @スマホ @アプリ @apliのどれでもヒットします</p>
<p>・NOTで特定の板からの検索を除外できます</p>
<p>・最大1000件まで表示されます</p>
<p>・例: "経済 NOT @ニュース" →ニュースを含む板以外からの検索</p>
</div>
</div>
<?
exit;
}
$file = $BBQSERV."threads.txt";
$LOG = file($file);
krsort($LOG);
$s = 1;
$original = $q;
$q = str_replace('　', ' ', $q);
if (strpos($q, '&') !== false) list($q,$qa) = explode("&",$q);
if (strpos($q, ' ') !== false) list($q,$qa) = explode(" ",$q);
if (strpos($q, 'NOT ') !== false) list($q,$qn) = explode("NOT ",$q);
if (strpos($q, 'OR ') !== false) list($q,$qo) = explode("OR ",$q);
if (strpos($q, ' ') !== false) list($q,$qa) = explode(" ",$q);
$qi = str_replace('@', '', $q);
$qj = str_replace('@', '', $qa);
$qk = str_replace('@', '', $qn);
$ql = str_replace('@', '', $qo);
foreach($LOG as $tmp){
	list($bbs,$key,$title,$board,$d) = explode("<>",$tmp);
	if (!$d) $d = $_SERVER[HTTP_HOST];
	$BBASERV = "/virtual/bbs3ch/public_html/".$d."/";	#格納鯖のパス
	$found = false;
	if (stristr($title, $q) !== false) $found = true;
	if (strpos($q, '@') !== false and (stristr($bbs, $qi) !== false or stristr($board, $qi) !== false)) $found = true;
	if ($qo) {
	 if (stristr($title, $qo) !== false) $found = true;
	 if (strpos($qo, '@') !== false and (stristr($bbs, $ql) !== false or stristr($board, $ql) !== false)) $found = true;
	}
	if ($qa) {
	 if (strpos($qa, '@') !== false) {
	  if (stristr($bbs, $qj) === false and stristr($board, $qj) === false) $found = false;
	 }elseif (stristr($title, $qa) === false) $found = false;
	}
	if ($qn) {
	 if (strpos($qn, '@') !== false) {
	  if (stristr($bbs, $qk) === false and stristr($board, $qk) === false) $found = false;
	 }elseif (stristr($title, $qn) === false) $found = false;
	}
	if (!$found) continue;
	$DATE = date("Y/m/d H:i", $key);
	$time = filemtime($BBASERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi");
	$res = count(file($BBASERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi"));
	#時間
	if ($time) {
	$time = $NOWTIME - $time;
	 if ($time < 60) $time .= "秒";
	 elseif ($time < 3600) {
	 $time = floor($time / 60);
	 $time .= "分";
	 }
	 elseif ($time < 86400) {
	 $time = floor($time / 3600);
	 $time .= "時間";
	 }
	 else {
	 $time = floor($time / 86400);
	 $time .= "日";
	 }
	}
	# 勢い
	$a = $NOWTIME - $key;
	$b = $res / $a;
	$ikioi = round($b * 86400,1);
	if ($ikioi > 99) $ikioi = floor($ikioi);
	echo '<div class="thread"><div class="title"><a href="https://'.$d.'/test/read.html/'.$bbs.'/'.$key.'/l10/?ls=10">'.$title.' ('.$res.')</a></div><div class="meta"><a href="https://'.$d.'/'.$bbs.'/" class="ita">'.$board.'</a>　<span class="time">'.$DATE.'</span>　<span class="mae">'.$time.'</span>　<span class="ikioi">'.$ikioi.'/日</span></div></div>';
	++$s;
	if ($s > 1000) break;
}
if ($s == 1) { ?>
<div class="notfound"><b class="notfound_word"><?=$original?></b>に一致するスレッドは見つかりませんでした。
<div class="notfound_hint">検索のヒント:</div>
<ul>
<li>キーワードに誤字・脱字がないか確認します。</li>
<li>別のキーワードを試してみます。</li>
<li>もっと一般的なキーワードに変えてみます。</li>
</ul>
</div>
<? } ?>
</div>
</body>
</html>
<? exit; ?>