<?php
header("Content-type: text/html; charset=Shift_JIS");
$st = $to = 0;
$nofirst = '';
$ls = 0;
#==================================================
#　時刻を設定
#==================================================
$NOW = time();
$today = getdate(); 
$JIKAN = $today['hours']; 
#==================================================
#　リクエスト解析
#==================================================
if ($_SERVER['REQUEST_METHOD'] != 'GET') push();
$pairs = explode('/',$_SERVER['REQUEST_URI']);
	$bbs = $pairs[3];
	$key = $pairs[4];
	if (!empty($pairs[5])) {
		if (strstr($pairs[5], 'n')) {
			$nofirst = 'true';
			$pairs[5] = str_replace("n","",$pairs[5]);
		}
		if (substr($pairs[5], 0, 1) == 'l') {
			$ls = substr($pairs[5],1);
		}
		elseif (strstr($pairs[5], '-')) {
			list($st, $to) = explode('-',$pairs[5]);
			if (!$st) $st = 1;
		}
		else {
			$st = $pairs[5];
			$to = $pairs[5];
			$nofirst = 'true';
		}
	}
	if (!$bbs) push();
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
$BBSSERV = "/virtual/banana356s/public_html/".$_SERVER['HTTP_HOST']."/";	#格納鯖のパス
preg_match("/(.*)(\/test\/read\.cgi)(.*)/", $_SERVER['SCRIPT_NAME'], $match);
$URL = 'https://'.$_SERVER['HTTP_HOST'].$match[1];
$SCRIPT = $match[2];
$BASEURL = "$URL/$bbs/";
#if(!file_exists($BBSSERV.$bbs."/")) nodat();
#if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/")) nodat();
#if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/")) nodat();
#スレッドの場所
$thread_file = $BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi";
if (!is_file($thread_file)) nodat();
$subjectfile = $BBSSERV.$bbs."/subject.txt";
#告知欄
$kokuti = @file_get_contents($BBSSERV.$bbs."/kokuti.txt");
#==================================================
#　表示範囲の決定
#==================================================
$LOG = file($thread_file);
$LINENUM = count($LOG);
$s = 1;
$mae = 0;
$END = $LINENUM;
if ($to and is_numeric($to) and $to < $LINENUM) $END = $to;
if ($st and is_numeric($st)) $s = ($st < $LINENUM) ? $st : $LINENUM;
if ($ls) {
	preg_match("/^(\d+)/", $ls, $match);
	$s = $LINENUM - $match[1] + 2;
	if ($nofirst == 'true') $s--;
}
if ($s < 1) $s = 1;
if ($s > 1) $mae = $s-1;
$fsize = (int)(filesize($thread_file) / 1024);
list($num,,,,,,,$subject,$threadinfo,) = explode("<>",$LOG[0]);
	if ($num == "saku") nodat();
	if ($num == "del" || strpos($num, "del") !== false) {
		$subject='あぼーん';
	}
#スレッド設定をSETTINGに反映
$SETT = unserialize($threadinfo);
foreach ($SETT as $keys => $value) $SETTING[$keys] = $value;
if (!$SETTING['MAX_RES']) $SETTING['MAX_RES'] = 1000;
if ($SETTING['MAX_RES'] > 2000) $SETTING['MAX_RES'] = 2000;
if ($SETTING['MAX_RES'] < 300) $SETTING['MAX_RES'] = 300;
if (($live or $SETTING['LIVE_THREAD']) and $SETTING['MAX_RES'] > 1000) $SETTING['MAX_RES'] = 1000;
#######################################################################
# dat落ちを検出
#######################################################################
$subss = @file($subjectfile);
	if ($subss) {
		foreach ($subss as $tmp){
		list($k1,,$r1,) = explode("<>", $tmp);
		if ($k1 == $key) $isdat = true;
		if ($r1 > 5) ++$tc;
		}
	}
