<?php
header("Content-type: text/html; charset=Shift_JIS");
$st = $to = 0;
$nofirst = false;
if (!$SETTING['BBS_CONTENTS_NUMBER']) $SETTING['BBS_CONTENTS_NUMBER'] = 10;
$ls = $SETTING['BBS_CONTENTS_NUMBER'];
#==================================================
#　時刻を設定
#==================================================
$NOW = time();
$today = getdate(); 
$JIKAN = $today['hours']; 
#==================================================
#　リクエスト解析
#==================================================
if ($_SERVER['REQUEST_METHOD'] != 'GET') nodat();
if (!$bbs) nodat();
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
$BBSSERV = "/virtual/banana356s/public_html/".$_SERVER['HTTP_HOST']."/";	#格納鯖のパス
$BASEURL = "$URL/$bbs/";
if(!file_exists($BBSSERV.$bbs."/")) nodat();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/")) nodat();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/")) nodat();
#スレッドの場所
$thread_file = $BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi";
if (!is_file($thread_file)) nodat();
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
		$subject='削除';
	}
#==================================================
#　出力
#==================================================
$i = 0;
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
		$message = " [ここ壊れてます] ";
	}
	if ($num == "del" || strpos($num, "del") !== false) {
		#レスが削除済みの場合
		$name='';
		$mail='';
		$DATE = '';
		$id = '';
		$message=' '.$SETTING[DELETED_TEXT].' ';
	}
	$message = str_replace('<img src="https://', '<img src="//', $message);
	$message = str_replace('<img src="http://', '<img src="//', $message);
	$message = str_replace('<a href="https://', '<a href="//', $message);
	$message = str_replace('<a href="http://', '<a href="//', $message);
	$message = str_replace('align="left"', '', $message);
	$message = str_replace("<br>", " <br> ", $message);
	$message = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $message);
	$message = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $s;
  	  $url = $m[0];
	$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
	if(preg_match('/https?/', $url) and preg_match('/rentalbbs\.net/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"noopener noreferrer\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $message);
	$message = preg_replace("/sssp:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<img class=\"image img-1\" src=\"https://$1\">", $message);
#レスアンカーをリンクに変換
$message = preg_replace_callback('/&gt;&gt;([0-9]+),?([0-9]+)?,?([0-9]+)?,?([0-9]+)?,?([0-9]+)?(?![-\d])/', function ($m) {
	global $bbs, $key ,$s, $LINENUM, $st ,$to;
	$anka = "<a href=\"/test/read.html/$bbs/$key/$m[1]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[1]</a>";
	if ($m[2]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[2]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[2]</a>";
	if ($m[3]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[3]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[3]</a>";
	if ($m[4]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[4]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[4]</a>";
	if ($m[5]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[5]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[5]</a>";
	return $anka;
	}, $message);
$message = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	return "<a href=\"/test/read.html/$bbs/$key/$m[1]-$m[2]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $message);
	# 名前の色
	$ncolor = '';
	if (strpos($DATE, "02/14") !== false) $ncolor = "#785f01";	#バレンタインデー
	if ($ncolor) $name = "<span style=\"color:$ncolor\">".$name."</span>";
	if (!$SETTING['BBS_NAME_COLOR']) $SETTING['BBS_NAME_COLOR'] = "green";
	$mailto = $mail ? "<a href=\"mailto:$mail\"><b>$name</b></a>" : "<font color=\"$SETTING[BBS_NAME_COLOR]\"><b>$name</b></font>";
	if ($name) $mailto = " 名前：".$mailto;
	# レス出力
	echo "<dt>1".$mailto." ".$DATE." ".$id."</dt><dd>".$message."<br><br></dd>\n";
}
while ($s <= $END) {
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
		$message = " [ここ壊れてます] ";
	}
	if ($num == "del" || strpos($num, "del") !== false) {
		#レスが削除済みの場合
		$name='';
		$mail='';
		$DATE = '';
		$id = '';
		$message=' '.$SETTING[DELETED_TEXT].' ';
	}
	$message = str_replace('<img src="https://', '<img src="//', $message);
	$message = str_replace('<img src="http://', '<img src="//', $message);
	$message = str_replace('<a href="https://', '<a href="//', $message);
	$message = str_replace('<a href="http://', '<a href="//', $message);
	$message = str_replace('align="left"', '', $message);
	$message = str_replace("<br>", " <br> ", $message);
	$message = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $message);
	$message = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $s;
  	  $url = $m[0];
	$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
	if(preg_match('/https?/', $url) and preg_match('/rentalbbs\.net/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"noopener noreferrer\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $message);
	$message = preg_replace("/sssp:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<img class=\"image img-1\" src=\"https://$1\">", $message);
#レスアンカーをリンクに変換
$message = preg_replace_callback('/&gt;&gt;([0-9]+),?([0-9]+)?,?([0-9]+)?,?([0-9]+)?,?([0-9]+)?(?![-\d])/', function ($m) {
	global $bbs, $key ,$s, $LINENUM, $st ,$to;
	$anka = "<a href=\"/test/read.html/$bbs/$key/$m[1]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[1]</a>";
	if ($m[2]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[2]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[2]</a>";
	if ($m[3]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[3]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[3]</a>";
	if ($m[4]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[4]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[4]</a>";
	if ($m[5]) $anka .= ",<a href=\"/test/read.html/$bbs/$key/$m[5]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[5]</a>";
	return $anka;
	}, $message);
$message = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	return "<a href=\"/test/read.html/$bbs/$key/$m[1]-$m[2]\" rel=\"noopener noreferrer\" target=\"_blank\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $message);
	# 名前の色
	$ncolor = '';
	if (strpos($DATE, "02/14") !== false) $ncolor = "#785f01";	#バレンタインデー
	if ($ncolor) $name = "<span style=\"color:$ncolor\">".$name."</span>";	if (!$SETTING['BBS_NAME_COLOR']) $SETTING['BBS_NAME_COLOR'] = "green";
	$mailto = $mail ? "<a href=\"mailto:$mail\"><b>$name</b></a>" : "<font color=\"$SETTING[BBS_NAME_COLOR]\"><b>$name</b></font>";
	if ($name) $mailto = " 名前：".$mailto;
	# レス出力
	echo "<dt>".$s.$mailto." ：".$DATE." ".$id."</dt><dd>".$message."<br><br></dd>\n";
	$s++;
}
$cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$bbs.$key.$NOW.$subject.$_SERVER['REMOTE_ADDR'].$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
?><hr><a href="/test/read.html/<?=$bbs?>/<?=$key?>/">全部読む</a> <a href="/test/read.html/<?=$bbs?>/<?=$key?>/l50/?ls=50">最新50</a> <a href="/test/read.html/<?=$bbs?>/<?=$key?>/-100/?to=100">1-100</a> <a href="#menu">板のトップ</a> <a href="./index.html">リロード</a><hr><h3 style="color: #06F;">書き込み欄</h3><form method="POST" action="/test/bbs.cgi?guid=ON" style="margin: 0 0 0 2em;"><input type="hidden" name="bbs" value="<?=$bbs?>"><input type="hidden" name="key" value="<?=$key?>"><input type="hidden" name="time" value="<?=$NOW?>"><input type="hidden" name="cert" value="<?=$cert?>"><input type="submit" value="書き込む" name="submit">
 名前：	
<input type="text" name="FROM" size="24">
 E-mail：
<input type="text" name="mail" size="24" value="<?=$_COOKIE["MAIL"]?>"><div class="backmsg" style="display: inline-block;"><input value="on" type="checkbox" id="seticon" name="icon" checked=""><a href="/test/icon.cgi">アイコン</a></div>
<br>
<textarea rows="8" cols="80" name="MESSAGE" wrap="off"></textarea><br></form><? exit;
function nodat() {
	exit('<div class="errorCode">datが存在しません。削除されたかURL間違ってますよ。</div>');
}
?>