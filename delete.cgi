<?php
#############################################################################
# 削除＆ログ閲覧
#############################################################################
header("Content-type: text/html; charset=Shift_JIS");
if (!$_POST[bbs]) exit("板が指定されていません");
$PATH = $BBSSERV.$_POST[bbs]."/";
if (!$_POST[key]) {
?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>ログ閲覧・削除・ロールバック</title><link href="https://rentalbbs.net/css/a.css" rel="stylesheet" type="text/css"></head><body><div id="container"><section><h1 class="section-title">ログ閲覧・削除・ロールバック</h1><form class="form-basic" method="POST" accept-charset="Shift_JIS" action=""><input type="hidden" name="bbs" value="<?=$_POST[bbs]?>"><input type="hidden" name="mode" value="view"><div class="contents"><input type="text" class="form-control" name="key" value="" placeholder="スレッドkey"><p class="notice mt5">スレッドkeyを入力してください。</p></div><div class="contents"><input type="password" class="form-control" name="pass" value="" placeholder="パスワード"><p class="notice mt5">パスワードを入力してください。</p></div><div class="contents"><button type="submit" class="btn btn-primary btn-lg btn-block">ログ閲覧・削除画面へ</button></div><div class="contents"><button type="submit" class="btn btn-primary btn-lg btn-block" name="back">ロールバック確認画面へ</button></div></form></section></div></body></html><?
exit;
}
if (!$_POST[pass]) exit("パスワードがありません");
$password = file_get_contents($PATH."pass.cgi");
if ($_POST[pass] != $password) {
	if (is_file($PATH."cap.cgi")) {
		$cap_str = file($PATH."cap.cgi");
		foreach ($cap_str as $tmp){
		$tmp = trim($tmp);
		if (!$tmp or strpos($tmp, '#') !== false or strpos($tmp, '<>') === false) continue;
		list($name1,$pass1,$a1) = explode("<>", $tmp);
			if ($_POST[pass] == $pass1 and ($a1 == "saku" or $a1 == "sakud")) {
				$cap = 1;
				if ($a1 == "sakud") $sakud = 1;
				break;
			}
		}
	}
if (!$cap) exit("パスワードが無効です");
}
#==================================================
#　時刻を設定
#==================================================
$NOW = time();
$today = getdate();
$JIKAN = $today['hours'];
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
$BBSSERV = "/virtual/oyster356s/public_html/".$_SERVER['HTTP_HOST']."/";	#格納鯖のパス
if(!file_exists($BBSSERV.$_POST[bbs]."/")) nodat();
if(!file_exists($BBSSERV.$_POST[bbs]."/".substr($_POST[key], 0, 4)."/")) nodat();
if(!file_exists($BBSSERV.$_POST[bbs]."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/")) nodat();
#スレッドの場所
$thread_file = $BBSSERV.$_POST[bbs]."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/".$_POST[key].".cgi";
if (!is_file($thread_file)) nodat();
$LOG = file($thread_file);
$backup_file = $BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/back_".$_POST['key'].".cgi";
#==================================================
#　ロールバック確認画面
#==================================================
if (isset($_POST['back'])) {
 if ($sakud) exit('このキャップではロールバックを行う権限がありません。<hr><a href="/'.$_POST[bbs].'/index.html">板TOPへ戻る</a>');
 if (!is_file($backup_file)) exit('このスレッドはロールバックできません。<hr><a href="/'.$_POST[bbs].'/index.html">板TOPへ戻る</a>');
 ?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>ロールバック確認</title><link href="https://rentalbbs.net/css/a.css" rel="stylesheet" type="text/css"></head><body><div id="container"><section><h1 class="section-title">ロールバック確認</h1><div>スレッドを下記の復元日時時点の状態へロールバックしますか？<font color="red"><br>※一度ロールバックすると元に戻すことはできません<br>※ロールバックを行うと復元日時以降の書き込みはあらゆるログを含め消失します。書き込みログが必要な場合は必ずお控えの上ロールバックを行ってください<br>※ロールバック時、スレッド一覧でのレス数は変更されません。正しい数値にするにはロールバック後に書き込みが必要です</font></div><div>復元(このスレッドがバックアップされた)日時：<b><? echo date ("Y-m-d H:i:s", filemtime($backup_file)); ?></b></div><div><small>スレッド最終更新日時：<b><? echo date ("Y-m-d H:i:s", filemtime($thread_file)); ?></b></small></div><form class="form-basic" method="POST" accept-charset="Shift_JIS" action=""><input type="hidden" name="bbs" value="<?=$_POST[bbs]?>"><input type="hidden" name="pass" value="<?=$_POST[pass]?>"><input type="hidden" name="key" value="<?=$_POST[key]?>"><input type="hidden" name="mode" value="rollback"><div class="contents"><button type="submit" class="btn btn-primary btn-lg btn-block">ロールバックを行う</button></div></form></section></div></body></html>
 <?
 exit;
}
#==================================================
#　ロールバックを行う
#==================================================
if ($_POST[mode] == "rollback") {
 file_put_contents($thread_file, file_get_contents($backup_file));
 exit('完了<hr><a href="/test/read.cgi/'.$_POST[bbs].'/'.$_POST[key].'/">スレッドへ戻る</a><br><a href="/'.$_POST[bbs].'/index.html">板TOPへ戻る</a>');
}
#==================================================
#　ログ閲覧
#==================================================
if ($_POST[mode] == "view") {
?><!DOCTYPE HTML>
<html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>ログ閲覧＆削除</title>
<link href="https://kakiko.org/a.css" rel="stylesheet" type="text/css"><style>
dd {
	color: black;
	margin-left: 40px;
	clear: both;
	font-size: 16px;
}
</style></head><body>
<form class="form-basic" method="POST" accept-charset="Shift_JIS" action=""><input type="hidden" name="bbs" value="<?=$_POST[bbs]?>"><input type="hidden" name="key" value="<?=$_POST[key]?>"><input type="hidden" name="pass" value="<?=$_POST[pass]?>"><input type="hidden" name="mode" value="del"><div class="contents"><button type="submit" class="btn btn-primary btn-lg btn-block">削除を実行</button></div>
<?php
list($num,) = explode("<>",$LOG[0]);
if ($num == "saku") echo '<font color="red">スレ削除済</font>';
echo "スレッド削除/復帰<input type=\"checkbox\" name=\"thread\" value=\"checked\">";
echo '<div>一括削除(範囲指定)：<input type="text" name="from">-<input type="text" name="to"></div><div>一括削除(条件一致)：<input type="text" name="itti"></div>';
$i = 0;
if (!$st) $st = $s;
if (!$to) $to = $LINENUM;
foreach($LOG as $tmp) {
	$n++;
	list($num,$name,$mail,$time,$id,$msg,$inf,$subject,,$ua,$ua1,$phone,$SID,$REMOTE_HOST,$REMOTE_ADDR,,,$PHOEBELV,) = explode("<>",$LOG[$i]);
	list(,$REMOTE_PORT,$COUNTRY,,,$slip,) = explode("|",$inf);
	if ($time) {
	$time = substr($time, 0, 10);	#unixtime
	$wday = array('日','月','火','水','木','金','土');
	$today = getdate($time);
	$JIKAN = $today['hours'];
	$DATE = date("Y/m/d(", $time).$wday[$today['wday']].date(") H:i:s", $time);
	}else $DATE = '';
	if ($num == "del") $d = '<font color="red">削除済</font>';
	else $d = '';
	$name = str_replace("<b>", "", $name);
	$name = str_replace("</b>", "", $name);
	echo "<dt>削/復<input type=\"checkbox\" name=\"".$i."\" value=\"checked\"> ".$n."[$d] ：".$name."[".$mail."]：".$DATE." ".$id." [ ".$REMOTE_HOST." ] ".$slip."<dd>".$msg."<hr>IP:".$REMOTE_ADDR." Key:".$SID."<br>UA:".$ua."<br>UA2:".$ua1."<br>PHONE:".$phone." Elapsed Time:".$PHOEBELV."<br>REMOTE_PORT:".$REMOTE_PORT." COUNTRY:".$COUNTRY."</dd>";
	$i++;
}
exit('<div class="contents"><button type="submit" class="btn btn-primary btn-lg btn-block">削除を実行</button></div></body></html>');
}
if ($_POST[mode] == "del") {
	$i = 0;
	foreach($LOG as $tmp) {
	list($num,$name,$mail,$time,$id,$msg,$inf,$subject,$ti,$ua,$ua1,$phone,$SID,$REMOTE_HOST,$REMOTE_ADDR,$sr,$wr,$PHOEBELV,) = explode("<>",$LOG[$i]);
	if ($_POST[thread] == "checked" and $i == 0) {
		if ($num == "saku") $num = '';
		else $num = 'saku';
	}
	if ($_POST[$i] == "checked") {
		if ($num == "del") $num = '';
		else $num = 'del';
	}
	if ($i + 1 >= $_POST[from] and $i + 1 <= $_POST[to]) {
		if ($num == "del") $num = '';
		else $num = 'del';
	}
	if (strpos($LOG[$i],$_POST[itti]) !== false) {
		if ($num == "del") $num = '';
		else $num = 'del';
	}
	$fp .= "$num<>$name<>$mail<>$time<>$id<>$msg<>$inf<>$subject<>$ti<>$ua<>$ua1<>$phone<>$SID<>$REMOTE_HOST<>$REMOTE_ADDR<>$sr<>$wr<>$PHOEBELV<>\n";
	$i++;
	}
	file_put_contents($thread_file, $fp, LOCK_EX);
exit('完了<hr><a href="/test/read.cgi/'.$_POST[bbs].'/'.$_POST[key].'/">スレッドへ戻る</a><br><a href="/'.$_POST[bbs].'/index.html">板TOPへ戻る</a>');
}
function nodat() {
exit('スレッドが見つかりません。<hr><a href="/'.$_POST[bbs].'/index.html">板TOPへ戻る</a>');
}
?>