#if (!$isdat) $stop = true;
# 停止済みスレッド
if ($SETTING['THREAD_STOP'] == "yes") $stop = true;
# 即死判定
#if (!$SETTING['BBS_TH_LINE']) $SETTING['BBS_TH_LINE'] = 1;
#if (!$SETTING['TIME_TO_LIVE']) $SETTING['TIME_TO_LIVE'] = 1209600;
#if ($NOW > $key + $SETTING['TIME_TO_LIVE'] and $SETTING['BBS_TH_LINE'] > $LINENUM) $stop = true;
# 突然死判定
#if ($live and !$SETTING['BBS_MAX_MODIFIED']) $SETTING['BBS_MAX_MODIFIED'] = 18000;
#if ($SETTING['BBS_MAX_MODIFIED'] and $NOW > filemtime($thread_file) + $SETTING['BBS_MAX_MODIFIED']) $stop = true;
# lifetimeルール
#if ($SETTING['BBS_THREAD_LIFETIME'] and $NOW > $key + $SETTING['BBS_THREAD_LIFETIME']) $stop = true;
# 最大レス数超え
if ($LINENUM >= $SETTING['MAX_RES']) $maxover = $SETTING['MAX_RES'];
# 最大レス数近い
if ($LINENUM >= $SETTING['MAX_RES'] - 50) $maxout = $SETTING['MAX_RES'] - 50;
#==================================================
#　出力
#==================================================
?><!DOCTYPE HTML>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><meta property="og:title" content="<?=$subject?> - <?=$SETTING[BBS_TITLE]?> - レンタル掲示板delight"><meta name="og:description" content="スレッドフロート式高機能無料レンタル掲示板：delight。"><meta property="og:url" content="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/"><meta property="og:type" content="website"><meta property="og:site_name" content="レンタル掲示板delight"><link rel="apple-touch-icon" href="https://dream.kakiko.org/icon.png"><link rel="icon" href="https://dream.kakiko.org/favicon.ico"><script type="text/javascript" src="https://dream.kakiko.org/js/jquery-1.11.3.min.js"></script><script type="text/javascript" src="https://dream.kakiko.org/js/ad.js"></script><script type="text/javascript" src="https://dream.kakiko.org/js/index.js"></script><script type="text/javascript" src="https://dream.kakiko.org/js/active.js"></script><title><?=$subject?>
</title><link href="https://dream.kakiko.org/css/ad.css" rel="stylesheet" type="text/css">
<link href="https://dream.kakiko.org/css/s.css" rel="stylesheet" type="text/css"><link href="https://dream.kakiko.org/css/style.css" rel="stylesheet" type="text/css">
<style>
body{background-color:<?=$SETTING['BBS_THREAD_COLOR']?>;color:<?=$SETTING['BBS_TEXT_COLOR']?>;}a{color:<?=$SETTING['BBS_LINK_COLOR']?>;}a:visited{color:<?=$SETTING['BBS_VLINK_COLOR']?>;}a:hover{color:<?=$SETTING['BBS_ALINK_COLOR']?>;}.message{color:<?=$SETTING['BBS_TEXT_COLOR']?>;}.name{color:<?=$SETTING['BBS_NAME_COLOR']?>;}
</style>
<script language="JavaScript"><!-- 
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
//--></script>
</head><body><input type="hidden" id="zxcvtypo" value="http://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>"><div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="font-size:15px !important;"><?=$SETTING['BBS_TITLE']?></div><div class="search-input"><input value="" id="search-text" type="text" name="q" placeholder="キーワードを入力"><button id="search-button"><img src="https://delight.kakiko.org/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><div class="search-setting dropdown"><a href="javascript:void(0)" id="options"><img class="dropBtnSetting settingDrop" src="https://delight.kakiko.org/static/icon_settings.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop"><span class="dropBtnSetting">設定</span><img class="dropBtnSetting" src="https://delight.kakiko.org/static/icon_extend.png" style="margin-left:5px;margin-bottom:2px;"></span></a></div></div><div class="search-clear"></div></div><div class="topmenu"><a class="menuitem" href="https://delight.kakiko.org/">delight</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/">全部</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/-100">1-</a><?php for ($iCnt = 100; $iCnt <= $LINENUM; $iCnt += 100){
	$iTo = $iCnt + 99;
	echo "<a class=\"menuitem\" href=\"/test/read.cgi/$bbs/$key/$iCnt-$iTo\">$iCnt-</a>";
} ?><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/l50">最新50</a><a class="menuitem" href="javascript:switchReadJsMode();">read.htmlに切替える</a><hr></div><? if ($maxover) { ?><div class="stoplight">レス数が<?=$maxover?>を超えています。これ以上書き込みはできません。</div><?php }elseif ($stop) { ?><div class="stoplight">■ このスレッドは過去ログ倉庫に格納されています</div><?php }elseif ($maxout) { ?><div class="stoplight">レス数が<?=$maxout?>を超えています。<?=$SETTING[MAX_RES]?>を超えると書き込みができなくなります。</div><?php } ?><h1 class="title"><?=$subject?>
</h1><div class="thread"><?php
$i = 0;
$ncolor = '';
if (!$st) $st = $s;
if (!$to) $to = $LINENUM;
if ($nofirst != "true" or $st == 1) {
	list($num,$name,$mail,$time,$id,$message,$info,,$threadinfo,$reply,$spam,$sinki,$UID,$REMOTE_HOST,$REMOTE_ADDR,) = explode("<>",$LOG[0]);
if (!$name || strpos(substr($name, 0, 3), '</') !== FALSE) $name = $SETTING['BBS_NONAME_NAME'].$name;
if ($time) {
$time = substr($time, 0, 10);	#unixtime
$today = getdate($time);
$JIKAN = $today['hours'];
$DATE = date("y/m/d H:i:s", $time);
}else $DATE = '';
$id = trim($id);
if ($info) $resinfo = unserialize($info);
	if (!$message) {
		$name = "[ここ壊れてます](4)";
		$message = " [ここ壊れてます] ";
		$ncolor = "red";
	}
	if (!$DATE) $DATE = 'NG';
	if ($num == "del" || strpos($num, "del") !== false) {
		#レスが削除済みの場合
		$name='';
		$mail='';
		$DATE = 'NG';
		$id = '';
		$message=' '.$SETTING[DELETED_TEXT].' ';
	}
	$message = str_replace("rentalbbs.net", "kakiko.org", $message);
	$message = str_replace('<img src="https://', '<img src="//', $message);
	$message = str_replace('<img src="http://', '<img src="//', $message);
	$message = str_replace('<a href="https://', '<a href="//', $message);
	$message = str_replace('<a href="http://', '<a href="//', $message);
	$message = str_replace('align="left"', '', $message);
	$message = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $message);
	$message = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $s;
  	  $url = $m[0];
	$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
	if(preg_match('/https?/', $url) and preg_match('/rentalbbs\.net/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"nofollow noopener\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $message);
	$message = str_replace("<br>", " <br> ", $message);
	$message = preg_replace("/sssp:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<img class=\"image img-1\" src=\"https://$1\">", $message);
#レスアンカーをリンクに変換
$message = preg_replace_callback('/&gt;&gt;([0-9]+),?([0-9]+)?,?([0-9]+)?,?([0-9]+)?,?([0-9]+)?(?![-\d])/', function ($m) {
	global $bbs, $key;
	$anka = "<a href=\"/test/read.cgi/$bbs/$key/$m[1]\">&gt;&gt;$m[1]</a>";
	if ($m[2]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[2]\">&gt;&gt;$m[2]</a>";
	if ($m[3]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[3]\">&gt;&gt;$m[3]</a>";
	if ($m[4]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[4]\">&gt;&gt;$m[4]</a>";
	if ($m[5]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[5]\">&gt;&gt;$m[5]</a>";
	return $anka;
	}, $message);
$message = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	global $bbs, $key;
	return "<a href=\"/test/read.cgi/$bbs/$key/$m[1]-$m[2]\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $message);
	$mailto = $mail ? "<b><a href=\"mailto:$mail\">$name</a></b>" : "<b>$name</b>";
	# 名前の色
	if (strpos($DATE, "02/14") !== false) $ncolor = "#785f01";	#バレンタインデー
	if ($ncolor) $mailto = "<font color=\"".$ncolor."\">".$mailto."</font>";
	# レス出力
	echo "<div class=\"post\" id=\"1\" data-date=\"NG\" data-userid=\"$id\" data-id=\"1\"><div class=\"number\">1 : </div><div class=\"name\">$mailto</div><div class=\"date\">$DATE $id</div><div class=\"message\">$message</div></div><div id=\"banner\"><div class=\"push\"><div id=\"bannerLeft\"></div><div id=\"bannerRight\"></div><div class=\"push\"></div></div><div class=\"push\"></div></div>";
}
while ($s <= $END) {
	$ncolor = '';
	if ($s == 1) {
	$s++;
	continue;
	}
	list($num,$name,$mail,$time,$id,$message,$info,,$threadinfo,$reply,$spam,$sinki,$UID,$REMOTE_HOST,$REMOTE_ADDR,) = explode("<>",$LOG[$s-1]);
if (!$name || strpos(substr($name, 0, 3), '</') !== FALSE) $name = $SETTING['BBS_NONAME_NAME'].$name;
if ($time) {
$time = substr($time, 0, 10);	#unixtime
$today = getdate($time);
$JIKAN = $today['hours'];
$DATE = date("y/m/d H:i:s", $time);
}else $DATE = '';
$id = trim($id);
if ($info) $resinfo = unserialize($info);
	if (!$message) {
		$name = "[ここ壊れてます](4)";
		$message = " [ここ壊れてます] ";
		$ncolor = "red";
	}
	if (!$DATE) $DATE = 'NG';
	if ($num == "del" || strpos($num, "del") !== false) {
		#レスが削除済みの場合
		$name='';
		$mail='';
		$DATE = 'NG';
		$id = '';
		$message=' '.$SETTING[DELETED_TEXT].' ';
	}
	$message = str_replace("rentalbbs.net", "kakiko.org", $message);
	$message = str_replace('<img src="https://', '<img src="//', $message);
	$message = str_replace('<img src="http://', '<img src="//', $message);
	$message = str_replace('<a href="https://', '<a href="//', $message);
	$message = str_replace('<a href="http://', '<a href="//', $message);
	$message = str_replace('align="left"', '', $message);
	$message = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $message);
	$message = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $s;
  	  $url = $m[0];
	$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
	if(preg_match('/https?/', $url) and preg_match('/rentalbbs\.net/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"nofollow noopener\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $message);
	$message = str_replace("<br>", " <br> ", $message);
	$message = preg_replace("/sssp:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<img class=\"image img-1\" src=\"https://$1\">", $message);
#レスアンカーをリンクに変換
$message = preg_replace_callback('/&gt;&gt;([0-9]+),?([0-9]+)?,?([0-9]+)?,?([0-9]+)?,?([0-9]+)?(?![-\d])/', function ($m) {
	global $bbs, $key;
	$anka = "<a href=\"/test/read.cgi/$bbs/$key/$m[1]\">&gt;&gt;$m[1]</a>";
	if ($m[2]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[2]\">&gt;&gt;$m[2]</a>";
	if ($m[3]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[3]\">&gt;&gt;$m[3]</a>";
	if ($m[4]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[4]\">&gt;&gt;$m[4]</a>";
	if ($m[5]) $anka .= ",<a href=\"/test/read.cgi/$bbs/$key/$m[5]\">&gt;&gt;$m[5]</a>";
	return $anka;
	}, $message);
$message = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	global $bbs, $key;
	return "<a href=\"/test/read.cgi/$bbs/$key/$m[1]-$m[2]\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $message);
	$mailto = $mail ? "<b><a href=\"mailto:$mail\">$name</a></b>" : "<b>$name</b>";
	# 名前の色
	if (strpos($DATE, "02/14") !== false) $ncolor = "#785f01";	#バレンタインデー
	if ($ncolor) $mailto = "<font color=\"".$ncolor."\">".$mailto."</font>";
	# レス出力
	echo "<div class=\"post\" id=\"$s\" data-date=\"NG\" data-userid=\"$id\" data-id=\"$s\"><div class=\"number\">$s : </div><div class=\"name\">$mailto</div><div class=\"date\">$DATE $id</div><div class=\"message\">$message</div></div>";
	$s++;
}
$e = $END + 1;
$t = $END + 100;
$f = $st - 1;
$u = $f - 100;
if ($f < 1) $f = 1;
if ($u < 1) $u = 1;
$cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$bbs.$key.$NOW.$subject.$_SERVER['REMOTE_ADDR'].$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
?></div><div class="cLength"><?=$fsize?>KB</div><? if ($maxover) { ?><div class="stoplight">レス数が<?=$maxover?>を超えています。これ以上書き込みはできません。</div><?php }elseif ($stop) { ?><div class="stoplight">■ このスレッドは過去ログ倉庫に格納されています</div><? }else { ?><hr><div class="newposts"><div class="newpostbutton"><a href="/test/read.cgi/<?=$bbs?>/<?=$key?>/<?=$END?>-n">新着レスの表示</a></div></div><hr><? } ?><div class="bottommenu"><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/">全部</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/<?=$u?>-<?=$f?>">前100</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/<?=$e?>-<?=$t?>">次100</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/l50">最新50</a></div><? if (!$stop and !$maxover) { ?><form method="POST" accept-charset="Shift_JIS" action="//<?=$_SERVER['HTTP_HOST']?>/test/bbs.cgi"><p><input type="submit" value="書き込む" name="submit">名前:<input name="FROM" size="19">E-mail:<input name="mail" size="19" value="<?=$_COOKIE["MAIL"]?>"><span class="backmsg"><input value="on" type="checkbox" id="seticon" name="icon" checked=""><a href="/test/icon.cgi">アイコン</a></span><br><textarea rows="5" cols="70" name="MESSAGE" wrap="off"></textarea><input type="hidden" name="bbs" value="<?=$bbs?>"><input type="hidden" name="key" value="<?=$key?>"><input type="hidden" name="time" value="<?=$NOW?>"><input type="hidden" name="cert" value="<?=$cert?>"></p></form><div style="min-height:50px">■ 告知欄<br><?=$kokuti?><br><br></div><? } ?><div class="footer push">read.cgi ver 06.0.0 2015/11 </div></body></html><? exit;
function nodat() {
	global $bbs;
	?><!DOCTYPE HTML>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><script type="text/javascript" src="https://dream.kakiko.org/js/jquery-1.11.3.min.js"></script><script type="text/javascript" src="https://dream.kakiko.org/js/ad.js"></script><title>datが存在しません。削除されたかURL間違ってますよ。</title><link href="https://dream.kakiko.org/css/ad.css" rel="stylesheet" type="text/css"><link href="https://dream.kakiko.org/css/style.css" rel="stylesheet" type="text/css"></head><body><div class="return"><a href="//<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a></div><div class="errorCode">datが存在しません。削除されたかURL間違ってますよ。</div><div class="footer push">read.cgi ver 06.0.0 2015/11 </div></body></html><? exit;
}
function push() {
	exit('<div class="footer push">read.cgi ver 06.0.0 2015/11 </div>');
}
?>