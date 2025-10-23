<?php
header("Content-Type: text/html; charset=Shift_JIS");
$NOWTIME = time();
$BBQSERV = "/virtual/banana356s/public_html/rentalbbs/";	#格納鯖のパス
$PATH = $BBSSERV.$_POST['bbs']."/";

# ホスト名を取得
$HOST = gethostbyaddr($_SERVER['REMOTE_ADDR']);
$SID = $_SESSION['REMOTE_ADDR'] = $_SERVER['REMOTE_ADDR'];
$REMOTE_HOST = $HOST;
$DUA = $_SERVER[HTTP_USER_AGENT];
#######################################################################
# IPv6接続かどうかをチェックする
# IPアドレスの先端を取り出す
#######################################################################
$REMOTEADDR = $_SERVER['REMOTE_ADDR'];	#IPアドレスを入れる(IPv6用)
# IPv6とIPv4を判別
$count_semi = substr_count($_SERVER['REMOTE_ADDR'], ':');
$count_dot = substr_count($_SERVER['REMOTE_ADDR'], '.');
if ($count_semi > 0 and $count_dot == 0) $ipv6 = $_SERVER['REMOTE_ADDR'];
# IPアドレス範囲
if ($ipv6) {
$d = explode(":", $_SERVER['REMOTE_ADDR']);
$HOST = $_SERVER['REMOTE_ADDR'];
$_SERVER['REMOTE_ADDR'] = $d[0].":".$d[1].":".$d[2].":".$d[3];	#後半は端末ごとに変わるので切り捨て
if (isset($d)) {
$c = count($d);
$iprange = $d[0].":".$d[1].":".substr($d[2], 0, 1);
}
}else {
#IPv4でリモートホストがおかしいときは修正
if ($HOST != gethostbyaddr($_SERVER['REMOTE_ADDR'])) $HOST = gethostbyaddr($_SERVER['REMOTE_ADDR']);
$d = explode(".", $_SERVER['REMOTE_ADDR']);
if (isset($d)) {
$c = count($d);
$range = $d[0];
$iprange = $d[0].".".$d[1];
}
}
$file_ipaddr = str_replace(".", "", $_SERVER['REMOTE_ADDR']);
$file_ipaddr = str_replace(":", "", $file_ipaddr);
#######################################################################
# 文字コード変換（UTF-8 -> Shift_JIS）
#######################################################################
$default_substitute_char = mb_substitute_character();	#デフォルトの設定を取っておく
mb_substitute_character('entity');	#絵文字・特殊文字対策
# UTF-8を検出し文字コード変換
if (is_utf8($_POST['submit'].$_POST['MESSAGE'].$_POST['subject'].$_POST['FROM'].$_POST['mail']) === true) mb_convert_variables('SJIS-win','UTF-8',$_POST);
mb_substitute_character($default_substitute_char);	#設定を戻す
#######################################################################
# 
#######################################################################
# Ruthless Angel
if (is_file($BBSSERV."/".date('z')."/403_".$file_ipaddr.".cgi")) DispError2("ＥＲＲＯＲ！","<h1>You just summoned a Ruthless Angel. あなたは残酷な天使を召喚しました。</h1><h2>Your IP address is ".$REMOTEADDR."</h2><div>I am a Ruthless Angel.<br>私は、残酷な天使。<br>ERROR! Your post is too excessive.<br>ｴﾗｰ! あなたの投稿は過剰すぎます。<br>I am regulated you.<br>私はあなたを規制しました。<br>So you will not be able to write for a while.<br>なので(従って)、あなたはしばらく書き込めません。</div>","9998 Banned;");
# おかしなアクセス
if ($_SERVER["REQUEST_METHOD"] != "POST") DispError("ＥＲＲＯＲ！","ERROR: Recieve GET METHOD: POST メソッドを使ってください。","2400 Invalid GET METHOD.;");
#-------------------------------特定条件のUAを変換
# あり得ないUA
if (strpos($_SERVER['HTTP_USER_AGENT'], 'JaneStyle/') !== false or strpos($_SERVER['HTTP_USER_AGENT'], 'BB2C') !== false or strpos($_SERVER['HTTP_USER_AGENT'], 'mae2c/6.0.0') !== false) DispError("ＥＲＲＯＲ！","ERROR: しばらくお断りしております。[".$_POST['bbs']."]","9990 Banned;");
##########################################################
# JaneStyle_mobile対応までの暫定
if (strpos($_SERVER['HTTP_USER_AGENT'], 'JaneStyle') !== false) DispError("ＥＲＲＯＲ！","ERROR: しばらくお断りしております。[".$_POST['bbs']."]","9990 Banned;");
##########################################################
# BB2C
$_SERVER['HTTP_USER_AGENT'] = str_replace('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36', "Monazilla/1.00 (BB2C 1.3.95; iOS 16.0.0 iPhone)", $_SERVER['HTTP_USER_AGENT']);
# mae2c
$_SERVER['HTTP_USER_AGENT'] = str_replace('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393', "Monazilla/1.00 mae2c/6.0.0 iOS16.0.0 iPhone", $_SERVER['HTTP_USER_AGENT']);
# JaneStyle
$_SERVER['HTTP_USER_AGENT'] = str_replace('Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko', "Monazilla/1.00 JaneStyle/4.23 Windows/10.0 Trident/7.0; rv:11.0", $_SERVER['HTTP_USER_AGENT']);
if ($_SERVER['HTTP_ACCEPT'] == "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" and strpos($_SERVER['HTTP_USER_AGENT'], 'Windows') !== false) $_SERVER['HTTP_USER_AGENT'] = str_replace('Mozilla/', "Monazilla/1.00 Jane/", $_SERVER['HTTP_USER_AGENT']);
# Mozilla -> Monazilla
if ($_SERVER['HTTP_ACCEPT'] == "*/*") $_SERVER['HTTP_USER_AGENT'] = str_replace('Mozilla/5.0', "Monazilla/1.00", $_SERVER['HTTP_USER_AGENT']);
#====================================================
#　入力情報を取得（ＰＯＳＴ）
#====================================================
#数値実体参照を数える
$emojix = preg_match_all("/&#x[A-za-z0-9]{1,};/", $_POST['MESSAGE'], $matches);
$emojia = preg_match_all("/&#[0-9]{1,6};/", $_POST['MESSAGE'], $matches);
$semojix = preg_match_all("/&#x[A-za-z0-9]{1,};/", $_POST['subject'], $matches);
$semojia = preg_match_all("/&#[0-9]{1,6};/", $_POST['subject'], $matches);
$emoji = $emojix + $emojia + $semojix + $semojia;
if (preg_match('/&#0?10[^0-9]/', $_POST['MESSAGE']) or preg_match('/&#[xX]0?a[^a-zA-Z0-9]/', $_POST['MESSAGE']) or preg_match('/&#0?10[^0-9]/', $_POST['subject']) or preg_match('/&#[xX]0?a[^a-zA-Z0-9]/', $_POST['subject'])) DispError("ＥＲＲＯＲ！","ERROR: 使用できない文字が含まれています。","9990 Banned;");	#不正文字を検出
if (!$emoji) {
 if (strpos($_POST['subject'], '&#') !== false or strpos($_POST['MESSAGE'], '&#') !== false or strpos($_POST['FROM'], '&#') !== false) $emoji = true;
}
#====================================================
#　板・スレ情報の取得（設定ファイル）
#====================================================
#設定ファイルを読む
$set_file = $PATH . "SETTING.TXT";
if (is_file($set_file)) {
	$set_str = file($set_file);
	foreach ($set_str as $tmp){
		$tmp = trim($tmp);
		list ($name, $value) = explode("=", $tmp);
		$SETTING[$name] = $value;
		$BSETTING[$name] = $value;
	}
}
#設定ファイルがない
else DispError2("ＥＲＲＯＲ！","ERROR: 存在しない板に投稿しようとしています。");
#######################################################################
# Googleログイン関連
#######################################################################
if ($BSETTING['Use_Account']) {
 # ログイン用に取り出しておく
 $gid = str_replace("#", "", $_POST['mail']);
 if (is_file("/virtual/banana356s/public_html/rentalbbs/gid/".$gid.".cgi")) {
	$_COOKIE[secretkey] = $gid;
 }else {
	if (!is_file("/virtual/banana356s/public_html/rentalbbs/gid/".$_COOKIE[secretkey].".cgi")) $_COOKIE[secretkey] = '';
 }
 if ($_COOKIE[secretkey]) {
	$gpath = "/virtual/bbs3ch/public_html/rentalbbs/gid/".$_COOKIE[secretkey].".cgi";
	#if (filemtime($gpath) < $NOWTIME - 2592000) DispError("ＥＲＲＯＲ！","ERROR: ログイン後31日が経過しました。再度ログインしてください。","G7000 Please login;");
	$BANF = $BBSSERV."/".date('z')."/BAN_".$_COOKIE[secretkey].".cgi";
	if ($BSETTING['Use_Banned'] == "checked" and is_file($BANF)) DispError("ＥＲＲＯＲ！","ERROR: このアカウントはスパムであると判定されたため日付が変わるまで投稿できません。","G7900 Banned;");
	$login = true;
	$SID = $_COOKIE[secretkey];
	$_SESSION['REMOTE_ADDR'] = $_COOKIE[secretkey];
	setcookie("secretkey", $_COOKIE[secretkey], $NOWTIME+2592000, "/", "rentalbbs.net");
 }
}
#-------------------------------read.cgi以外からの投稿でCAPTCHAを通してない場合は認証画面を出す
if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) {
	if (!$_POST['cert'] and $_POST['key']) DispError("ＥＲＲＯＲ！","ERROR: 新仕様に対応した専用ブラウザをご利用ください。","E3001 Unavailable an old dedicated browser.;");
 if (!$login) {
 #--------------未ログイン時の処理 ここから-------
	if (!isset($_POST['g-recaptcha-response']) and !$_GET['manment']) {
	# if (!isset($_SERVER['HTTP_X_REQUESTED_WITH']) or strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) != 'xmlhttprequest') Kakunin();
	}
 #--------------未ログイン時の処理 ここまで-------
 }
}else {
	#-------------------------------サードパーティー製アプリからの投稿を禁止する
	if ($BSETTING['third_party_apps_post'] != "enable") {
	Header("HTTP/1.0 401 Unauthorized");
	exit("Error Code: Could not authenticate you.;");
	}
}
#############################################################################
# 「いきなり」チェックするルーチン
# 歴史的事情がたくさんあるようなので、更新時には注意すること
#############################################################################
if (get_magic_quotes_gpc()) $_POST = array_map("stripslashes", $_POST);
$_POST['subject'] = str_replace(array("\r\n","\r","\n"), " ", $_POST['subject']);
$_POST['FROM'] = str_replace('"', "&quot;", $_POST['FROM']);
$_POST['FROM'] = str_replace("<", "&lt;", $_POST['FROM']);
$_POST['FROM'] = str_replace(">", "&gt;", $_POST['FROM']);
$_POST['FROM'] = str_replace("'", "&#039;", $_POST['FROM']);
$_POST['FROM'] = str_replace("&amp", "", $_POST['FROM']);
$_POST['FROM'] = str_replace(array("\r\n","\r","\n"), " ", $_POST['FROM']);
$_POST['FROM'] = trim($_POST['FROM']);
$_POST['mail'] = htmlspecialchars($_POST['mail'], ENT_QUOTES, 'SJIS');
$_POST['mail'] = str_replace(array("\r\n","\r","\n"), " ", $_POST['mail']);
$_POST['mail'] = trim($_POST['mail']);
$_POST['bbs'] = str_replace(array(".","/","|"), "", $_POST['bbs']);
$_POST['key'] = str_replace(array(".","/","|"), "", $_POST['key']);
$_POST['MESSAGE'] = str_replace('"', "&quot;", $_POST['MESSAGE']);
$_POST['MESSAGE'] = str_replace("<", "&lt;", $_POST['MESSAGE']);
$_POST['MESSAGE'] = str_replace(">", "&gt;", $_POST['MESSAGE']);
$_POST['MESSAGE'] = str_replace("'", "&#039;", $_POST['MESSAGE']);
$_POST['MESSAGE'] = str_replace("&amp", "", $_POST['MESSAGE']);
$_POST['MESSAGE'] .= " ";
$_POST['MESSAGE'] = rtrim($_POST['MESSAGE']);
$_POST['MESSAGE'] = str_replace(array("\r\n","\r","\n"), "<br>", $_POST['MESSAGE']);
# ＮＧワード
if ($BSETTING['change_sakujyo'] == "checked" and !$admin) {
$_POST['FROM'] = str_replace("管理", '"管理"', $_POST['FROM']);
$_POST['FROM'] = str_replace("削除", '"削除"', $_POST['FROM']);
$_POST['FROM'] = str_replace("sakujyo", '"sakujyo"', $_POST['FROM']);
}
# 全角＃のパス漏れ防止
#香美バグのためmb_ereg_replaceにしようかとも考えたが中止
$_POST['FROM'] = str_replace("＃", "#", $_POST['FROM']);
$_POST['mail'] = str_replace("＃", "#", $_POST['mail']);
# read.html対応用
# AAを検出
if ($BSETTING['aa_check'] == "checked") {
if (strpos($_POST['MESSAGE'], '∧') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '＿') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '￣') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '彡') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], 'Ｕ') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '＜') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '／') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '＼') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '&lt;') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '┼') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '┬') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '::') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], '≡') !== false) $aa = 1;
if (strpos($_POST['MESSAGE'], ':.') !== false) $aa = 1;
}
# 偽キャップ、偽トリップ変換
$_POST['FROM'] = str_replace("★", "☆", $_POST['FROM']);
$_POST['FROM'] = str_replace("◆", "◇", $_POST['FROM']);
# 本文を行ごとに分割
$msgbr = explode("<br>", $_POST['MESSAGE']);
if (!$_POST['bbs']) endhtml("2600 Invalid Post.;");
# subjectもkeyも両方ある/両方ない
if (($_POST['subject'] and $_POST['key']) or (!$_POST['subject'] and !$_POST['key'])) endhtml("2600 Invalid Post.;");
# キーが数字じゃない場合ばいばい！
if (preg_match("/\D/", $_POST['key'])) endhtml("2600 Invalid Post.;");
# ありえないホスト
if (stristr($HOST, "proxy") or stristr($HOST, "cache") or stristr($HOST, "mail") or stristr($HOST, "www") or stristr($HOST, "mail") or stristr($HOST, "googleusercontent.com") or stristr($HOST, "vpn") or stristr($HOST, "tor")) DispError("ＥＲＲＯＲ！","ERROR: このホストからはdelightに投稿できません。","9990 Banned;");
# 最近の素のIE8はUAがとても長いので、256ではきつすぎ
if (strlen($_SERVER['HTTP_USER_AGENT']) > 384 or strlen($_SERVER['HTTP_USER_AGENT']) != mb_strlen($_SERVER['HTTP_USER_AGENT'],"SJIS") or strlen($_SERVER['HTTP_USER_AGENT']) < 7 or strpos($_SERVER['HTTP_USER_AGENT'], '<') !== false or strpos($_SERVER['HTTP_USER_AGENT'], '>') !== false) endhtml("2600 Invalid Post.;");
# Mozilla/Monazilla どちらも含まれていない
if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') === false and strpos($_SERVER['HTTP_USER_AGENT'], 'Monazilla') === false) endhtml("2600 Invalid Post.;");
# 変な文字
if (strpos($_POST[MESSAGE], '&ZeroWidthSpace;') !== false) DispError("ＥＲＲＯＲ！","ERROR: 使用できない文字が含まれています。","9990 Banned;");
# 本文なし
if (strlen($_POST['MESSAGE']) == 0) DispError("ＥＲＲＯＲ！","ERROR: 本文がありません。","2031 Message is empty;");
#==================================================
#　トリップ
#==================================================
#名前欄は先に取っておく
$Cookname = $_POST[FROM];
# トリップ
$_POST['FROM'] = str_replace("&#", '&!E', $_POST['FROM']);
if (preg_match("/([^\#]*)\#(.+)/", $_POST['FROM'], $tr)) {
 $_POST['FROM'] = $tr[1].nametrip("#".$tr[2]);
}
$_POST['FROM'] = str_replace("&!E", '&#', $_POST['FROM']);
#######################################################################
# キャップ
#######################################################################
# 管理
if (preg_match("/([^\#]*)\#(.+)/", $_POST['mail'], $ca)) {
 $pass1 = file_get_contents($PATH."pass.cgi");
  if ($ca[2] == $pass1) {
	if ($_POST['FROM']) $_POST['FROM'] .= "＠管理人 ★";
	else $_POST['FROM'] = "管理人 ★";
	$admin = 1;
	$cap = 1;
	$CAPID = "administrator";
  }
}
# 通常
if (preg_match("/([^\#]*)\#(.+)/", $_POST['mail'], $ca)) {
	if (is_file($PATH."cap.cgi")) {
		$cap_str = file($PATH."cap.cgi");
		foreach ($cap_str as $tmp){
		$tmp = trim($tmp);
		if (!$tmp or strpos($tmp, '#') !== false or strpos($tmp, '<>') === false) continue;
		list($name1,$pass1,$a1,$caid) = explode("<>", $tmp);
			if ($ca[2] == $pass1) {
				if ($_POST['FROM']) $_POST['FROM'] .= "＠$name1 ★";
				else $_POST['FROM'] = "$name1 ★";
				if ($a1 != "plus" and $a1 != "ncmd" and $a1 != "sakud") $admin = 1;
				if ($a1 == "ncmd") $kaihi = 1;
				if ($a1 == "sakud") $sakud = 1;
				$cap = 1;
				if ($caid) $CAPID = $caid;
				else $CAPID = "CAP_USER";
				break;
			}
		}
	}
}
if (preg_match("/([^\#]*)\#(.+)/", $_POST['mail'], $ca)) {
	$Cookmail = $_POST['mail'];
	$_POST['mail'] = $ca[1];
}
#名前とメールを保存
if (!$Cookmail) $Cookmail = $_POST[mail];
$_SESSION["NAME"] = $Cookname;
$_SESSION["MAIL"] = $Cookmail;

if ($admin || $kaihi || strstr($_POST['FROM'], "!ch2kanri3")) $errorskip = 1;
$_POST['FROM'] = str_replace("!ch2kanri3", "", $_POST['FROM']);
#====================================================
#　各種ＰＡＴＨ生成＆日付・時刻を設定
#====================================================
$DATE = date("Y/m/d H:i:s", $NOWTIME);
$SIDPATH	= $BBQSERV."agreement/sess_";
$RESFILE	= $PATH."res.cgi";
$bbx_kiroku	= $BBQSERV."bbx.cgi";
$subjectfile = $BBSSERV.$_POST[bbs]."/subject.txt";
if (!isset($_POST['subject'])) $_POST['subject'] = '';
if (!isset($_POST['FROM'])) $_POST['FROM'] = '';
if (!isset($_POST['mail'])) $_POST['mail'] = '';
if (!isset($_POST['bbs'])) $_POST['bbs'] = '';
if (!isset($_POST['key'])) $_POST['key'] = '';
if (!isset($_POST['MESSAGE'])) $_POST['MESSAGE'] = '';
$zumbatime = 256;
#######################################################################
# 記録用ディレクトリをチェック
#######################################################################
$file_ipaddr1 = str_replace(".", "", $REMOTEADDR);
$file_ipaddr1 = str_replace(":", "", $file_ipaddr1);
	if (!file_exists($BBSSERV."/".date('z'))) {
	#日付が変わった時の処理
    	@mkdir($BBSSERV."/".date('z'), 0777, true);
	}
	#前日分を消去
	$maedz = date('z') - 1;
	if (file_exists($BBSSERV."/".$maedz)) {
	$maedzs = $BBSSERV."/".$maedz."/*.*";
    	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/".$maedz);
	}
	if (date('z') != 364 and file_exists($BBSSERV."/364")) {
	$maedzs = $BBSSERV."/364/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/364");
	}
	if (date('z') != 365 and file_exists($BBSSERV."/365")) {
	$maedzs = $BBSSERV."/366/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/365");
	}
	if (date('z') != 366 and file_exists($BBSSERV."/366")) {
	$maedzs = $BBSSERV."/366/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/366");
	}
#-------------------------------板毎	
	if (!file_exists($BBSSERV."/tmp/".$_POST['bbs'].date('z'))) {
	#日付が変わった時の処理
    	@mkdir($BBSSERV."/tmp/".$_POST['bbs'].date('z'), 0777, true);
	}
	#前日分を消去
	$maedz = date('z') - 1;
	if (file_exists($BBSSERV."/tmp/".$_POST['bbs'].$maedz)) {
	$maedzs = $BBSSERV."/tmp/".$_POST['bbs'].$maedz."/*.*";
    	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$_POST['bbs'].$maedz);
	}
	if (date('z') != 364 and file_exists($BBSSERV."/tmp/".$_POST['bbs']."364")) {
	$maedzs = $BBSSERV."/tmp/".$_POST['bbs']."364/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$_POST['bbs']."364");
	}
	if (date('z') != 365 and file_exists($BBSSERV."/tmp/".$_POST['bbs']."365")) {
	$maedzs = $BBSSERV."/tmp/".$_POST['bbs']."365/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$_POST['bbs']."365");
	}
	if (date('z') != 366 and file_exists($BBSSERV."/tmp/".$_POST['bbs']."366")) {
	$maedzs = $BBSSERV."/tmp/".$_POST['bbs']."366/*.*";
	@array_map('unlink', glob($maedzs));
  	@rmdir($BBSSERV."/tmp/".$_POST['bbs']."_366");
	}
#############################################################################
#	端末判定(USER_AGENT)
#############################################################################
#-------------------------------端末・ブラウザ情報を取得
if ($_SERVER['HTTP_SEC_CH_UA_FULL_VERSION_LIST']) $_SERVER['HTTP_SEC_CH_UA'] = $_SERVER['HTTP_SEC_CH_UA_FULL_VERSION_LIST'];
if ($_SERVER['HTTP_SEC_CH_UA_PLATFORM_VERSION'] or $_SERVER['HTTP_SEC_CH_UA_MODEL']) $terminal = $_SERVER['HTTP_SEC_CH_UA_PLATFORM']." ".$_SERVER['HTTP_SEC_CH_UA_PLATFORM_VERSION']." ".$_SERVER['HTTP_SEC_CH_UA_BITNESS']." ".$_SERVER['HTTP_SEC_CH_UA_ARCH']." ".$_SERVER['HTTP_SEC_CH_UA_MODEL']." ".$_SERVER['HTTP_SEC_CH_UA_MOBILE']." ;";
else {
 preg_match('/ \((.+)\)/', $_SERVER['HTTP_USER_AGENT'], $m);
 $terminal = $m[1]." ;";
 if (!$m[1]) {
  preg_match('/(iOS.+)/', $_SERVER['HTTP_USER_AGENT'], $m); 
  $terminal = $m[1]." ;";
 }
}
$USER_AGENT = $_SERVER['HTTP_SEC_CH_UA']." ".$_SERVER['HTTP_ACCEPT']." ".$_SERVER['HTTP_ACCEPT_LANGUAGE']." ".$_SERVER['HTTP_PRIORITY']." ".$_SERVER['CONTENT_TYPE'];

#######################################################################
# PHOEBE
#######################################################################
if (!$login) {
#--------------未ログイン時の処理 ここから-------
$PHOEBELV = $NOWTIME - $_SESSION['firsttime'];
$LV = floor($PHOEBELV / 82800);
if ($PHOEBELV > 600) ++$LV;
if ($PHOEBELV > 3600) ++$LV;
if ($PHOEBELV > 18000) ++$LV;
if ($LV > 40) $LV = 40;
#--------------未ログイン時のみ発行 ここまで-------
}else $LV = 40;	#ログイン時は40固定
#############################################################################
#	smart phone marks 
#############################################################################
	if (strpos($HOST, 'spmode') !== false) {
		if (strpos($HOST, 'msb') !== false) $SLIP_NAME = "ｽﾌﾟｯｯ";
		elseif (strpos($HOST, 'msc') !== false) $SLIP_NAME = "ｽｯﾌﾟ";
		elseif (strpos($HOST, 'msd') !== false) $SLIP_NAME = "ｽｯｯﾌﾟ";
		elseif (strpos($HOST, 'mse') !== false) $SLIP_NAME = "ｽﾌﾟﾌﾟ";
		elseif (strpos($HOST, 'msf') !== false) $SLIP_NAME = "ｽﾌｯ";
		else $SLIP_NAME = "ｽﾌﾟｰ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'au-net') !== false) {
		if (strpos($HOST, 'KD027') !== false || strpos($HOST, 'kd027') !== false) $SLIP_NAME = "ｱｳｱｳｱｰ";
		elseif (strpos($HOST, 'KD036') !== false || strpos($HOST, 'kd036') !== false) $SLIP_NAME = "ｱｳｱｳｲｰ";
		elseif (strpos($HOST, 'KD106') !== false || strpos($HOST, 'kd106') !== false) $SLIP_NAME = "ｱｳｱｳｳｰ";
		elseif (strpos($HOST, 'KD111') !== false || strpos($HOST, 'kd111') !== false) $SLIP_NAME = "ｱｳｱｳｴｰ";
		elseif (strpos($HOST, 'KD119') !== false || strpos($HOST, 'kd119') !== false) $SLIP_NAME = "ｱｳｱｳｵｰ";
		elseif (strpos($HOST, 'KD182249') !== false || strpos($HOST, 'kd182249') !== false || strpos($HOST, 'KD182250') !== false || strpos($HOST, 'kd182250') !== false || strpos($HOST, 'KD1822512') !== false || strpos($HOST, 'kd1822512') !== false) $SLIP_NAME = "ｱｳｱｳｶｰ";
		elseif (strpos($HOST, 'KD182251') !== false || strpos($HOST, 'kd182251') !== false) $SLIP_NAME = "ｱｳｱｳｷｰ";
		elseif (strpos($HOST, 'UQ') !== false || strpos($HOST, 'uq') !== false) { 
			$SLIP_NAME = "ｱｳｱｳｸｰ";
			$MM = 1;
		}
 		else $SLIP_NAME = "ｱｳｱｳ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'openmobile') !== false) {
		$SLIP_NAME = "ｵｯﾍﾟｹ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'panda-world') !== false) {
		if (strpos($HOST, 'tss') !== false || strpos($HOST, 'pw126152') !== false || strpos($HOST, 'pw126161') !== false || strpos($HOST, 'pw126186') !== false || strpos($HOST, 'pw126199') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾗ";
		elseif (strpos($HOST, 'kyb') !== false || strpos($HOST, 'pw126205') !== false || strpos($HOST, 'pw126214') !== false || strpos($HOST, 'pw126225') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾘ";
		elseif (strpos($HOST, 'pw126236') !== false || strpos($HOST, 'pw126237') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾙ";
		elseif (strpos($HOST, 'pw126245') !== false || strpos($HOST, 'pw126247') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾚ";
		elseif (strpos($HOST, 'pw126253') !== false || strpos($HOST, 'pw126254') !== false || strpos($HOST, 'pw126255') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾛ";
		else $SLIP_NAME = "ｻｻｸｯﾃﾛ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'access-internet') !== false) {
		$SLIP_NAME = "ｱ-ｸｾ-";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'e-mobile') !== false) {
		$SLIP_NAME = "ｴ-ｲﾓ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'emobile') !== false) {
		$SLIP_NAME = "ｲﾓ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'air.mopera.net') !== false) {
		$SLIP_NAME = "ｴｱﾍﾟﾗ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'mopera') !== false) {
		$SLIP_NAME = "ﾍﾟﾗﾍﾟﾗ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'google-proxy') !== false) {
		$SLIP_NAME = "ｸﾞｸﾞﾚｶｽ";
		$SLIP_SP = 1;
	}elseif (strpos($HOST, 'wi-fi.wi2') !== false) {
		$SLIP_NAME = "ﾜｲｰﾜ2";
		$WF = 1;
	}elseif (strpos($HOST, 'wi-fi.kddi') !== false) {
		$SLIP_NAME = "ｱｳｳｨﾌ";
		$WF = 1;
	}elseif (strpos($HOST, 'm-zone') !== false) {
		$SLIP_NAME = "ｴﾑｿﾞﾈ";
		$WF = 1;
	}elseif (strpos($HOST, 'wi-fi.fc2') !== false) {
		$SLIP_NAME = "ｴﾌｼｰﾂｰ";
		$WF = 1;
	}elseif (strpos($HOST, 'wi2.co.jp') !== false || strpos($HOST, 'wi2.ne.jp') !== false) {
		$SLIP_NAME = "ﾜｲﾜｲ";
		$WF = 1;
	}elseif (strpos($HOST, 'freespot.com') !== false) {
		$SLIP_NAME = "ﾌﾘｽﾎﾟ";
		$WF = 1;
	}elseif (strpos($HOST, '7spot') !== false) {
		$SLIP_NAME = "ｾﾌﾞﾝ";
		$WF = 1;
	}elseif (strpos($HOST, 'family-wifi') !== false) {
		$SLIP_NAME = "ﾌｧﾐﾏ";
		$WF = 1;
	}elseif (strpos($HOST, 'freemobile.jp') !== false) {
		$SLIP_NAME = "ﾌﾘﾓﾊﾞ";
		$WF = 1;
	}elseif (strpos($HOST, 'ntt-bp.net') !== false) {
		$SLIP_NAME = "ﾐｶｶｳｨﾌｨ";
		$WF = 1;
	}elseif (strpos($HOST, 'wi-fi') !== false) {
		$SLIP_NAME = "ﾜｲｰﾜ";
		$WF = 1;
	}elseif (strpos($HOST, 'vmobile') !== false) {
		$SLIP_NAME = "ﾌﾞｰｲﾓ";
		$MM = 1;
	}elseif (strpos($HOST, 'mp') !== false and strpos($HOST, 'ap.nuro.jp') !== false) {
		$SLIP_NAME = "ｿﾈｯﾄ";	# So-net モバイル LTE
		$MM = 1;
	}elseif (strpos($HOST, 'wimax') !== false || strpos($HOST, 'wmaxuq') !== false) {
		$SLIP_NAME = "ﾜｲﾓﾏｰ";
		$MM = 1;
	}elseif (strpos($HOST, 'wi-gate.net') !== false) {
		$SLIP_NAME = "ﾜｷｹﾞｰ";
		$MM = 1;
	}elseif (strpos($HOST, 'kualnet.jp') !== false) {
		$SLIP_NAME = "ﾜｲｴﾃﾞｨ";
		$MM = 1;
	}elseif (strpos($HOST, 'omed01.tokyo') !== false) {
		$SLIP_NAME = "ﾜﾝﾄﾝｷﾝ";
		$MM = 1;
	}elseif (strpos($HOST, 'omed01.osaka') !== false) {
		$SLIP_NAME = "ﾊﾞｯﾐﾝｸﾞｸ";
		$MM = 1;
	}elseif (strpos($HOST, 'mineo') !== false) {
		$SLIP_NAME = "ｵｲｺﾗﾐﾈｵ";
		$MM = 1;
	}elseif (strpos($HOST, 'neoau1') !== false) {
		$SLIP_NAME = "ﾄﾞﾅﾄﾞﾅｰ";
		$MM = 1;
	}elseif (strpos($HOST, 'dcm2') !== false) {
		$SLIP_NAME = "ﾄﾞｺｸﾞﾛ";
		$MM = 1;
	}elseif (strpos($HOST, 'libmo') !== false) {
		$SLIP_NAME = "ﾌﾞﾓｰ";
		$MM = 1;
	}elseif (strpos($HOST, 'ap.mvno.net') !== false) {
		$SLIP_NAME = "ｱﾒ";
		$MM = 1;
	}else {
		$SLIP_NAME = "ﾜｯﾁｮｲ";
	}
	if ($HOST == $_SERVER['REMOTE_ADDR']) {
		$SLIP_NAME = "JP";
	}
	if (strpos($_SERVER[REMOTE_ADDR], '133.106') !== false || strpos($_SERVER[REMOTE_ADDR], '193.119') !== false || strpos($_SERVER[REMOTE_ADDR], '133.100') !== false) {
		$SLIP_NAME = "ﾃﾃﾝﾃﾝﾃﾝ";
		$MM = 1;
	}
	if (strpos($HOST, 'rakuten') !== false || strpos($_SERVER[REMOTE_ADDR], '240b:c0') !== false) {
		$SLIP_NAME = "ﾗｸｯﾍﾟﾍﾟ";
		$MM = 1;
	}
	if (strpos($_SERVER[REMOTE_ADDR], '103.5.14') !== false) {
		$SLIP_NAME = "ﾜｲｰﾜ2";
		$WF = 1;
	}
	if (strpos($HOST, '2001:240:24') !== false) {
		$SLIP_NAME = "ﾌﾞｰｲﾓ";
		$MM = 1;
	}
	if (strpos($HOST, '240a:61:') !== false) {
		if (strpos($HOST, '240a:61:a') !== false || strpos($HOST, '240a:61:c') !== false || strpos($HOST, '240a:61:e') !== false || strpos($HOST, '240a:61:1') !== false || strpos($HOST, '240a:61:2') !== false || strpos($HOST, '240a:61:3') !== false || strpos($HOST, '240a:61:4') !== false) $SLIP_NAME = "ｽﾌﾟｯｯ";
		elseif (strpos($HOST, '240a:61:5') !== false || strpos($HOST, '240a:61:6') !== false || strpos($HOST, '240a:61:7') !== false || strpos($HOST, '240a:61:8') !== false || strpos($HOST, '240a:61:b') !== false || strpos($HOST, '240a:61:9') !== false || strpos($HOST, '240a:61:d') !== false || strpos($HOST, '240a:61:f') !== false) $SLIP_NAME = "ｽｯﾌﾟ";
		else $SLIP_NAME = "ｽﾌﾟｰ";
		$SLIP_SP = 1;
	}
	if (strpos($HOST, '240a:6b:') !== false) {
		if (strpos($HOST, '240a:6b:a') !== false || strpos($HOST, '240a:6b:c') !== false || strpos($HOST, '240a:6b:e') !== false || strpos($HOST, '240a:6b:1') !== false || strpos($HOST, '240a:6b:2') !== false || strpos($HOST, '240a:6b:3') !== false || strpos($HOST, '240a:6b:4') !== false) $SLIP_NAME = "ｽｯｯﾌﾟ";
		elseif (strpos($HOST, '240a:6b:5') !== false || strpos($HOST, '240a:6b:6') !== false || strpos($HOST, '240a:6b:7') !== false || strpos($HOST, '240a:6b:8') !== false || strpos($HOST, '240a:6b:b') !== false || strpos($HOST, '240a:6b:9') !== false || strpos($HOST, '240a:6b:d') !== false || strpos($HOST, '240a:6b:f') !== false) $SLIP_NAME = "ｽﾌﾟﾌﾟ";
		else $SLIP_NAME = "ｽﾌﾟｯ";
		$SLIP_SP = 1;
	}
	if (strpos($HOST, '2001:268:9') !== false) {
		if (strpos($HOST, '2001:268:9a') !== false || strpos($HOST, '2001:268:9e') !== false || strpos($HOST, '2001:268:9f') !== false) $SLIP_NAME = "ｱｳｱｳｱｰ";
		elseif (strpos($HOST, '2001:268:9b') !== false || strpos($HOST, '2001:268:9c') !== false || strpos($HOST, '2001:268:9d') !== false) $SLIP_NAME = "ｱｳｱｳｲｰ";
		elseif (strpos($HOST, '2001:268:98') !== false || strpos($HOST, '2001:268:91') !== false) $SLIP_NAME = "ｱｳｱｳｳｰ";
		elseif (strpos($HOST, '2001:268:92') !== false || strpos($HOST, '2001:268:93') !== false) $SLIP_NAME = "ｱｳｱｳｴｰ";
		elseif (strpos($HOST, '2001:268:94') !== false || strpos($HOST, '2001:268:95') !== false) $SLIP_NAME = "ｱｳｱｳｵｰ";
		elseif (strpos($HOST, '2001:268:96') !== false || strpos($HOST, '2001:268:97') !== false) $SLIP_NAME = "ｱｳｱｳｶｰ";
		elseif (strpos($HOST, '2001:268:99') !== false) $SLIP_NAME = "ｱｳｱｳｷｰ";
		else $SLIP_NAME = "ｱｳｱｳ";
		$SLIP_SP = 1;
	}
	if (strpos($HOST, '2400:2200:') !== false) {
		if (strpos($HOST, '2400:2200:a') !== false || strpos($HOST, '2400:2200:c') !== false || strpos($HOST, '2400:2200:e') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾗ";
		elseif (strpos($HOST, '2400:2200:1') !== false || strpos($HOST, '2400:2200:2') !== false || strpos($HOST, '2400:2200:3') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾘ";
		elseif (strpos($HOST, '2400:2200:4') !== false || strpos($HOST, '2400:2200:5') !== false || strpos($HOST, '2400:2200:6') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾙ";
		elseif (strpos($HOST, '2400:2200:7') !== false || strpos($HOST, '2400:2200:8') !== false || strpos($HOST, '2400:2200:b') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾚ";
		elseif (strpos($HOST, '2400:2200:9') !== false || strpos($HOST, '2400:2200:d') !== false || strpos($HOST, '2400:2200:f') !== false) $SLIP_NAME = "ｻｻｸｯﾃﾛﾛ";
		else $SLIP_NAME = "ｻｻｸｯﾃﾛ";
		$SLIP_SP = 1;
	}
	if ($admin) {
		$SLIP_NAME = "★";
	}

	#ID末尾
	$slip = "0";
	if ($HOST == $_SERVER['REMOTE_ADDR']) {
	$slip = "H";
	}
	if ($MM) {
		$slip = "M";
	}elseif ($WF) {
		$slip = "F";
	}elseif (strpos($HOST, 'spmode') !== false || strpos($HOST, '240a:61:') !== false || strpos($HOST, '240a:6b:') !== false) {
		$slip = "d";
	}elseif (strpos($HOST, 'au-net') !== false || strpos($HOST, '2001:268:9') !== false){
 		$slip = "a";
	}elseif (strpos($HOST, 'panda-world') !== false || strpos($HOST, '2400:2200:') !== false) {
		$slip = "p";
	}elseif (strpos($HOST, 'openmobile') !== false) {
		$slip = "r";
	}elseif (strpos($HOST, 'access-internet') !== false) {
		$slip = "x";
	}elseif (strpos($HOST, 'e-mobile') !== false) {
		$slip = "E";
	}elseif (strpos($HOST, 'mopera.net') !== false) {
		$slip = "D";
	}elseif (strpos($HOST, 'google-proxy') !== false) {
		$slip = "X";
	}
#######################################################################
#	IPアドレスを記録
#######################################################################
	$ip_file = $BBSSERV."/".date('z')."/".hash('sha256', $HOST.$_SERVER[HTTP_USER_AGENT]).".cgi";
	#IPが登録されていなければ記録
	if (!is_file($ip_file)) {
		file_put_contents($ip_file, $HOST."<>".$_SERVER[HTTP_USER_AGENT]."<>".$terminal." ".$USER_AGENT);
	}
	#IPが登録(初回記録)された時間を取得
	$firsttime = filemtime($ip_file);

#新規スレッド
if ($_POST['subject']) $_POST[key] = $NOWTIME;

#タイトルの変換形式
if ($SETTING['BBS_UNICODE'] != "checked" and !$login) {
$_POST['subject'] = htmlspecialchars($_POST['subject'], ENT_QUOTES, 'SJIS');
}else {
$_POST['subject'] = str_replace('"', "&quot;", $_POST['subject']);
$_POST['subject'] = str_replace("<", "&lt;", $_POST['subject']);
$_POST['subject'] = str_replace(">", "&gt;", $_POST['subject']);
$_POST['subject'] = str_replace("'", "&#039;", $_POST['subject']);
$_POST['subject'] = str_replace("&amp", "？", $_POST['subject']);
$_POST['subject'] .= " ";
$_POST['subject'] = trim($_POST['subject']);
}
#スレッドの場所
$thread_file = $BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/".$_POST['key'].".cgi";
$backup_file = $BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/back_".$_POST['key'].".cgi";

#timecount/timeclose
if (!$BSETTING['timecount']) $BSETTING['timecount'] = 100;
if (!$BSETTING['timeclose']) $BSETTING['timeclose'] = 25;
if ($BSETTING['timeclose'] > $BSETTING['timecount']){
	$BSETTING['timeclose'] = $BSETTING['timecount'];
} 
#######################################################################
# dat落ちを検出
#######################################################################
$subss = @file($subjectfile);
$tc = 1;
	if ($subss) {
		foreach ($subss as $tmp){
		list($k1,,$r1,) = explode("<>", $tmp);
		if ($k1 == $_POST['key']) $isdat = true;
		if ($k1 == $_POST['key'] + 1) $isdat1 = true;
		++$tc;	
		}
	}
# 924スレは対象外
if (substr($_POST[key], 0, 3) == 900 || substr($_POST[key], 0, 3) == 924) $isdat = true;
#if ($tc > 10 and !$_POST['subject'] and !$isdat and $SETTING['FORCE_SAGE'] != 'on') DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
# 同じファイルが既にあった場合
if ($_POST['subject'] and ($isdat or is_file($thread_file))) {
 # +1してOKならそれを使用
 if (!$isdat1) $_POST['key'] += 1;
 # それもだめだったらごめんなさい
 else DispError2("ＥＲＲＯＲ！","ERROR: 別の人が同時刻にスレッドを立てようとしています。再度お試しください。");
}
#######################################################################
# 新IP初回書込処理＆クッキー食いチェック
#######################################################################
if (!$login) {
#	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') === false and $NOWTIME < $firsttime + 5) HoutekiToukouKakunin();
	#クッキー食いチェック
	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') === false and !$_COOKIE) HoutekiToukouKakunin();
	elseif (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false and !$_COOKIE) Kakunin();
}
#====================================================
#　スレッドデータ取得
#====================================================
#スレ立て★持ち限定板
if ($_POST['subject'] and $SETTING['BBS_PASSWORD_CHECK'] == "checked" and !$admin and (!$cap or $kaihi or $sakud)) DispError2("ＥＲＲＯＲ！","ERROR: この掲示板はキャップでなければスレッドを作成することが出来ません。");
if (is_file($thread_file)) {
#スレ立て時刻が被った場合
if ($_POST['subject']) DispError2("ＥＲＲＯＲ！","ERROR: 別の人が同時刻にスレッドを立てようとしています。再度お試しください。");
#スレッドのデータを読み込む
$LOG = file($thread_file);
#スレッドのレス数=現在のレス番を取得
$number = count($LOG) + 1;
#スレッドタイトルと>>1の情報を取得
list($nb,$name,$mail,$time,$nid,$message,$info,$subject,$threadinfo,,,,$rsid,,$rip,$rfip,) = explode("<>",$LOG[0]);
#スレッド設定をSETTINGに反映
if (!$BSETTING['Forced_Setting']) {
 $SETT = unserialize($threadinfo);
 foreach ($SETT as $key => $value) $SETTING[$key] = $value;
}
# 主判定
if ($rsid == $SID || $_SERVER['REMOTE_ADDR'] == $rip || $_SESSION['REMOTE_ADDR'] == $rfip) $nusi = 1;
# 副主/アク禁
if (!$nusi) {
if ($SETTING[$SID] == "sub" || $SETTING[$_SERVER[REMOTE_ADDR]] == "sub" || $SETTING[$SESSION[REMOTE_ADDR]] == "sub") $subnusi = 1;
}
if ($SETTING['BBS_DISABLE_NUSI'] == "checked") {
$nusi = 0;
$subnusi = 0;
}
# 新規と判定する秒数
$stime = 600;
# lifetimeルール
#if ($BSETTING['BBS_THREAD_LIFETIME'] and $NOWTIME > $_POST['key'] + $BSETTING['BBS_THREAD_LIFETIME']) DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
if (!$SETTING['MAX_RES']) $SETTING['MAX_RES'] = 1000;
if (!$BSETTING['MAX_RES']) $BSETTING['MAX_RES'] = 1000;
elseif ($SETTING['MAX_RES'] > 2000) $SETTING['MAX_RES'] = 2000;
elseif ($SETTING['MAX_RES'] < 300) $SETTING['MAX_RES'] = 300;
if (strpos($subject, '実況') !== false) $SETTING['LIVE_THREAD'] = 1;
#############################################################################
# 上限超えの処理
#############################################################################
# 1000/2000超えの処理をする
if ($number > $SETTING['MAX_RES'] or $number > 2000) {
	if ($number == $SETTING['MAX_RES'] + 1) {
		if (is_file($BBSSERV.$_POST['bbs']."/1000.txt")) $maxmsg = @file_get_contents($BBSSERV.$_POST['bbs']."/1000.txt");
		if (!$maxmsg) $maxmsg = " このスレッドは".$SETTING['MAX_RES']."を超えました。<br>これ以上書き込みはできません。 ";
		$fp = @fopen($thread_file, "a");
		fputs($fp, "<>$number<><>Over ".$SETTING['MAX_RES']." Thread<><>".$maxmsg."<><><><><><><><><><>");
		fclose($fp);
	}
	# 1100/2100超え緊急ストッパー(最後の手段)
	if ($number > $SETTING['MAX_RES'] + 100 or $number > 2100) DispError2("ＥＲＲＯＲ！","ERROR: このスレッドには書き込めません。最後の手段!!","1032 Last resort!;");
	# 1050/2050超え緊急ストッパー
	if ($number > $SETTING['MAX_RES'] + 50 or $number > 2050) DispError2("ＥＲＲＯＲ！","ERROR: このスレッドには書き込めません。緊急緊急緊急!!","1031 Emergency!;");
	DispError2("ＥＲＲＯＲ！","ERROR: このスレッドはレス数の上限を超えているので書けません。","1030 Thread is stopped;");
}
# 1000超え処理（板）- 最終書き込みから 10 秒以上経過
if ($number > $BSETTING['MAX_RES']) {
 list(,,,$t,) = explode("<>", $LOG[$number-2]);
 if ($NOWTIME - $t > 10) DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
}
	if ($SETTING['THREAD_STOP'] == "yes") DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
	if ($SETTING['BBS_FORCE_NONAME'] == "yes" and !$admin) {
	$_POST['FROM'] = "";
	$SETTING['NANASHI_CHECK'] = 0;
	}
	if ($SETTING['NOPIC'] == "checked") {
	if (preg_match('/.(gif|jpg|jpeg|png)/', $_POST[MESSAGE]) || strpos($_POST['MESSAGE'], 'imgur.com') !== false) DispError2("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドは画像の投稿が禁止されています。","9990 Banned;");
	}
	if ($SETTING['timeinterval']) {
	 list(,,,$t,) = explode("<>", $LOG[$number-2]);
	 if ($NOWTIME < $t + $SETTING['timeinterval']) DispError("ＥＲＲＯＲ！","ERROR: Sorry このスレッドでは直前の投稿から".$SETTING['timeinterval']."秒経たなければ書き込むことが出来ません。");
	}
}else {
	# 新規スレッドの場合
	if ($_POST['subject']) {
	#ログ格納場所をチェック	なければ作成
	if(!file_exists($BBSSERV.$_POST['bbs']."/")) @mkdir($BBSSERV.$_POST['bbs']."/", 0777);
	if(!file_exists($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/")) @mkdir($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/", 0777);
	if(!file_exists($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/")) @mkdir($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/", 0777);
	$number = 1;
	$message = $_POST['MESSAGE'];
	$info = "";
	$subject = $_POST['subject'];
	$nusi = 1;
	$LOG = array();
	$nprocess = true;
	}else {
	DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
	}
}
#############################################################################
# 
#############################################################################
if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) $cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$_POST['bbs'].$_POST['key'].$_POST['time'].$subject.$REMOTEADDR.$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
if (!$login) {
#--------------未ログイン時の処理 ここから-------
#-------------------------------認証鍵
if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') === false and !$jane and !$kakunindame and $SETTING['RES_CHECK'] == "checked") {
	if (!$_COOKIE['cert'] or !$_COOKIE['time'] or $_COOKIE['time'] < $NOWTIME - 3600) {
	 $cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$_POST['bbs'].$_POST['key'].$NOWTIME.$subject.$REMOTEADDR.$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
	 setcookie("cert", $cert, $NOWTIME+3600, "/");
	 setcookie("time", $NOWTIME, $NOWTIME+3600, "/");
	 HoutekiToukouKakunin();
	}else {
	 $cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$_POST['bbs'].$_POST['key'].$_COOKIE['time'].$subject.$REMOTEADDR.$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
	 if ($_COOKIE['cert'] and $_COOKIE['cert'] != $cert) HoutekiToukouKakunin();
	 if ($_COOKIE['time'] > $NOWTIME - 4) DispError("ＥＲＲＯＲ！","ERROR: 投稿間隔が短すぎます。","9801 Posting is so fast.;");
	}
}
#-------------------------------reCAPTCHA
if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) {
 if (isset($_POST['g-recaptcha-response'])) {
    $url = 'https://www.google.com/recaptcha/api/siteverify';
    $param = array(
      'secret' => '6Lc-RPUkAAAAAPTaL5FBC7zxj2FkRpg48lLQJcrI',
      'response' => $_POST['g-recaptcha-response']
    );
    $context = array(
      'http' => array(
        'method'  => 'POST',
        'header'  => 'Content-Type: application/x-www-form-urlencoded\r\n',
        'content' => http_build_query($param)
      )
    );
    $json = file_get_contents($url, false, stream_context_create($context));
    $results = json_decode($json,true);
    $success = $results["success"];
    $error = $results["error-codes"];
    if ($success == false or $error) {
	#reCAPTCHA認証に失敗
	DispError("ＥＲＲＯＲ！","ERROR: reCAPTCHA認証に失敗しました。再度お試しください。","9990 Banned;");
    }
 }
    if (!$_POST['submit']) $_POST['submit'] = "書き込む";
    $web = true;
    $approval = true;
}else {
	if ($_GET['manment']) DispError("ＥＲＲＯＲ！","ERROR: 新仕様に対応した専用ブラウザをご利用ください。","E3001 Unavailable an old dedicated browser.;");
}
#--------------未ログイン時の処理 ここまで-------
}
# 時間をチェック
if ($_POST['time'] > $NOWTIME) {
	$diff = $_POST[time] - $NOWTIME;
	DispError2("ＥＲＲＯＲ！","ERROR: 投稿時刻が不正です。(Diff:".$diff.")","1000 Post date is invalid;");
}
# 時間切れ
#if ($_POST['time'] < $NOWTIME - 86400) DispError("ＥＲＲＯＲ！","ERROR: 認証に失敗しました。スレッドをリロード、またはブラウザを再起動してください。","9990 Banned;");
# 認証用クエリ
#if ($_POST['cert'] and $_POST['cert'] != $cert) DispError("ＥＲＲＯＲ！","ERROR: 認証に失敗しました。スレッドをリロード、またはブラウザを再起動してください。","9990 Banned;");
#時間が読み込めなかったらばいばい
if (!$_POST['time']) DispError2("ＥＲＲＯＲ！","ERROR: 不正な投稿です。");
# sage/強制sage
if (strpos($_POST['mail'], 'sage') !== false) $sage = 'checked';
if ($BSETTING['BBS_SOKO'] == 'on') $sage = 1;
if ($BSETTING['BBS_SOKO'] == 'onon') $sage = 0;
#if ($BSETTING['BBS_SOKO'] == 'checked' and $number < 10) $sage = 1;
if ($BSETTING['BBS_SOKO'] == 'on' or $BSETTING['BBS_SOKO'] == 'onon' or $BSETTING['BBS_SOKO'] == 'ononon' and $NOWTIME - $_POST['key'] > 600) {
 if (strpos($_POST['mail'], 'soko') !== false) $soko = 1;
}
if (strpos($_POST['mail'], 'age') !== false and strpos($_POST['mail'], 'sage') === false) $sage = 0;
if ($BSETTING['BBS_FORCE_SAGE'] and $NOWTIME > $_POST['key'] + $BSETTING['BBS_FORCE_SAGE']) $sage = 1;
if ($SETTING['FORCE_SAGE'] == 'on') $sage = 'checked';

# ログイン必須
if ($SETTING['BBS_BE_ID'] == "1" and !$login) DispError("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドはログインユーザーのみ投稿することができます。","G7001 Required login;");

# 勢い1万以上のスレは調整
$a = $NOWTIME - $_POST[key];
$b = $number / $a;
$ikioi = round($b * 86400,1);
if ($ikioi > 99) $ikioi = floor($ikioi);
if ($ikioi > 10000 and $number > 50 and !$login) DispError2("ＥＲＲＯＲ！","ERROR: スレッド速度が速すぎるため非ログインユーザーに制限を設けております。","8904 Rejected;");
if ($ikioi > 100000 and $number > 100) DispError2("ＥＲＲＯＲ！","ERROR: スレッド速度が速すぎるため制限を設けております。","8902 Rejected;");

# ユニコード変換
if ($SETTING['BBS_UNICODE'] == "deny") {
	if ($emoji) DispError2("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドはUNICODE・絵文字の使用が禁止されています。","9990 Banned;");
}elseif ($SETTING['BBS_UNICODE'] == "change") {
	$_POST['subject'] = preg_replace("/\&\#\d+\;/", "？", $_POST['subject']);
	$_POST['MESSAGE'] = preg_replace("/\&\#\d+\;/", "？", $_POST['MESSAGE']);
	$_POST['subject'] = preg_replace("/\&\#x1F\d+\;/", "？", $_POST['subject']);
	$_POST['MESSAGE'] = preg_replace("/\&\#x1F\d+\;/", "？", $_POST['MESSAGE']);
}

# 書けない板
if ($SETTING['BBS_HEISA'] == "checked" or $BSETTING['BBS_HEISA'] == "checked") DispError("ＥＲＲＯＲ！","ERROR: この板は書き込み停止状態のため、キャップでなければ投稿することができません。");
#############################################################################
# dat落ち
#############################################################################
if (substr($_POST['key'], 0, 3) != 900 and substr($_POST['key'], 0, 3) != 924 and !$_POST['subject']) {
	# 即死判定
	if (!$BSETTING['BBS_TH_LINE']) $BSETTING['BBS_TH_LINE'] = 1;
	if (!$BSETTING['TIME_TO_LIVE']) $BSETTING['TIME_TO_LIVE'] = 1209600;
#	if ($NOWTIME > $_POST['key'] + $BSETTING['TIME_TO_LIVE'] and $BSETTING['BBS_TH_LINE'] > $number) DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
	# 突然死判定
#	if ($BSETTING['BBS_MAX_MODIFIED'] and $NOWTIME > filemtime($thread_file) + $BSETTING['BBS_MAX_MODIFIED']) DispError2("ＥＲＲＯＲ！","ERROR: 該当するスレッドがありません。https://".$_SERVER[HTTP_HOST]."/test/read.cgi/".$_POST[bbs]."/".$_POST[key]."/","1021 Thread is not alive;");
	# スレ欄から非表示
	if ($SETTING['MAX_RES'] - 5 < $number or $SETTING['THREAD_STOP'] == "yes" or ($BSETTING['BBS_THREAD_LIFETIME'] and $NOWTIME > $_POST['key'] + $BSETTING['BBS_THREAD_LIFETIME'])) $hide = "hide";
}

#############################################################################
# 串/VPN/TOR規制
#############################################################################
# PROXY判定
if (isset($_SERVER['HTTP_X_FORWARDED_FOR']) and $_SERVER['HTTP_X_FORWARDED_FOR']) {
	if ($_SERVER['REMOTE_ADDR'] != $_SERVER['HTTP_X_FORWARDED_FOR'] and $HOST != $_SERVER['HTTP_X_FORWARDED_FOR']) {
	$KUSICHECK = "Proxy05";
	$REMOTE_HOST .= ",".$_SERVER['HTTP_X_FORWARDED_FOR'];
	}
}
if (isset($_SERVER['HTTP_VIA']) and $_SERVER['HTTP_VIA']) {
	$KUSICHECK = "Proxy02";
	$REMOTE_HOST .= ",".$_SERVER['HTTP_VIA'];
}
if (isset($_SERVER['HTTP_FORWARDED']) and $_SERVER['HTTP_FORWARDED']) {
	$KUSICHECK = "Proxy03";
	$REMOTE_HOST .= ",".$_SERVER['HTTP_FORWARDED'];
}
if (isset($_SERVER['HTTP_CACHE_INFO']) and $_SERVER['HTTP_CACHE_INFO']) {
	$KUSICHECK = "Proxy04";
}
if (isset($_SERVER['HTTP_CLIENT_IP']) and $_SERVER['HTTP_CLIENT_IP']) {
	endhtml("9999 Not yet;");
#	$KUSICHECK = "Proxy05";
}
if (isset($_SERVER['HTTP_PROXY_CONNECTION']) and $_SERVER['HTTP_PROXY_CONNECTION']) {
	$KUSICHECK = "Proxy06";
}
if (isset($_SERVER['HTTP_SP_HOST']) and $_SERVER['HTTP_SP_HOST']) {
	$KUSICHECK = "Proxy07";
	$REMOTE_HOST .= ",".$_SERVER['HTTP_FORWARDED'];
}
if (isset($_SERVER['HTTP_X_LOCKING']) and $_SERVER['HTTP_X_LOCKING']) {
	$KUSICHECK = "Proxy08";
	$REMOTE_HOST .= ",".$_SERVER['HTTP_X_LOCKING'];
}
if (isset($_SERVER['HTTP_TE']) and $_SERVER['HTTP_TE']) {
#	$KUSICHECK = "Proxy09";
}
if ($KUSICHECK) DispError("ＥＲＲＯＲ！","ERROR: このホストからはdelightに投稿することができません。");
# 串リスト
$IN = file($BBQSERV."proxy20.cgi");
foreach ($IN as $tmp){
	if (strpos($tmp, '#') !== false) continue;
	$tmp = trim($tmp);
	if (stristr($REMOTE_HOST, $tmp) || stristr($_SERVER['REMOTE_ADDR'], $tmp)) $PROXYCHECK = "Proxy20";
}

if ($PROXYCHECK) {
$slip = "8";
$BBX = "Burned BBQ (".$PROXYCHECK.")";
}

if (!$login and $BSETTING['Use_Banned'] == "checked") {
#--------------未ログイン時の処理 ここから-------
#############################################################################
# BAN
############################################################################
if ($_SESSION['kisei'] == "BAN" or $_SESSION['kisei'] == date('z')) DispError("ＥＲＲＯＲ！","ERROR: あなたはスパムであると判定されたためBANされました。※日付が変わってから再度お試しください","E3390 Unavailable key.;");
else $_SESSION['kisei'] = '';
if ($_COOKIE[TAKO] == "ODORI") DispError("ＥＲＲＯＲ！","ERROR: あなたはスパムであると判定されたためBANされました。&#128025;","9991 Banned;");
#--------------未ログイン時の処理 ここまで-------
}
#############################################################################
# BBM
#############################################################################
	if ($phone) {
	 $bbm_file = $BBQSERV."/bbm/".date('Ymd')."_".$phone.".cgi";
	 if (is_file($bbm_file) and $SETTING['BBS_BBX_PASS'] != "on") {
	  $BBM = "Burned BBM ".file_get_contents($bbm_file);
	  if (!$login) DispError("ＥＲＲＯＲ！","ERROR: この携帯（べっかんこ）はBBx規制中です。->".$phone."<br>".$BBM);
	 }elseif (is_file($bbm_file)) {
	  $BBM = file_get_contents($bbm_file);
	 }
	}
	if (!$BBM) $BBM = "NONE";
#############################################################################
# BBQ
#############################################################################
	$bbx_file = $BBQSERV."/bbq/".date('Ymd')."_".$file_ipaddr.".cgi";
	$banfile = $BBQSERV."/bbq/bbq_".$file_ipaddr.".cgi";
	$banfile1 = $BBQSERV."/bbq/".date('Ym')."_".$file_ipaddr.".cgi";
	$banfilea = $BBQSERV."/bbq/".date('Ym').substr(date("d"), 0, 1)."_".$file_ipaddr.".cgi";
	if (is_file($banfile)) $BBX = "Burned BBQ (Proxy60) BBR-".file_get_contents($banfile);
	elseif (is_file($banfile1)) $BBX = "Burned BBQ (Proxy60) BBR-".file_get_contents($banfile1);
	elseif (is_file($banfilea)) $BBX = "Burned BBQ (Proxy60) BBR-".file_get_contents($banfilea);
	elseif (is_file($bbx_file)) $BBX = "Burned BBQ (Proxy60) ".file_get_contents($bbx_file);
	if (!$BBX) $BBX = "NONE";
	elseif ($SETTING['BBS_BBX_PASS'] != "on" and !$login) DispError("ＥＲＲＯＲ！","ERROR: このホストはBBx規制中です。->".$HOST."<br>".$BBX,"5900 BBxed IP;");
#############################################################################
# URLチェック
#############################################################################
	if ($SETTING['DISABLE_LINK'] and preg_match('/(https?|ttps?):\S+/', $_POST['MESSAGE'])) DispError2("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドではリンクの投稿が禁止されています。","9990 Banned;");
#====================================================
#　フィールドサイズの判定
#====================================================
# 各種チェック
if (!$login) {
if (strlen($_POST['MESSAGE']) > $BSETTING['BBS_MESSAGE_COUNT']) DispError2("ＥＲＲＯＲ！","ERROR: 本文が長すぎます。 (Check:".strlen($_POST['MESSAGE'])."/".$BSETTING['BBS_MESSAGE_COUNT'].")");
if (strlen($_POST['FROM']) > $BSETTING['BBS_NAME_COUNT']) DispError2("ＥＲＲＯＲ！","ERROR: 名前が長すぎます。");
if (strlen($_POST['mail']) > $BSETTING['BBS_MAIL_COUNT']) DispError2("ＥＲＲＯＲ！","ERROR: メールアドレスが長すぎます。");
if (strlen($_POST['subject']) > $BSETTING['BBS_SUBJECT_COUNT']) DispError2("ＥＲＲＯＲ！","ERROR: スレッドタイトルが長すぎます。");
if ($emoji > $BSETTING['BBS_LINE_NUMBER'] * 3) DispError("ＥＲＲＯＲ！","ERROR: UNICODE・絵文字の個数が多すぎます。","9990 Banned;");
if (preg_match_all("/&gt;&gt;[0-9]/", $_POST['MESSAGE'], $matches) > $BSETTING['BBS_LINE_NUMBER'] * 2) DispError("ＥＲＲＯＲ！","ERROR: レスアンカーリンクの個数が多すぎます。","9990 Banned;");
}else {
	$maxkaigy = $BSETTING['BBS_LINE_NUMBER'] * 3;
	if (mb_strlen($_POST['MESSAGE'], 'SJIS') > 10000) DispError2("ＥＲＲＯＲ！","ERROR: 本文が長すぎます。 (Check:".mb_strlen($_POST['MESSAGE'], 'SJIS')."/10000)");
	if (mb_strlen($_POST['FROM'], 'SJIS') > 280) DispError2("ＥＲＲＯＲ！","ERROR: 名前が長すぎます。 (Check:".mb_strlen($_POST['FROM'], 'SJIS')."/280)");
	if (mb_strlen($_POST['mail'], 'SJIS') > 280) DispError2("ＥＲＲＯＲ！","ERROR: メールアドレスが長すぎます。 (Check:".mb_strlen($_POST['mail'], 'SJIS')."/280)");
	if (mb_strlen($_POST['subject'], 'SJIS') > 280) DispError2("ＥＲＲＯＲ！","ERROR: スレッドタイトルが長すぎます。 (Check:".mb_strlen($_POST['subject'], 'SJIS')."/280)");
}
#--------------ログイン時の処理 ここまで-------
#############################################################################
# BBQ
#############################################################################
#if (is_file($BBSSERV."/".date('z')."/proxy_".$file_ipaddr.".cgi")) $kushi = @file_get_contents($BBSSERV."/".date('z')."/proxy_".$file_ipaddr.".cgi");
#
#if (!$kushi) {
#//オプション設定
#$options =array(
#        'http' =>array(
#                'method' => "GET",
#                )
#        );
#$url = "https://spur.us/context/".$REMOTEADDR;
#$cp = curl_init();
#/*オプション:リダイレクトされたらリダイレクト先のページを取得する*/
#curl_setopt($cp, CURLOPT_RETURNTRANSFER, 1);
#/*オプション:URLを指定する*/
#curl_setopt($cp, CURLOPT_URL, $url);
#/*オプション:タイムアウト時間を指定する*/
#curl_setopt($cp, CURLOPT_TIMEOUT, 2000);
#/*オプション:ユーザーエージェントを指定する*/
#curl_setopt($cp, CURLOPT_USERAGENT, "Mozilla/5.0 P2/2.5 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1");
#curl_setopt($cp, CURLOPT_HEADER, true);
#$source = curl_exec($cp);
#$curlInfo = curl_getinfo($cp);
#   // ヘッダを一緒に出力したときは分割させる
#   $headerSize = 0;
#   if ( isset($curlInfo["header_size"]) && $curlInfo["header_size"]!="" ) {
#      $headerSize = $curlInfo["header_size"];
#   }
#   $head = substr($source, 0, $headerSize); // ヘッダ部
#$head = str_replace(["\r\n", "\r", "\n"], "\n", $head);
#$header = explode("\n", $head);
#foreach ($header as $tmp) {
#	list($key, $value) = explode(": ", $tmp);
#	$HTTP[$key] = $value;
#}
#   $kushi = substr($source, $headerSize);    // ボディ部
#curl_close($cp);
#@file_put_contents($BBSSERV."/".date('z')."/proxy_".$file_ipaddr.".cgi", $kushi);	#キャッシュ
#	}
#if ($kushi and strpos($kushi, 'Not Anonymous') === false) {
#if (strpos($kushi, 'Possible Proxy') === false) $slip = "h";
#else $BBX = "Burned BBQ (Proxy60)";
#}
#############################################################################
# ISP解析（県名＆串・モバイル判定）
#############################################################################
if ($slip == "d" || $slip == "D") $ken = "茸";
elseif ($slip == "a") $ken = "光";
elseif ($slip == "r") $ken = "SB-Android";
elseif ($slip == "p") $ken = "SB-iPhone";
elseif ($slip == "x") $ken = "空";
elseif ($slip == "E") $ken = "芋";
elseif ($slip == "M") $ken = "ジパング";
elseif ($slip == "F") $ken = "公衆";
elseif ($slip == "H") $ken = "catv?";
else $ken = "pc?";
#if (is_file($BBSSERV."/".date('z')."/ip_".$file_ipaddr.".cgi")) $data = @file_get_contents($BBSSERV."/".date('z')."/ip_".$file_ipaddr.".cgi");
#	if (!$data) {
#//オプション設定
#$options =array(
#        'http' =>array(
#                'method' => "GET",
#                )
#        );
#$url = "http://ip-api.com/json/".$REMOTEADDR."?fields=countryCode,regionName,city,asname,mobile,proxy,hosting&lang=ja";
#$cp = curl_init();
#/*オプション:リダイレクトされたらリダイレクト先のページを取得する*/
#curl_setopt($cp, CURLOPT_RETURNTRANSFER, 1);
#/*オプション:URLを指定する*/
#curl_setopt($cp, CURLOPT_URL, $url);
#/*オプション:タイムアウト時間を指定する*/
#curl_setopt($cp, CURLOPT_TIMEOUT, 2000);
#/*オプション:ユーザーエージェントを指定する*/
#curl_setopt($cp, CURLOPT_USERAGENT, "Mozilla/5.0 P2/2.5 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1");
#curl_setopt($cp, CURLOPT_HEADER, true);
#$source = curl_exec($cp);
#$curlInfo = curl_getinfo($cp);
#   // ヘッダを一緒に出力したときは分割させる
#   $headerSize = 0;
#   if ( isset($curlInfo["header_size"]) && $curlInfo["header_size"]!="" ) {
#      $headerSize = $curlInfo["header_size"];
#   }
#   $head = substr($source, 0, $headerSize); // ヘッダ部
#$head = str_replace(["\r\n", "\r", "\n"], "\n", $head);
#$header = explode("\n", $head);
#foreach ($header as $tmp) {
#	list($key, $value) = explode(": ", $tmp);
#	$HTTP[$key] = $value;
#}
#   $data = substr($source, $headerSize);    // ボディ部
#curl_close($cp);
#@file_put_contents($BBSSERV."/".date('z')."/ip_".$file_ipaddr.".cgi", $data);	#キャッシュ
#	}
#$area = json_decode($data, true);
#@mb_convert_variables('SJIS-win','UTF-8',$area);
#if (!$area["asname"]) $area["asname"] = preg_replace("/[0-9]/", "", $HOST);
## 国名
#if (!$_SERVER[HTTP_CF_IPCOUNTRY]) {
#if ($area["countryCode"]) $_SERVER[HTTP_CF_IPCOUNTRY] = $area["countryCode"];
#else $_SERVER[HTTP_CF_IPCOUNTRY] = "JP";
#}
# 海外ドメイン規制
if ($SETTING['BBS_FOREIGN_PASS'] != "on" and $_SERVER[HTTP_CF_IPCOUNTRY] != "JP" and !$login) DispError("ＥＲＲＯＲ！","ERROR: 海外ドメイン規制中です！ (".$_SERVER[HTTP_CF_IPCOUNTRY].")");
if ($_SERVER[HTTP_CF_IPCOUNTRY] != "JP") {
	$SLIP_NAME = $_SERVER[HTTP_CF_IPCOUNTRY];
	$slip = "H";
}
# モバイルを検出
if ($area['mobile'] == true and $slip == "0" and strpos($HOST, 'bbtec.net') === false and strpos($HOST, 'ocn.ne.jp') === false and strpos($HOST, 'dion.ne.jp') === false) {
$slip = "S";
$SLIP_SP = 1;
$SLIP_NAME = $area["asname"];
}
# 県名
if (!$area["regionName"]) $area["regionName"] = "catv?";
if ($SETTING['BBS_JP_CHECK'] == 1) $ken = $area["regionName"];
elseif ($SETTING['BBS_JP_CHECK'] == 2) $ken = $area["city"];
elseif ($SETTING['BBS_JP_CHECK'] == 3) $ken = $area["regionName"].$area["city"];
elseif ($SETTING['BBS_JP_CHECK'] == 4) $ken = $area["asname"];
elseif ($SETTING['BBS_JP_CHECK'] == 5) $ken = $area["regionName"]." ".$area["asname"];
elseif ($SETTING['BBS_JP_CHECK'] == 6) $ken = $area["regionName"].$area["city"]." ".$area["asname"];
if ($area["city"] == "Chiyoda") {
 if ($slip == "d") $ken = "茸";
 elseif ($slip != "0") $ken = "光";
 elseif ($area["asname"] == "KDDI" or strpos($HOST, 'dion.ne.jp') !== false) $ken = "dion軍";
}
if ($area["city"] == "東京" or $area["city"] == "大阪市") {
 if ($slip == "d") $ken = "茸";
 elseif ($slip == "M") $ken = "ジパング";
 elseif ($slip != "0") $ken = "光";
 elseif ($area["asname"] == "KDDI" or strpos($HOST, 'dion.ne.jp') !== false) $ken = "dion軍";
}
if ($area["city"] == "港区") {
 if ($slip == "p") $ken = "SB-iPhone";
 elseif ($slip == "r") $ken = "SB-Android";
 elseif ($area["asname"] == "GIGAINFRA" or strpos($HOST, 'bbtec.net') !== false) $ken = "やわらか銀行";
}
$ken = trim($ken);
# PROXYを検出
if ($area['proxy'] == true) $slip = "8";
# hostingを検出
if ($area['hosting'] == true and $slip != "8") $slip = "h";
# 広域ID（県+ISP+OS+ブラウザ）
$rdata = $area["regionName"].$area["asname"].$platform.$browser.$USER_AGENT;
$rid = hash('sha256', $rdata);
if (!$PROXYCHECK) $PROXYCHECK = "NONE";
if ($admin) $ken = "★";
# BBS_PROXY_CHECK=checked 逆引きできないIPアドレス規制
if ($SETTING['BBS_PROXY_CHECK'] == "checked" and !$login) {
 if ($HOST == $_SERVER['REMOTE_ADDR'] and !$SLIP_SP and !$MM and !$WF) DispError("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドでは逆引きできないホストからの投稿が禁止されています。","9990 Banned...;");
}
#if ($slip != '0' && !$login) DispError("ＥＲＲＯＲ！","ERROR: このスレッドにはもう書き込めませんでした。[".$_POST['bbs']."]","9990 Banned...;");
#if ($_POST['subject']) DispError("ＥＲＲＯＲ！","ERROR: この端末ではスレッドが立てられません。[".$_POST['bbs']."]","9990 Banned...;");
#############################################################################
# PROXY規制
#############################################################################
 # 国コードが日本なのに県名が日本名でない場合はほぼ串確定
# if ($area["regionName"] and $_SERVER[HTTP_CF_IPCOUNTRY] == "JP" and strlen($area["regionName"]) == mb_strlen($area["regionName"],"SJIS")) $BBX = "Burned BBQ (Proxy10)";
# if ($slip == "8") $BBX = "Burned BBQ (Proxy01)";
# elseif ($slip == "h") $BBX = "Burned BBQ (Proxy20)";
#if ($SETTING['BBS_BBX_PASS'] != "on" and $BBX != "NONE" and !$login) DispError("ＥＲＲＯＲ！","ERROR: このホストはBBx規制中です。->".$HOST."<br>".$BBX,"5900 BBxed IP;");
#====================================================
#　IDを生成する
#====================================================
 if ($SETTING['BBS_SLIP'] == "vvvvvv") $SLIP_SERV = substr(hash('sha256', date("Ym").substr(date("d"), 0, 1).$_POST['bbs']."vvvvvv"), 2, 3);
 elseif ($SETTING['BBS_SLIP'] == "vvvvv") $SLIP_SERV = substr(hash('sha256', date("Ym").substr(date("d"), 0, 1).$_POST['bbs']."vvvvv"), 2, 3);
 elseif ($SETTING['BBS_SLIP'] == "vvvv") $SLIP_SERV = substr(hash('sha256', date("Ym").substr(date("d"), 0, 1).$_POST['bbs']."vvvv"), 2, 3);
 else $SLIP_SERV = substr(hash('sha256', date("Ym").substr(date("d"), 0, 1).$_POST['bbs']), 2, 3);	#10日ごとに変わる+板毎に変わる
if (!$range) $range = $iprange;
# KOROKORO
$SLIP_IP = substr(hash('sha256', $range.$SLIP_SERV), 2, 2);	#IP先頭
$SLIP_ID = substr(hash('sha256', $area["regionName"].$area["asname"].$area['mobile'].$SLIP_SERV), 2, 2);	#プロバイダ
$SLIP_AC = substr(hash('sha256', $USER_AGENT.$SLIP_SERV), 2, 2);	#ブラウザ
if ($login) $SLIP_TE = substr(hash('sha256', $_COOKIE[secretkey].$SLIP_SERV), 2, 2);	#gmail
else $SLIP_TE = substr(hash('sha256', $terminal.$SLIP_SERV), 2, 2);	#端末
# 細分化ID末尾
if ($SETTING['BBS_SLIP']) {
if ($SLIP_SP and $slip != "S") $SLIP_AREA = strtoupper(substr(hash('sha256', $SLIP_IP), 2, 1));
else $SLIP_AREA = strtoupper(substr(hash('sha256', $SLIP_ID), 2, 1));
}
# 従来式ID
if (!$SETTING['BBS_ID_CHANGE']) {
 if ($SETTING['BBS_DIVID']) $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['bbs'].date("Ymdi")), 2, 8);
 elseif ($SETTING['BBS_SLIP'] == "vvvvvv") $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['bbs'].date("Ymd")."vvvvvv"), 2, 8);
 elseif ($SETTING['BBS_SLIP'] == "vvvvv") $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['bbs'].date("Ymd")."vvvvv"), 2, 8);
 elseif ($SETTING['BBS_SLIP'] == "vvvv") $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['bbs'].date("Ymd")."vvvv"), 2, 8);
 else $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['bbs'].date("Ymd")), 2, 8);
}else {
 if (!$SETTING['BBS_DIVID']) $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['key'].date("Ymd")), 2, 8);	#スレ毎にIDを変える
 else $idcrypt = substr(hash('sha256', $_SERVER['REMOTE_ADDR'].$_POST['key'].date("Ymdi")), 2, 8);
}
$idcrypt = substr(crypt(substr($idcrypt, 2),substr($idcrypt, 0, 2)), 2, 8);
$idcrypt = preg_replace('/\./','+',$idcrypt);
$idcrypt = str_replace('/','+',$idcrypt);
$idcrypt = str_replace('+','0',$idcrypt);
# 識別ID
if (!$SETTING['BBS_ID_CHANGE']) {
 if ($SETTING['BBS_SLIP'] == "vvvvvv") $IDYMD = date("Ymd")."vvvvvv";
 elseif ($SETTING['BBS_SLIP'] == "vvvvv") $IDYMD = date("Ymd")."vvvvv";
 elseif ($SETTING['BBS_SLIP'] == "vvvv") $IDYMD = date("Ymd")."vvvv";
 else $IDYMD = date("Ymd");
$CCC = substr(hash('sha256', $range.$_POST['bbs'].date("Ymd")), 2, 5);	#IP先頭
$DDD = substr(hash('sha256', $area["regionName"].$_POST['bbs'].date("Ymd")), 2, 5);	#県
$PRB = substr(hash('sha256', $area["asname"].$area['mobile'].$_POST['bbs'].date("Ymd")), 2, 5);	#プロバイダ
$TE = substr(hash('sha256', $terminal.$_POST['bbs'].date("Ymd")), 2, 3);	#端末
$AC = substr(hash('sha256', $USER_AGENT.$_POST['bbs'].date("Ymd")), 2, 3);	#ブラウザ
$SS = substr(hash('sha256', $_SESSION['REMOTE_ADDR'].$_POST['bbs'].date("Ymd")), 2, 4);	#鍵/gmail
}else {
#スレ毎
$CCC = substr(hash('sha256', $range.$_POST['key'].date("Ymd")), 2, 5);	#IP先頭
$DDD = substr(hash('sha256', $area["regionName"].$_POST['key'].date("Ymd")), 2, 5);	#県
$PRB = substr(hash('sha256', $area["asname"].$area['mobile'].$_POST['key'].date("Ymd")), 2, 5);	#プロバイダ
$TE = substr(hash('sha256', $terminal.$_POST['key'].date("Ymd")), 2, 3);	#端末
$AC = substr(hash('sha256', $USER_AGENT.$_POST['key'].date("Ymd")), 2, 3);	#ブラウザ
$SS = substr(hash('sha256', $_SESSION['REMOTE_ADDR'].$_POST['key'].date("Ymd")), 2, 4);	#鍵/gmail
}
$ID = "ID:".$idcrypt;
if (!$SLIP_SP and !$MM) $AAA = substr(hash('sha256', $area["regionName"].date("Ymd")), 2, 5);	#県(固定回線)
else $AAA = substr(hash('sha256', $_SESSION['REMOTE_ADDR'].date("Ymd")), 2, 5);	#IP
$FFF = substr(hash('sha256', $_SESSION['REMOTE_ADDR'].date("Ymd")), 2, 5);
$HHH = substr(hash('sha256', $rid.date("Ymd")), 2, 5);	#ドメイン+県+OS+ブラウザ
$EEE = $TE.$AC;	#端末+ブラウザ
$III = substr(hash('sha256', $USER_AGENT.date("Ymd")), 2, 5);	#ブラウザ値のみ
$UID_DATA = $idcrypt." ".$AAA." ".$CCC." ".$DDD." ".$EEE." ".$FFF."  ".$HHH." ".$III;
# モバイル関連
if ($MM) {
	$SLIP_ID = $SLIP_IP;
	$SLIP_SMF = "M" . $SLIP_AREA;
}elseif ($SLIP_SP) {
	$SLIP_ID = $SLIP_IP;
	$SLIP_SMF = $slip . $SLIP_AREA;
}elseif ($WF) {
	$SLIP_ID = $SLIP_IP;
	$SLIP_SMF = "F" . $SLIP_AREA;
}
if ($SLIP_SMF) {
	$SLIP_KEN = $SLIP_SMF;
	$SLIP_IP = $SLIP_SMF;
}else $SLIP_KEN = $SLIP_AREA . strtoupper(substr(hash('sha256', $SLIP_IP), 2, 1));
# 識別ID
$SLIP = $SLIP_KEN."-".$SS.$TE.$AC.substr($PRB, 0, 2).substr($DDD, 0, 2).substr($CCC, 0, 2);	#回線/県名-鍵/gmail+端末+ブラウザ+プロバイダ+県+IP先端
#############################################################################
# 連投規制/コピペ規制
#############################################################################
#制限値は(Lv*10)くらい？	>>1-10までは緩めに スレ主/副主はスレ立て時以外は適用しない
#-------------------------------投稿内容を判定
 #未ログイン時で本文が半角文字のみ
 if ($SETTING['JAPANESE_CHECK'] == "checked" and strlen($_POST[MESSAGE]) == mb_strlen($_POST[MESSAGE],"SJIS") and !$login) DispError("ＥＲＲＯＲ！","ERROR: この掲示板・スレッドでは未ログイン時の日本語を含まない投稿が禁止されています。","9990 Banned;");
#-------------------------------本文を行ごとに分割
$tags = array(); 	#ハッシュタグを格納する配列
$ca = 1;
$crkct = 0;
$msgar = array_filter($msgbr);	#空の行を削除
	foreach ($msgbr as $tmp) {
	if ($tmp and $tmpstr) {
	similar_text($tmpstr, $tmp, $perc);
	if ($tmpst1) similar_text($tmpst1, $tmp, $per1);
	if ($perc >= 95 or $per1 >= 95) ++$crkct;
	$tmpst1 = $tmpstr;
	}
	if (strlen($tmp) > 3) $tmpstr = $tmp;
	if (strpos(substr($tmp, 0, 4),'&gt;') !== false and !preg_match("/&gt;&gt;[0-9]/", $tmp)) $tmp = '<div style="display:block;margin-left:8px;padding:6px 0px 6px 12px;border-left:solid 3px rgb(103, 103, 103);opacity:0.7;"><font color="gray"> '.$tmp.' </font></div>';	#引用
	if (strpos(mb_substr($tmp, 0, 1, "SJIS"),'＞') !== false) $tmp = '<div style="display:block;margin-left:8px;padding:6px 0px 6px 12px;border-left:solid 3px rgb(103, 103, 103);opacity:0.7;"><font color="gray"> '.$tmp.' </font></div>';	#引用
	if (strpos(substr($tmp, 0, 1),'*') !== false) $tmp = '<b> '.$tmp.' </b>';	#太字
	if (strpos(substr($tmp, 0, 1),'_') !== false) $tmp = '<i> '.$tmp.' </i>';	#斜体
	if (strpos(substr($tmp, 0, 1),'-') !== false) $tmp = '<s> '.$tmp.' </s>';	#取り消し線
	if (strpos(substr($tmp, 0, 1),'^') !== false) $tmp = '<small style="opacity: 0.7;"> '.$tmp.' </small>';	#目立たなくする
	if (strpos(substr($tmp, 0, 1),'~') !== false) $tmp = '<span class="_mfm_blur_"> '.$tmp.' </span>';	#ぼかし
	if (strpos(substr($tmp, 0, 1),'\\') !== false) $tmp = '<center> '.$tmp.' </center>';	#中央寄せ
	if (strpos(substr($tmp, 0, 1),'@') !== false) $tmp = '<font color="green"> '.$tmp.' </font>';	#緑字
	if (strpos(substr($tmp, 0, 1),'#') !== false) {
	 list($tmpa,) = explode(" ",$tmp);
	 list($tmpb,) = explode("　",$tmpa);
	 $hashtag = substr($tmpb, 0, 41);
	 $HASHT = str_replace("#", "", $hashtag);
	 $tmp = str_replace($hashtag, '<a href="/hashtag/'.$HASHT.'/">'.$hashtag.'</a>', $tmp);
	 array_push($tags,mb_convert_encoding($HASHT, 'HTML-ENTITIES', 'SJIS-win'));
	}
	if ($ca == 1) $_POST['MESSAGE'] = $tmp;
	else $_POST['MESSAGE'] .="<br>".$tmp;
	++$ca;
	}
	if ($crkct >= 2) {
	if (!$login) DispError("ＥＲＲＯＲ！","ERROR: 未ログインユーザーは同一あるいは類似した行を反復することができません。","9990 Banned;");
	else $_POST['MESSAGE'] .= '<br><small style="color: #F66;">(同一行反復)</small>';
	}
# アイコン
if ($_POST['icon'] == "on" and $_COOKIE['icon'] and $SETTING['DISABLE_ICON'] != "checked") {
 if (strlen($_COOKIE['icon']) > 1000) DispError2("ＥＲＲＯＲ！","ERROR: このアイコンは使用できません");
 if (strpos($_COOKIE['icon'],'javascript') !== false or strpos($_COOKIE['homepage'],'javascript') !== false or strpos($_COOKIE['icon'],'(') !== false or strpos($_COOKIE['icon'],')') !== false or strpos($_COOKIE['icon'],'http') === false or strpos($_COOKIE['icon'],'://') === false) DispError2("ＥＲＲＯＲ！","ERROR: このアイコンは使用できません");
 if ($_COOKIE['homepage']) {
  if (strpos($_COOKIE['homepage'],'(') !== false or strpos($_COOKIE['homepage'],')') !== false or strpos($_COOKIE['homepage'],'http') === false or strpos($_COOKIE['homepage'],'://') === false) DispError2("ＥＲＲＯＲ！","ERROR: このアイコンは使用できません");
 }
 if ($_COOKIE['homepage']) $_POST['MESSAGE'] = '<a href="'.$_COOKIE[homepage].'" target="_blank"><img src="'.$_COOKIE[icon].'" class="icon" width="50" height="50" align="left"></a>'.$_POST['MESSAGE'];
 else $_POST['MESSAGE'] = '<img src="'.$_COOKIE[icon].'" class="icon" width="50" height="50" align="left">'.$_POST['MESSAGE'];
}
	#本文前後に空白を挿入
	$_POST['MESSAGE'] = " ".$_POST['MESSAGE']." ";
	if ($_POST['subject']) $message = $_POST['MESSAGE'];
# AAモード
	if ($aa || $SETTING['BBS_AA']) {
	$_POST[MESSAGE] = trim($_POST[MESSAGE]);
	$_POST[MESSAGE] = ' <span class="AA">'.$_POST[MESSAGE].'</span> ';
	}
# その他機能
	if (strpos($_POST['FROM'], 'tasukeruyo') !== false) {
		$_POST['FROM'] = str_replace("tasukeruyo", "</b>".$HOST."<b>", $_POST['FROM']);
		$_POST[MESSAGE] .= "<hr><var style='color:blue;'>".$_SERVER[HTTP_USER_AGENT]."</var> ";
	}
	if (strpos($_POST['MESSAGE'], '!chkBBx:') !== false) {
		$_POST[MESSAGE] .= "<hr><var style='color:blue;'>Region: [".$_SERVER[HTTP_CF_IPCOUNTRY]."]<br>QUERY:[".$REMOTEADDR."] (".$area["regionName"].$area["city"]." ".$area["asname"].") (".$SLIP_NAME." ".$SLIP_IP.$SLIP_ID."-".$SLIP_TE.$SLIP_AC.")<br>HOST NAME: ".$HOST."<br>IP: ".$REMOTEADDR."<br>CITY: ".$area["regionName"].$area["city"]."<br>SLIP: ".$SLIP."<br>UA: ".$browser."<br>-- Results<br>BBQ: ".$BBX."<br>BBM: ".$BBM."<br>-- End of job.</var> ";
	}
# レス情報欄
$info = $UID_DATA."|".$_SERVER['REMOTE_PORT']."|".$_SERVER[HTTP_CF_IPCOUNTRY]."|".$rid."|".$REMOTEADDR."|(".$area["regionName"].$area["city"]." ".$area["asname"].") (".$SLIP_NAME." ".$SLIP_IP.$SLIP_ID."-".$SLIP_TE.$SLIP_AC.")||".$area['mobile'];
	if (strpos($_POST[MESSAGE], '!info') !== false) {
		$_POST[MESSAGE] .= "<hr><var style='color:blue;'>".$info."</var> ";
	}
#-------------------------------スレッド監視(>>21以降のみ)
if ($BSETTING['BBS_FR_LEVEL'] > 0 and $number > 20) {
	$num = 1;
	# スレごとのtimecover規制
	#H秒内
	if ($SETTING['RESET_POSTCOUNT'] == "year") $maxtime = 31536000;
	elseif ($SETTING['RESET_POSTCOUNT'] == "month") $maxtime = 2592000;
	elseif ($SETTING['RESET_POSTCOUNT'] == "10days") $maxtime = 864000;
	elseif ($SETTING['RESET_POSTCOUNT'] == "10hours") $maxtime = 36000;
	elseif ($SETTING['RESET_POSTCOUNT'] == "hour") $maxtime = 3600;
	elseif ($SETTING['RESET_POSTCOUNT'] == "10minutes") $maxtime = 600;
	elseif ($SETTING['RESET_POSTCOUNT'] == "minute") $maxtime = 60;
	else $maxtime = 86400;
	if (!$SETTING['timecover']) $SETTING['timecover'] = 10;
	$maxcount = $SETTING['timecover'] * 1.8;	#N回中
	$ngcount = $SETTING['timecover'] * 1.5;
	#大量投稿を検出
	foreach($LOG as $tmp){
	list($de,$n,$m,$t,$i,$mess,$in,,,,,,$trid,$rhost,$p,$sp,$mk,$pl,) = explode("<>",$tmp);
	 $t = substr($t, 0, 10);
	 list($iddata,) = explode("|",$in);
	  list($id1,$ida,$idc,$idd,$ide,$idf,,$idh,$idi) = explode(" ",$iddata);
	if ($number - $num < $maxcount and $NOWTIME - $t < $maxtime and !$nusi and !$subnusi and !$admin and !$login) {
	 if ($id1 == $idcrypt or $idf == $FFF) ++$tidc;	#ID or SIP
	 if ($ida == $AAA) ++$tidca;	#県名
	 if ($idc == $CCC) ++$tidcc;	#IP先端
	 if ($idd == $DDD) ++$tidcd;	#プロバイダ
	 if ($ide == $EEE) ++$tidce;	#端末+ブラウザ
	 if ($idh == $HHH) ++$tidch;	#ドメイン+県+OS+ブラウザ
	 if ($idi == $III) ++$tidci;	#ブラウザデータ
	}
	#連続投稿規制1
	if ($tidc > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: 一定時間内に連続してこのスレッドに書き込める上限に達しました。※スレッド毎連続投稿規制の値に関する問い合わせは各板の管理者へどうぞ。".$_POST['key']);
	}
	#広域規制
	if (!$SETTING['LIVE_THREAD'] and !$login and $BSETTING['BBS_FR_LEVEL'] > 2) {
	 if ($tidca > $SETTING['timecover'] or $tidcc > $SETTING['timecover'] or $tidcd > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: このスレッドでの広域規制の対象となっています。しばらくお待ちください。※ログインするとすぐに書き込めます。 1(".$_POST['key'].")");
	 }
	 if ($tidce > $SETTING['timecover'] or $tidch > $SETTING['timecover'] or $tidci > $ngcount) {
		DispError("ＥＲＲＯＲ！","ERROR: このスレッドでの広域規制の対象となっています。しばらくお待ちください。※ログインするとすぐに書き込めます。 2(".$_POST['key'].")");
	 }
	}
	#連続投稿規制2
	if ($number - $num < $maxcount and $NOWTIME - $t < $maxtime and ($p == $_SERVER['REMOTE_ADDR'] or $p == $_SESSION['REMOTE_ADDR'] or $sp == $_SERVER['REMOTE_ADDR'] or $sp == $_SESSION['REMOTE_ADDR'] or $SID == $trid) and !$nusi and !$subnusi and !$admin and !$login) ++$uidcount;
	if ($uidcount > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: 一定時間内に連続してこのスレッドに書き込める上限に達しました。※スレッド毎連続投稿規制の値に関する問い合わせは各板の管理者へどうぞ。".$_POST['key']);
	}
	#新規規制
	if ($number - $num < $maxcount and $NOWTIME - $t < $maxtime and $pl < $stime and $PHOEBELV < $stime and !$nusi and !$subnusi and !$admin and !$login and (!$SETTING['SINKI_PASS'] or $SETTING['SINKI_PASS'] == "no") and $BSETTING['BBS_FR_LEVEL'] > 4) ++$scount;
	if ($scount > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: 一定時間内に新規ユーザーが連続してこのスレッドに書き込める上限に達しました。他の人が書き込むのを待ってください。※ログインするとすぐ書けます ".$_POST['key']);
	}

	#文字数規制
	if ($number - $num < $maxcount and $NOWTIME - $t < $maxtime and strlen($mess) == strlen($_POST['MESSAGE']) and !$nusi and !$subnusi and !$admin and !$login and !$SETTING['LIVE_THREAD'] and $BSETTING['BBS_FR_LEVEL'] > 1) ++$bcount;
	if ($bcount > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: このスレッドでの広域規制の対象となっています。しばらくお待ちください。※ログインするとすぐに書き込めます。 3".$bcount);
	}

	#コピペを検知
	similar_text($mess, $_POST['MESSAGE'], $perc);

	#１つ前のレスが殆ど同一の場合は書き込まない
	if (($num == $number - 1 or $num == $number - 2) and $perc > 95 and !$SETTING['LIVE_THREAD'] and !$login and $BSETTING['BBS_FR_LEVEL'] > 1) DispError("ＥＲＲＯＲ！","ERROR: 未ログインユーザーは同じスレッドに同一・類似した投稿を連続して行うことはできません。 ".floor($perc));

	#コピペ規制
	if ($number - $num < $maxcount and $NOWTIME - $t < $maxtime and $perc > 95 and !$nusi and !$subnusi and !$admin and !$login and !$SETTING['LIVE_THREAD'] and $BSETTING['BBS_FR_LEVEL'] > 1) ++$mc;
	if ($mc > $SETTING['timecover']) {
		DispError("ＥＲＲＯＲ！","ERROR: このスレッドに同一・類似した投稿が大量に投稿されているため制限されました。本文を変えて再度お試しください。※ログインするとすぐに書き込めます。 ".$mc);
	}	
	
	++$num;
	}

}
#====================================================
#　書き込み情報のチェック
#====================================================
if (!isset($_SERVER['HTTP_REFERER']) or !$_SERVER['HTTP_REFERER']){
	#refererが無い場合
	endhtml("1020 No referrer;");
}
else {
	if (!stristr($_SERVER['HTTP_REFERER'], $_SERVER['HTTP_HOST'])){
		$str = parse_url($_SERVER['HTTP_REFERER']);
		DispError("ＥＲＲＯＲ！","ERROR: referer情報が不正です。(ref1)".$_SERVER['HTTP_REFERER'],"1021 invalid referrer.;");
	}
	if ($_SERVER['HTTP_HOST'] != $_SERVER['SERVER_NAME']){
		DispError("ＥＲＲＯＲ！","ERROR: ブラウザ情報が不正です。(host)".$_SERVER['HTTP_REFERER'],"1022 invalid host.;");
	}
}
#==================================================
#　スレ主用機能
#==================================================
if (($BSETTING['BBS_USE_VIPQ2'] and ($nusi or $subnusi)) or $admin) {
 if ($BSETTING['BBS_USE_VIPQ2'] == "checked" or $admin) {
	if (preg_match("/(.*)!add(.*)/", $_POST['MESSAGE'], $match) and $number != 1) {
	$nprocess = true;
	$message .="<br><font class=\"add\" color=\"red\">※追記 {$DATE}</font>{$match[2]}";
	}
	if (strpos($_POST['MESSAGE'], '!live') !== false) {
	$nprocess = true;
	$SETTING['LIVE_THREAD'] = 1;
	$message .="<br><font class=\"add\" color=\"red\">※実況モード(連投規制緩和)</font> ";
	}
	if (strpos($_POST['MESSAGE'], '!sage') !== false) {
	$nprocess = true;
	 if ($SETTING['FORCE_SAGE'] and $SETTING['FORCE_SAGE'] != "off") {
	 $SETTING['FORCE_SAGE'] = "off";
	 $message .="<br><font class=\"add\" color=\"red\">※強制sageを解除</font> ";
	 }else {
	 $SETTING['FORCE_SAGE'] = "on";
	 $message .="<br><font class=\"add\" color=\"red\">※強制sageを設定</font> ";
	 }
	}
	if (strpos($_POST['MESSAGE'], '!nopic') !== false) {
	$nprocess = true;
		if (!$SETTING['NOPIC']) {
		$SETTING['NOPIC'] = "checked";
		$message .="<br><font class=\"add\" color=\"red\">※画像投稿禁止</font> ";
		}else {
		$SETTING['NOPIC'] = "none";
		$message .="<br><font class=\"add\" color=\"red\">※画像禁止を解除</font> ";
		}
	}
	if (strpos($_POST['MESSAGE'], '!バルサン') !== false) {
	$nprocess = true;
		if (!$SETTING['BBS_PHOEBE'] or $SETTING['BBS_PHOEBE'] == "none" or $SETTING['BBS_PHOEBE'] < 2) {
		$SETTING['BBS_PHOEBE'] = 3;
		$message .="<br><font class=\"add\" color=\"red\">※バルサン(Lv2以下書込禁止)</font> ";
		}else {
		$SETTING['BBS_PHOEBE'] = "none";
		$message .="<br><font class=\"add\" color=\"red\">※バルサン解除</font> ";
		}
	}
	if (strpos($_POST['MESSAGE'], '!new') !== false) {
	$nprocess = true;
		if (!$SETTING['SINKI_PASS'] or $SETTING['SINKI_PASS'] == "no") {
		$SETTING['SINKI_PASS'] = "yes";
		$message .="<br><font class=\"add\" color=\"red\">※新規連投制限を解除</font> ";
		}else {
		$SETTING['SINKI_PASS'] = "no";
		$message .="<br><font class=\"add\" color=\"red\">※新規連投制限を有効化</font> ";
		}
	}
	if (strpos($_POST['MESSAGE'], '!idchange') !== false) {
	$nprocess = true;
	$SETTING['BBS_ID_CHANGE'] = 1;
	$message .="<br><font class=\"add\" color=\"red\">※独自のIDを設定</font> ";
	}
	if (strpos($_POST['MESSAGE'], '!AA') !== false) {
	$nprocess = true;
	$SETTING['BBS_AA'] = 1;
	$message .="<br><font class=\"add\" color=\"red\">※AAスレッド</font> ";
	}
	if (strpos($_POST['MESSAGE'], '!stop') !== false and $number != 1) {
	$nprocess = true;
	 if ($SETTING['THREAD_STOP'] != "yes") {
	 $SETTING['THREAD_STOP'] = "yes";
	 $_POST['MESSAGE'] .="<hr>このスレッドは停止されました。 ";
	 if (!$aa) {
		$_POST[MESSAGE] = trim($_POST[MESSAGE]);
		$_POST[MESSAGE] = ' <span class="AA">'.$_POST[MESSAGE].'</span> ';
	 }
	 $hide = "hide";
	 }
	}
 }
	if (strpos($msgbr[0],"!extend:") !== false) {
	$nprocess = true;
	$extend = explode(":", $msgbr[0]);
	if ($extend[1] == "none") $SETTING['BBS_NO_ID'] = "checked";
	else $SETTING['BBS_NO_ID'] = "none";
	if ($extend[1]) $SETTING['BBS_FORCE_ID'] = $extend[1];
	if ($extend[2] == "default") $SETTING['BBS_SLIP'] = $BSETTING['BBS_SLIP'];
	elseif ($extend[2]) $SETTING['BBS_SLIP'] = $extend[2];
	if ($extend[3]) $SETTING['MAX_RES'] = $extend[3];
	$message .=" <hr>VIPQ2_EXTDAT: ".$extend[1].":".$extend[2].":".$extend[3].":".$extend[4].": EXT was configured ";
	}
	if (strpos($_POST['MESSAGE'], "!save") !== false) {
	 $save = true;
	 if (strpos($_POST['MESSAGE'], "!save:0") !== false) {
		$fp = '';
		foreach($LOG as $tmp) $fp .= $tmp;
		file_put_contents($backup_file, $fp, LOCK_EX);
		DispError2("ＥＲＲＯＲ！","ERROR: バックアップしました");
	 }else $_POST['MESSAGE'] .="<br><small style=\"color: gray;\">バックアップしました</small> ";
	}
 if ($BSETTING['BBS_USE_VIPQ2'] == "checked" or $admin) {
	if ($nusi and strpos($_POST['MESSAGE'], '!sub') !== false) {
	$nprocess = true;
		$subres = preg_replace('/[^0-9]/', '', $_POST['MESSAGE']);
		list(,,,,,,,,,,,,$ui,,$ri,$rfi,$rfm,) = explode("<>",$LOG[$subres-1]);
		if ($SETTING[$ui] != "sub") {
		$SETTING[$ui] = "sub";
		$SETTING[$ri] = "sub";
		$SETTING[$rfi] = "sub";
		$SETTING[$rfm] = "sub";
		$_POST['MESSAGE'] .="<br><span style=\"color: red;\">★副主に追加:&gt;&gt; ".$subres."</span>";
		}else {
		$SETTING[$ui] = "kaijo";
		$SETTING[$ri] = "kaijo";
		$SETTING[$rfi] = "kaijo";
		$SETTING[$rfm] = "kaijo";
		$_POST['MESSAGE'] .="<br><span style=\"color: red;\">★副主を削除:&gt;&gt; ".$subres."</span>";
		}
	}
	if (strpos($_POST['MESSAGE'], '!kaijo') !== false) {
	$nprocess = true;
		$akures = preg_replace('/[^0-9]/', '', $_POST['MESSAGE']);
		list(,,,,,,,,,,,,$ui,,$ri,$rfi,) = explode("<>",$LOG[$akures-1]);
		$SETTING[$ui] = "kaijo";
		$SETTING[$ri] = "kaijo";
		$SETTING[$rfi] = "kaijo";
		$_POST['MESSAGE'] .="<br><span style=\"color: red;\">★解除:&gt;&gt; ".$akures."</span>";
	}
	foreach ($msgar as $tmp) {
		if (preg_match("/!SETTING:/", $tmp, $match)) {
		$nprocess = true;
		$sets = explode(":", $tmp);
		if (strlen($sets[2]) > 100) DispError2("ＥＲＲＯＲ！","ERROR: このコマンドは使用できません。(".strlen($sets[2]).")");
		if (strpos($sets[2], '-') !== false) DispError2("ＥＲＲＯＲ！","ERROR: このコマンドは使用できません。");
		if ($sets[1] == "BBS_PHOEBE" and $sets[2] > 40) DispError2("ＥＲＲＯＲ！","ERROR: このコマンドは使用できません。");
		$set = $sets[1];
		$SETTING[$set] = $sets[2];
		$message .="<br><span style=\"color: red;\">$set=$sets[2]</span> ";
		}
	}
	if (strpos($_POST['MESSAGE'], '!reset') !== false) {
		$nprocess = true;
		#設定ファイル再読込
		$SETTING = $BSETTING;
		$_POST['MESSAGE'] .="<br><span style=\"color: red;\">★スレッドの設定をリセット</span> ";
	}
 }
}
#################################################################################
# 全体規制
#############################################################################
@include $BBQSERV.'proxy999.cgi';
#################################################################################
# 板別規制
#################################################################################
$madakana = '';
if (is_file($PATH.'madakana.cgi')) {
	$aku_str = file($PATH."madakana.cgi");
	foreach ($aku_str as $tmp){
		$tmp = trim($tmp);
		if (!$tmp or strpos($tmp, '#') !== false) continue;
		list($kisei,$kt,$rw) = explode("<>", $tmp);
		if (strpos($kisei, '&') !== false) {
		list($ks,$ks1) = explode("&", $kisei);
		if (strpos($ks, '/') === false) $ks = "/".$ks."/";
		if (strpos($ks1, '/') === false) $ks1 = "/".$ks1."/";
		 if (preg_match($ks, $_SERVER[REMOTE_ADDR]) or preg_match($ks, $SID) or preg_match($ks, $HOST) or preg_match($ks, $UA) or preg_match($ks, $terminal." ".$USER_AGENT) or preg_match($ks, $phone) or preg_match($ks, $area["regionName"]) or preg_match($ks, $area["city"]) or preg_match($ks, $area["asname"])) {
			if (preg_match($ks1, $_SERVER[REMOTE_ADDR]) or preg_match($ks1, $SID) or preg_match($ks1, $HOST) or preg_match($ks1, $UA) or preg_match($ks1, $terminal." ".$USER_AGENT) or preg_match($ks1, $phone) or preg_match($ks1, $area["regionName"]) or preg_match($ks1, $area["city"]) or preg_match($ks1, $area["asname"])) {
				if ($kt) {
				if (strpos($kt, '/') === false) $kt = "/".$kt."/";
				if (preg_match($kt, $subject)) $madakana = "ERROR: あなたはこのスレッドには投稿することができません。※詳しくは板管理者にお問い合わせください。";
				}else $madakana = "ERROR: あなたはこの掲示板には投稿することができません。※詳しくは板管理者にお問い合わせください。";
			}
		 }
		}else {
		 if (strpos($kisei, '/') === false) $kisei = "/".$kisei."/";
		 if (preg_match($kisei, $_SERVER[REMOTE_ADDR]) or preg_match($kisei, $SID) or preg_match($kisei, $HOST) or preg_match($kisei, $UA) or preg_match($kisei, $terminal." ".$USER_AGENT) or preg_match($kisei, $phone) or preg_match($kisei, $area["regionName"]) or preg_match($kisei, $area["city"]) or preg_match($kisei, $area["asname"])) {
			if ($kt) {
			if (strpos($kt, '/') === false) $kt = "/".$kt."/";
			if (preg_match($kt, $subject)) $madakana = "ERROR: あなたはこのスレッドには投稿することができません。※詳しくは板管理者にお問い合わせください。";
			}else $madakana = "ERROR: あなたはこの掲示板には投稿することができません。※詳しくは板管理者にお問い合わせください。";
		 }
		}
		if ($rw and $madakana) {
		 if (strpos($rw, '/') === false) $rw = "/".$rw."/";
		 if (!preg_match($rw, $_POST['MESSAGE'].$_POST['subject'].$_POST['FROM'].$_POST['mail'])) $madakana = '';
		 elseif ($SETTING['BBS_NO_MADAKANA'] != "on") DispError("ＥＲＲＯＲ！","ERROR: 範囲ごとのNGワードです。※詳しくは板管理者にお問い合わせください。","9990 Banned;");
		 else {
			$madakana = '';
			$_POST['MESSAGE'] .= '<br><small style="color: #F66;">(NGワード)</small>';
		 }
		}
		if ($madakana) {
		if ($SETTING['BBS_NO_MADAKANA'] != "on") DispError("ＥＲＲＯＲ！",$madakana,"9990 Banned...;");
		elseif (strpos($_POST['FROM'], '</b>[´･ω･｀] <b>') === false) $_POST['FROM'] .= " </b>[´･ω･｀] <b>fusianasan";
		}
	}
}
#################################################################################
# Rock54（板別）
#################################################################################
if (is_file($PATH.'rock54.cgi')) {
	$rock_str = file($PATH."rock54.cgi");
	$P = $_POST['MESSAGE'].$_POST['subject'].$_POST['FROM'].$_POST['mail'];
		foreach ($rock_str as $tmp){
		$tmp = trim($tmp);
		if (!$tmp or strpos($tmp, '#') !== false) continue;
		if (strpos($tmp, '/') === false) $tmp = "/".$tmp."/";
		if (preg_match($tmp, $P)) DispError("ＥＲＲＯＲ！","ERROR: 板全体のNGワードです。(BBR-MD5:".md5($tmp).")<br>NGワードに関する問い合わせは各板の管理者へどうぞ。");
		}
}
#############################################################################
# Rock54（全体）
#############################################################################
if (!$login) @include $BBQSERV.'rock54.cgi';
#############################################################################
# PHOEBE での規制
#############################################################################
if (!$dame and $slip == "0" and $_SERVER[HTTP_CF_IPCOUNTRY] == "JP") $LV = 40;
if ($SETTING['BBS_PHOEBE'] != "none" and $LV < $SETTING['BBS_PHOEBE']) {
 if ($_POST['subject'] or (!$nusi and !$subnusi)) DispError("ＥＲＲＯＲ！","ERROR: この板・スレッドはLv".$SETTING[BBS_PHOEBE]."以上でないと投稿お断り中です。(you=".$LV.")");
}
#############################################################################
# 各種制限に使用する値を生成
#############################################################################
if ($BSETTING['RESET_POSTCOUNT'] == "year") $resett = date("Y");
elseif ($BSETTING['RESET_POSTCOUNT'] == "month") $resett = date("Ym");
elseif ($BSETTING['RESET_POSTCOUNT'] == "10days") $resett = date("Ym").substr(date("d"), 0, 1);
elseif ($BSETTING['RESET_POSTCOUNT'] == "10hours") $resett = date("Ymd").substr(date("H"), 0, 1);
elseif ($BSETTING['RESET_POSTCOUNT'] == "hour") $resett = date("YmdH");
elseif ($BSETTING['RESET_POSTCOUNT'] == "10minutes") $resett = date("YmdH");
elseif ($BSETTING['RESET_POSTCOUNT'] == "minute") $resett = date("YmdHi");
else $resett = date("Ymd");
$h_isp = substr(hash('sha256', $area["asname"].$area['mobile'].$resett), 0, 12);
$h_range = substr(hash('sha256', $range.$resett), 0, 12);
$h_id = substr(hash('sha256', $area["regionName"].$area["asname"].$area['mobile'].$resett), 0, 12);
$h_ua = substr(hash('sha256', $terminal.$resett), 0, 12);
$h_ip = substr(hash('sha256', $_SERVER[REMOTE_ADDR].$resett), 0, 12);
$h_sip = substr(hash('sha256', $_SESSION[REMOTE_ADDR].$resett), 0, 12);
$h_rid = substr(hash('sha256', $rid.$resett), 0, 12);
$h_browser = substr(hash('sha256', $_SERVER[HTTP_USER_AGENT].$resett), 0, 12);
$h_ken = substr(hash('sha256', $area["regionName"].$resett), 0, 12);
$h_area = substr(hash('sha256', $area["regionName"].$area["city"].$resett), 0, 12);
$h_accept = substr(hash('sha256', $USER_AGENT.$resett), 0, 12);
#10日毎
$c_isp = substr(hash('sha256', $area["asname"].$area['mobile'].$SLIP_SERV), 0, 12);
$c_range = substr(hash('sha256', $range.$SLIP_SERV), 0, 12);
$c_id = substr(hash('sha256', $area["regionName"].$area["asname"].$area['mobile'].$SLIP_SERV), 0, 12);
$c_ua = substr(hash('sha256', $terminal.$SLIP_SERV), 0, 12);
$c_ip = substr(hash('sha256', $_SERVER[REMOTE_ADDR].$SLIP_SERV), 0, 12);
$c_sip = substr(hash('sha256', $_SESSION[REMOTE_ADDR].$SLIP_SERV), 0, 12);
$c_rid = substr(hash('sha256', $rid.$SLIP_SERV), 0, 12);
$c_browser = substr(hash('sha256', $_SERVER[HTTP_USER_AGENT].$SLIP_SERV), 0, 12);
$c_ken = substr(hash('sha256', $area["regionName"].$SLIP_SERV), 0, 12);
$c_area = substr(hash('sha256', $area["regionName"].$area["city"].$SLIP_SERV), 0, 12);
$c_accept = substr(hash('sha256', $USER_AGENT.$SLIP_SERV), 0, 12);
#######################################################################
# 短時間連投規制
#######################################################################
if ($BSETTING['BBS_FR_LEVEL'] != "off") {
if ($SETTING['LIVE_THREAD'] or $BSETTING['BBS_FR_SECOND'] == "off") $samba24 = 5;
elseif (!$BSETTING['BBS_FR_SECOND']) $samba24 = 15;
else $samba24 = $BSETTING['BBS_FR_SECOND'];
if ($samba24 < 5) $samba24 = 5;
		#データ取得
		if (filemtime($kirokufile) > $_SESSION['posttime']) $posttime = filemtime($kirokufile);
		else $posttime = $_SESSION['posttime'];
if (is_file($BBSSERV."/".date('z')."/samba24_".$file_ipaddr.".cgi")) {
	if ($NOWTIME < filemtime($BBSSERV."/".date('z')."/samba24_".$file_ipaddr.".cgi") + $samba24) $sambac = @file_get_contents($BBSSERV."/".date('z')."/samba24_".$file_ipaddr.".cgi");
	else @unlink($BBSSERV."/".date('z')."/samba24_".$file_ipaddr.".cgi");
}
				if (!$sambac) $sambac = 0;
				$samba = $posttime + $samba24;
				if ($NOWTIME < $samba) {
					++$sambac;
					@file_put_contents($BBSSERV."/".date('z')."/samba24_".$file_ipaddr.".cgi", $sambac);
					if ($sambac > 4) {
					if ($BBX == "NONE") Burned("FlyRibbon:0011");
					DispError("ＥＲＲＯＲ！","ERROR: 5回連続して短時間連投規制を受けたため日付が変わるまで投稿できません。 ".$samba24);
					}elseif ($sambac > 1) DispError("ＥＲＲＯＲ！","ERROR: 短時間連投規制に引っ掛かりました。しばらくお待ちください。残り ".$samba24." 秒");
				}
}
#==================================================
#　連続投稿規制
#==================================================
if ($BSETTING['timecount'] >= 1) {
	# 投稿者のホスト名記録ファイルを読み込む（timecount個記録されている）
	$file = $PATH."timecheck.cgi";
	$IP = array();
	$count = 0;
	$sinkc = 0;
	if (!is_file($file)) @touch($file);
	if (is_file($file)) {
		$IP = file($file);
		foreach($IP as $tmp){
			$tmp = rtrim($tmp);
			list(,$pip,$psip,,$parea,$pua,$prid,$pid,$prange,$pbrowser,$pken,$paccept,$pisp) = explode("<>", $tmp);
			if ($h_ip == $pip or $h_ip == $psip or $h_sip == $pip or $h_sip == $psip) $pipc++;
			if ($h_area == $parea or $h_id == $pid) $pareac++;
			if ($h_ua == $pua) $puac++;
			if ($h_rid == $prid) $pridc++;
			if ($h_range == $prange) $prangec++;
			if ($h_browser == $pbrowser) $pbc++;
			if ($h_ken == $pken) $pkc++;
			if ($h_accept == $paccept) $pac++;
		}
	$maxclosea = $BSETTING['timecount'] / 2;
	$maxclosec = $BSETTING['timecount'] / 1.5;
	$maxcloseb = $BSETTING['timecount'] / 1.2;
	if ($pipc > $BSETTING['timeclose'] and $BSETTING['BBS_FR_LEVEL'] > 0) {
		DispError("ＥＲＲＯＲ！","ERROR: この掲示板で一定時間内に投稿可能な上限に達しました。※板毎連続投稿規制の値に関する問い合わせは各板の管理者へどうぞ。");
	}
	if ($BSETTING['timecount'] >= 8 and !$SETTING['LIVE_THREAD'] and !$login and $BSETTING['BBS_FR_LEVEL'] > 2) {
	 if ($pridc > $maxclosea or $pareac > $maxclosea or $pkc > $maxclosec or $prangec > $maxclosec) DispError("ＥＲＲＯＲ！","ERROR: この掲示板での広域規制の対象となっています。しばらくお待ちください。※ログインするとすぐに書き込めます。 1");
	 if ($puac > $maxclosea or $pbc > $maxcloseb or $pac > $maxcloseb) DispError("ＥＲＲＯＲ！","ERROR: この掲示板での広域規制の対象となっています。しばらくお待ちください。※ログインするとすぐに書き込めます。 2");
	}
	array_unshift($IP, "$PHOEBELV<>$h_ip<>$h_sip<><>$h_area<>$h_ua<>$h_rid<>$h_id<>$h_range<>$h_browser<>$h_ken<>$h_accept<>\n");
	# 記録ファイル内のホスト数を timecount 個以内に調整して保存
	while (count($IP) > $BSETTING['timecount']) array_pop($IP);
	$fp = @fopen($file, "w");
	foreach($IP as $tmp) fputs($fp, $tmp);
	fclose($fp);
	}
}
#############################################################################
# 各種スレ立てチェックをまとめて行う
#############################################################################
if ($_POST['subject']) {
	# 同時刻のスレ立ては弾く
	if (is_file($thread_file)) DispError2("ＥＲＲＯＲ！","ERROR: 別の人が同時刻にスレッドを立てようとしています。再度お試しください。");
 # 板別規制
 $deny = '';
 if (is_file($PATH.'denylist.cgi')) {
	$deny_str = file($PATH."denylist.cgi");
	foreach ($deny_str as $tmp){
		$tmp = trim($tmp);
		if (!$tmp or strpos($tmp, '#') !== false) continue;
		list($kisei,$rw) = explode("<>", $tmp);
		if (strpos($kisei, '&') !== false) {
		list($ks,$ks1) = explode("&", $kisei);
		if (strpos($ks, '/') === false) $ks = "/".$ks."/";
		if (strpos($ks1, '/') === false) $ks1 = "/".$ks1."/";
		 if (preg_match($ks, $_SERVER[REMOTE_ADDR]) or preg_match($ks, $SID) or preg_match($ks, $HOST) or preg_match($ks, $UA) or preg_match($ks, $terminal." ".$USER_AGENT) or preg_match($ks, $phone) or preg_match($ks, $area["regionName"]) or preg_match($ks, $area["city"]) or preg_match($ks, $area["asname"])) {
			if (preg_match($ks1, $_SERVER[REMOTE_ADDR]) or preg_match($ks1, $SID) or preg_match($ks1, $HOST) or preg_match($ks1, $UA) or preg_match($ks1, $terminal." ".$USER_AGENT) or preg_match($ks1, $phone) or preg_match($ks1, $area["regionName"]) or preg_match($ks1, $area["city"]) or preg_match($ks1, $area["asname"])) $deny = "ERROR: あなたはこの掲示板でスレッドを作成することができません。※詳しくは板管理者にお問い合わせください。";
		 }
		}else {
		 if (strpos($kisei, '/') === false) $kisei = "/".$kisei."/";
		 if (preg_match($kisei, $_SERVER[REMOTE_ADDR]) or preg_match($kisei, $SID) or preg_match($kisei, $HOST) or preg_match($kisei, $UA) or preg_match($kisei, $terminal." ".$USER_AGENT) or preg_match($kisei, $phone) or preg_match($kisei, $area["regionName"]) or preg_match($kisei, $area["city"]) or preg_match($kisei, $area["asname"])) $deny = "ERROR: あなたはこの掲示板でスレッドを作成することができません。※詳しくは板管理者にお問い合わせください。";
		}
		if ($rw and $deny) {
		 if (strpos($rw, '/') === false) $rw = "/".$rw."/";
		 if (!preg_match($rw, $_POST['MESSAGE'].$_POST['subject'].$_POST['FROM'].$_POST['mail'])) $deny = '';
		 else DispError("ＥＲＲＯＲ！","ERROR: スレッド作成時のNGワードです。※詳しくは板管理者にお問い合わせください。","9990 Banned;");
		}
		if ($deny) DispError("ＥＲＲＯＲ！",$deny,"5998 Unavailable New thread;");
	}
 }
 if (!$login) {
#--------------未ログイン時の処理 ここから-------
	if ($SETTING['THREAD_CHECK'] == "checked") DispError("ＥＲＲＯＲ！","ERROR: この掲示板はログインユーザーのみスレッドを作成できます。","G7002 Required login;");
	# TAKO=ODORI
	if ($_COOKIE[TAKO] == "ODORI") DispError("ＥＲＲＯＲ！","ERROR: あなたはスパムであると判定されたためスレッドを作成することができません。&#128025; OctpusCount:8");
	# 串＆hosting＆逆引きなし＆公衆Wi-Fiはスレ立て不可
	if ($slip == "8" or $slip == "h" or $slip == "H" or $slip == "F") DispError("ＥＲＲＯＲ！","ERROR: Sorry このホストではスレッドを作成することができません。 CODE:1001","5503 Unavailable New thread;");

#--------------未ログイン時の処理 ここまで-------
 }
	# 同一スレ乱立防止
  if ($SETTING['BBS_DUPLICATE'] != "off") {
	 if (!$SETTING['BBS_DUPLICATE']) $SETTING['BBS_DUPLICATE'] = 86400;
	 $threadss = @file($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/subject.txt");
	 if ($threadss) {
		foreach ($threadss as $tmp){
		list($sk1,$subje,$ti,$tm) = explode("<>", $tmp);
		if ($subje == $_POST['subject'] and $sk1 - $_POST['key'] < $SETTING['BBS_DUPLICATE']) DispError("ＥＲＲＯＲ！","ERROR: すでに同じタイトルのスレッドが存在しています。スレッド一覧でお確かめください。");
		if (strlen($ti) > 7 and strpos($ti, $ID) !== false) $ic++;
		if (strlen($_POST['MESSAGE']) > 512 and $tm == $_POST['MESSAGE'] and !$login) DispError("ＥＲＲＯＲ！","ERROR: スパムであると判定されたためスレッドの作成を拒否されました。本文を変えて再度お試しください。 CODE:3","5503 Unavailable New thread;");
		}
	 }
  }
	if ($ic > 5 and strlen($ID) > 7) DispError("ＥＲＲＯＲ！","ERROR: 日付が変わるまであなたはスレッドを作成できません。 CODE:2","5502 Unavailable New thread;");

  if ($BSETTING['BBS_THREAD_TATESUGI'] >= 1) {
	# スレ立て者の記録ファイルを読み込む（BBS_THREAD_TATESUGI個記録されている）
	$file = $PATH."RIP.cgi";
	$IP = array();
	if (is_file($file)) {
	 if ($NOWTIME < filemtime($file) + $BSETTING['THREAD_INTERVAL']) DispError("ＥＲＲＯＲ！","ERROR: Sorry この掲示板は直前のスレッド作成から".$BSETTING[THREAD_INTERVAL]."秒経たなければスレッドを作成することが出来ません。","5550 Unavailable New thread;");
		$IP = file($file);
		foreach ($IP as $tmp) {
			$tmp = rtrim($tmp);
			list($tid,$tarea,$tip,$tsip,,$tua,$trange,) = explode("<>", $tmp);
			if ($c_id == $tid or $c_area == $tarea or $trange == $c_range) $maked = true;
			if ($c_ip == $tip or $c_ip == $tsip or $c_sip == $tip or $c_sip == $tsip) $imake = true;
			if ($c_ua == $tua) $umake++;
		}
	}else touch($file);
	if (!$login) {
	$TATESUGI = $BSETTING['BBS_THREAD_TATESUGI'] / 3;
	if ($BSETTING['makethread_rangecheck'] == "checked" and $maked) DispError("ＥＲＲＯＲ！","ERROR: Sorry あなたと同じIPアドレスグループから直近のスレッド作成があったため拒否されました。※ログインするとすぐに作成できます。","5500 Unavailable New thread;");
	if ($imake) DispError("ＥＲＲＯＲ！","ERROR: Sorry スレッドを連続して作成することはできません。※ログインするとすぐに作成できます。 CODE:1","5502 Unavailable New thread;");
	if ($BSETTING['makethread_rangecheck'] == "checked" and $umake > $TATESUGI) DispError("ＥＲＲＯＲ！","ERROR: Sorry あなたと同じ端末・ブラウザから連続してスレッド作成があったため拒否されました。※ログインするとすぐに作成できます。 CODE:10","5510 Unavailable New thread;");
	}
	array_unshift($IP, "$c_id<>$c_area<>$c_ip<>$c_sip<><>$c_ua<>$c_range<>\n");
	# 記録ファイル内のホスト数を BBS_THREAD_TATESUGI 個以内に調整して保存
	while (count($IP) > $BSETTING['BBS_THREAD_TATESUGI']) array_pop($IP);
	$fp = @fopen($file, "w");
	foreach($IP as $tmp) fputs($fp, "$tmp");
	fclose($fp);
  }elseif ($BSETTING['THREAD_INTERVAL']) {
  	$file = $PATH."RIP.cgi";
	if (is_file($file) and $NOWTIME < filemtime($file) + $BSETTING['THREAD_INTERVAL']) DispError("ＥＲＲＯＲ！","ERROR: Sorry この掲示板は直前のスレッド作成から".$BSETTING[THREAD_INTERVAL]."秒経たなければスレッドを作成することが出来ません。","5550 Unavailable New thread;");
	touch($file);
  }
  if ($BSETTING['THREAD_JUNBAN'] >= 1) {
	# スレ立て者の記録ファイルを読み込む（THREAD_JUNBAN個記録されている）
	$file = $PATH."JUNBAN.cgi";
	$IP = array();
	if (!is_file($file)) touch($file);
	if (is_file($file)) {
		$IP = file($file);
		foreach ($IP as $tmp) {
			$tmp = rtrim($tmp);
			list($tpl,$tisp,$trid,$tbrowser,$tken,$taccept,) = explode("<>", $tmp);
			if ($tpl < $stime) $tsink++;
			if ($c_isp == $tisp) $tispc++;
			if ($c_rid == $trid) $tridc++; 
			if ($c_range == $trange) $trc++;
			if ($c_browser == $tbrowser) $tbc++;
			if ($c_ken == $tken) $tkc++;
			if ($c_accept == $taccept) $tac++;
		}
	}
	$JUNBAN = $BSETTING['THREAD_JUNBAN'] / 1.5;
	if ($PHOEBELV < $stime and !$login) {
	 if ($tsink > $JUNBAN) DispError("ＥＲＲＯＲ！","ERROR: 新規ユーザーから大量のスレッド作成があったため拒否されました。※ログインすると作成できます。 SinkiCount:".$tsink,"5530 Unavailable New thread;");
	 if ($tispc > $JUNBAN or $trc > $JUNBAN or $tridc > $JUNBAN or $tkc > $JUNBAN or $tbc > $JUNBAN or $tac > $JUNBAN) DispError("ＥＲＲＯＲ！","ERROR: 広域スレッド作成規制中です。しばらくお待ちください。※ログインするとすぐに作成できます。 CODE:".$tispc.$trc.$tridc.$tkc.$tbc.$tac,"5520 Unavailable New thread;");
	}
	array_unshift($IP, "$PHOEBELV<>$c_isp<>$c_rid<>$c_browser<>$c_ken<>$c_accept<>\n");
	# 記録ファイル内のホスト数を THREAD_JUNBAN 個以内に調整して保存
	while (count($IP) > $BSETTING['THREAD_JUNBAN']) array_pop($IP);
	$fp = @fopen($file, "w");
	foreach($IP as $tmp) fputs($fp, "$tmp");
	fclose($fp);
  }
}
#############################################################################
# 各種書込制限
#############################################################################
#----------------------------------------------sid基準

# マルチポスト対策
similar_text($_SESSION['one_msg'], $_POST['MESSAGE'], $percone);
similar_text($_SESSION['two_msg'], $_POST['MESSAGE'], $perctwo);
	if ($percone >= 95 and $perctwo >= 95 and $BSETTING['BBS_FR_LEVEL'] > 1) {
	DispError("ＥＲＲＯＲ！","ERROR: 同一・類似した投稿を連続して行わないでください。");
	}

	#過去2回分の投稿内容を記録
	$_SESSION['two_msg'] = $_SESSION['one_msg'];
	$_SESSION['one_msg'] = $_POST['MESSAGE'];

# 投稿量制限（1時間）
if (!$_SESSION['CPTIME']) $_SESSION['CPTIME'] = $NOWTIME;
$CPWHILE = $_SESSION['CPTIME'] + 3600;
if ($NOWTIME < $CPWHILE) {
++$_SESSION['CPCOUNT'];
#50回以上の書込数
if ($_SESSION['CPCOUNT'] > 50 and $BSETTING['BBS_FR_LEVEL'] > 0) {
	DispError("ＥＲＲＯＲ！","ERROR: 1時間に50回以上投稿を行ったため一時的に制限されています。");
}
	
}else {
	$_SESSION['CPTIME'] = '';
	$_SESSION['CPCOUNT'] = 0; 
}

#----------------------------------------------IP基準
$ip_temp = $BBSSERV."/".date('z')."/temp_".$file_ipaddr.".cgi";
if (is_file($ip_temp)) $ipdata = unserialize(file_get_contents($ip_temp));
else $ipdata = array();

# マルチポスト対策
similar_text($ipdata['one_msg'], $_POST['MESSAGE'], $percone);
similar_text($ipdata['two_msg'], $_POST['MESSAGE'], $perctwo);
	if ($percone >= 95 and $perctwo >= 95 and $BSETTING['BBS_FR_LEVEL'] > 1) {
	DispError("ＥＲＲＯＲ！","ERROR: 同一・類似した投稿を連続して行わないでください。");
	}

	#過去2回分の投稿内容を記録
	$ipdata['two_msg'] = $ipdata['one_msg'];
	$ipdata['one_msg'] = $_POST['MESSAGE'];

# 投稿量制限（1時間）
if (!$ipdata['CPTIME']) $ipdata['CPTIME'] = $NOWTIME;
$CPWHILE = $ipdata['CPTIME'] + 3600;
if ($NOWTIME < $CPWHILE) {
++$ipdata['CPCOUNT'];
#50回以上の書込数
if ($ipdata['CPCOUNT'] > 50 and $BSETTING['BBS_FR_LEVEL'] > 0) {
	DispError("ＥＲＲＯＲ！","ERROR: 1時間に50回以上投稿を行ったため一時的に制限されています。");
}
	
}else {
	$ipdata['CPTIME'] = '';
	$ipdata['CPCOUNT'] = 0;
}

file_put_contents($ip_temp, serialize($ipdata));

#----------------------------------------------rid基準
$rip_temp = $BBSSERV."/".date('z')."/temp_".$rid.".cgi";
if (is_file($rip_temp)) $riddata = unserialize(file_get_contents($rip_temp));
else $riddata = array();

# マルチポスト対策
similar_text($riddata['one_msg'], $_POST['MESSAGE'], $percone);
similar_text($riddata['two_msg'], $_POST['MESSAGE'], $perctwo);
	if ($percone >= 95 and $perctwo >= 95 and !$login and $BSETTING['BBS_FR_LEVEL'] > 1) {
	DispError("ＥＲＲＯＲ！","ERROR: 同一・類似した投稿を連続して行わないでください。");
	}

	#過去2回分の投稿内容を記録
	$riddata['two_msg'] = $riddata['one_msg'];
	$riddata['one_msg'] = $_POST['MESSAGE'];

# 投稿量制限（5分間）
if (!$riddata['CPTIME']) $riddata['CPTIME'] = $NOWTIME;
$CPWHILE = $riddata['CPTIME'] + 300;
if ($NOWTIME < $CPWHILE) {
$riddata['CPBYTE'] += strlen($_POST['MESSAGE']);
++$riddata['CPCOUNT'];
#5分間に51回以上の書込数
if ($riddata['CPCOUNT'] > 50 and !$login) {
	DispError("ＥＲＲＯＲ！","ERROR: しばらくお断りしております。[".$_POST['bbs']."]","9990 Banned;");
}

#5分間に40960B以上の投稿数
if ($riddata['CPBYTE'] >= 40960 and !$login) {
	DispError("ＥＲＲＯＲ！","ERROR: しばらくお断りしております。[".$_POST['bbs']."]","9990 Banned;");
}
	
}else {
	$riddata['CPTIME'] = '';
	$riddata['CPBYTE'] = strlen($_POST['MESSAGE']);
	$riddata['CPCOUNT'] = 0;
}

file_put_contents($rip_temp, serialize($riddata));
if ($login) {
$kpath = $BBSSERV."/".date('z')."/g_".$_COOKIE[secretkey].".cgi";
if (is_file($kpath)) $gdata = unserialize(file_get_contents($kpath));
else $gdata = array();

# マルチポスト対策
similar_text($gdata['one_msg'], $_POST['MESSAGE'], $percone);
similar_text($gdata['two_msg'], $_POST['MESSAGE'], $perctwo);
	if ($percone >= 95 and $perctwo >= 95 and $BSETTING['BBS_FR_LEVEL'] > 1) {
	DispError("ＥＲＲＯＲ！","ERROR: 同一・類似した投稿を連続して行わないでください。");
	}

	#過去2回分の投稿内容を記録
	$gdata['two_msg'] = $gdata['one_msg'];
	$gdata['one_msg'] = $_POST['MESSAGE'];

# 投稿量制限（1時間）
if (!$gdata['CPTIME']) $gdata['CPTIME'] = $NOWTIME;
$CPWHILE = $gdata['CPTIME'] + 3600;
if ($NOWTIME < $CPWHILE) {
$gdata['CPBYTE'] += strlen($_POST['MESSAGE']);
++$gdata['CPCOUNT'];
#50回以上の書込数
if ($gdata['CPCOUNT'] > 50 and $BSETTING['BBS_FR_LEVEL'] > 0) {
	DispError("ＥＲＲＯＲ！","ERROR: 1時間に50回以上投稿を行ったため一時的に制限されています。");
}

#100000B以上の投稿数
if ($gdata['CPBYTE'] >= 100000) {
	if ($BBX == "NONE") Burned("短時間に大量の投稿を行ったため制限されました。");
	DispError("ＥＲＲＯＲ！","ERROR: 短時間に大量の投稿を行ったため制限されました。日付が変わるまでお待ちください。","8901 Rejected;");
}
	
}else {
	$gdata['CPTIME'] = '';
	$gdata['CPBYTE'] = strlen($_POST['MESSAGE']);
	$gdata['CPCOUNT'] = 0;
}

if ($_POST['subject']) {
	if ($gdata['MAKETIME'] > $NOWTIME - 600) DispError("ＥＲＲＯＲ！","ERROR: 10分以内に連続してスレッドを作成することはできません。10分後に再度お試しください。","5590 Unavailable New thread;");
	# スレッド作成制限（1時間）
	if (!$gdata['TTIME']) $gdata['TTIME'] = $NOWTIME;
	$TWHILE = $gdata['TTIME'] + 3600;
	if ($NOWTIME < $TWHILE) {
	 #1時間に2個以上のスレ立て数
	 if ($gdata['TCOUNT'] > 1) {
		DispError("ＥＲＲＯＲ！","ERROR: 1時間にスレッドを作成できる上限に達しました。1時間後に再度お試しください。","5591 Unavailable New thread;");
	 }
	 #1時間内のスレ立て数をカウント
	 ++$gdata['TCOUNT'];
	}else {
		$gdata['TCOUNT'] = 0;
	}
	$gdata['MAKETIME'] = $NOWTIME;
}

file_put_contents($kpath, serialize($gdata));
}
#############################################################################
#	マルチポスト規制
#############################################################################
if ($BSETTING['BBS_FR_LEVEL'] > 1) {
$MD5 = array();
#----------------------------------------------本文全体
$CMSG = str_replace(" ", "", $_POST['MESSAGE']);
$CMSG = str_replace("　", "", $CMSG);
$CMSG = str_replace("<br>", "", $CMSG);
$CMSG = preg_replace('/[\.,、。]/','',$CMSG);
$CMSG = preg_replace('/&gt;&gt;([0-9]+)(?![-\d])/','$2',$CMSG);
$MSGMD5 = md5($CMSG);
array_push($MD5,$MSGMD5);
#----------------------------------------------行毎
foreach ($msgbr as $tmp) {
$tmp = str_replace(" ", "", $tmp);
$tmp = str_replace("　", "", $tmp);
$tmp = preg_replace('/[\.,、。]/','',$tmp);
$tmp = preg_replace('/&gt;&gt;([0-9]+)(?![-\d])/','$2',$tmp);
if (!$tmp) continue;
$BRMD5 = md5($tmp);
array_push($MD5,$BRMD5);
}
#----------------------------------------------URL
$_POST['MESSAGE'] = preg_replace_callback('/h?ttps?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
	global $MD5;
	$URLMD5 = md5($m[1]);
	array_push($MD5,$URLMD5);
  	      return $m[0];
	}, $_POST['MESSAGE']);
#----------------------------------------------BBR-MD5
 if ($SETTING['LIVE_THREAD'] or $login) $CPTIME = 64;
 else $CPTIME = 512;
 $ORIG = 'https://'.$_SERVER[HTTP_HOST].'/test/read.cgi/'.$_POST[bbs].'/'.$_POST[key].'/'.$number;
 foreach($MD5 as $tmp) {
	if (!$tmp) continue;
	# 板毎のMD5を比較
	$MLOG = file($BBSSERV."/tmp/".$_POST['bbs'].date('z')."/bbrmd5.txt");
	krsort($MLOG);
	foreach($MLOG as $tmps){
	 if (!$tmps) continue;
	 trim($tmps);
	 list($BBRMD5,$MTIME,$orig,) = explode("<>",$tmps);
	 if (!$md5pass and $NOWTIME - $MTIME > $CPTIME) break;
	 if ($BBRMD5 == $tmp) {
		$CTIME = $NOWTIME - $MTIME;
		$COPIPE = $CPTIME - $CTIME;
		if ($COPIPE > 0) DispError("ＥＲＲＯＲ！","ERROR: マルチポスト・コピペを検出しました。".$COPIPE."秒後に再度お試しください。");
		else break;
	 }
	}
 }
 # MD5ハッシュを記録
 foreach($MD5 as $tmp) {
	$fp = fopen($BBSSERV."/tmp/".$_POST['bbs'].date('z')."/bbrmd5.txt", "a");
	fputs($fp, "$tmp<>$NOWTIME<>$ORIG<>\n");
	fclose($fp);
 }
}
#####################################################
#　各種機能＆コマンド関連
#####################################################
# 新方式ID
if ($SETTING['BBS_SLIP'] and $SETTING['BBS_SLIP'] != "none" and $SETTING['BBS_SLIP'] != "checked") {
 if ($slip != "0" or $SETTING['BBS_SLIP'] == "verbose") {
	$ID = "ID:".$SLIP;
	$newid = true;
 }
}
# 短縮ID
if ($SETTING['BBS_SLIP'] == "short") $ID = substr($ID, 0, 5);

# IDを非表示
if ($SETTING['BBS_NO_ID'] == "checked" and strpos($_POST['mail'],'!id:on') === false) $ID = '';
$_POST['mail'] = str_replace("!id:on", "", $_POST['mail']);

# SLIP_NAME
if ($mobile) {
 if ($slip == "0" or $slip == "H" or $slip == "8" or $slip == "h" or $slip == "F") $SLIP_NAME .= "W";
}

$no = 0;
if ($SETTING['BBS_DISABLE_NUSI'] == "checked") $no = 1;
if (strpos($_POST['mail'],'!no') !== false and $SETTING['BBS_DISABLE_NO'] != "checked") $no = 1;
$_POST['mail'] = str_replace("!no", "", $_POST['mail']);

# ID強制表示じゃない場合でmail欄に記入があればIDを隠す
if ($_POST['mail'] and $SETTING['BBS_FORCE_ID'] != "checked" and $_POST['mail'] != "sage" and $_POST['mail'] != "soko") $ID = 'ID:???';
# キャップのID
if ($admin) {
$ID = 'ID:'.$CAPID;
$slip = '';
$SLIP_AREA = '';
}
# キャップの色
if ($ncolor) $_POST['FROM'] = "<font color=\"$ncolor\">".$_POST['FROM']."</font>";
# 924スレッド
if (substr($_POST['key'], 0, 3) == 924 and !$admin) DispError("ＥＲＲＯＲ！","ERROR: 924スレッドには書き込めません。");
# 名前入力チェックと補完
if (!$_POST['FROM']) {
 if ($SETTING['NANASHI_CHECK'] || $BSETTING['NANASHI_CHECK']) DispError("ＥＲＲＯＲ！","ERROR: この掲示板は名前の記入が必須です。");
}
# 焼き印
if ($_COOKIE[TAKO] == "ODORI") $_POST['FROM'] .= "</b><span>&#128025;</span><b>";
if ($BBX != "NONE") $_POST['FROM'] .= "</b><span>&#128123;</span><b>";
elseif ($BBM != "NONE") $_POST['FROM'] .= "</b><span>&#128245;</span><b>";

# 県名表示
if ($SETTING['BBS_JP_CHECK'] and $SETTING['BBS_JP_CHECK'] != "none" and !$admin) $_POST['FROM'] .= "</b>(".$ken.")<b>";
# BBS_SLIP
if ($SETTING['BBS_SLIP'] == "vvvvvv" and !$admin) {
 $_POST['FROM'] .= " </b>(".$SLIP_NAME." ".$SLIP_IP.$SLIP_ID."-".$SLIP_TE.$SLIP_AC." [".$REMOTEADDR."])<b>";
}elseif ($SETTING['BBS_SLIP'] == "vvvvv" and !$admin) {
 $_POST['FROM'] .= " </b>(".$SLIP_NAME." ".$SLIP_IP.$SLIP_ID."-".$SLIP_TE.$SLIP_AC.")<b>";
}elseif ($SETTING['BBS_SLIP'] == "vvvv" and !$admin) {
 $_POST['FROM'] .= " </b>(".$SLIP_NAME." ".$REMOTEADDR.")<b>";
}elseif ($SETTING['BBS_SLIP'] == "vvv" and !$admin) {
 $_POST['FROM'] .= " </b>(".$SLIP_NAME.")<b>";
}

# ID末尾
if ($SETTING['BBS_SLIP'] and $SETTING['BBS_SLIP'] != "none" and !$newid and !$admin) {
	if ($SETTING['BBS_SLIP'] != "checked") $ID .= $slip.$SLIP_AREA;
	else $ID .= $slip;
}

# スレッド主/副表示 
if ($nusi and !$no) $ID .= " 主";
elseif ($subnusi and !$no) $ID .= " 副";

$ID .= " ";
# スレ立てID
if ($_POST['subject'] and $BSETTING['BBS_BE_TYPE2'] == "checked" and !$admin) {
	$createid = hash('sha256', $SLIP_IP.$SLIP_ID.$SLIP_TE.$SLIP_AC);
	$createid = substr(preg_replace("/[^0-9]/", "", $createid), 0, 9);
	$_POST['subject'] .= " [".$createid."]";
	$subject .= " [".$createid."]";
}
# ホスト表示
if ($SETTING['BBS_DISP_IP'] == "checked" and !$admin) $ID .="HOST:".$HOST." ";
# IP表示
elseif ($SETTING['BBS_DISP_IP'] == "siberia" and !$admin) $ID .="発信元:".$REMOTEADDR." ";
# IP(一部)表示
elseif ($SETTING['BBS_DISP_IP'] == "feature" and !$admin) $ID .="発信元:".$iprange.".* ";
# ブラウザ名表示
elseif ($SETTING['BBS_DISP_IP'] == "browser" and !$admin) $ID .="発信元:".$browser." ";
# ID非表示(強制表示の場合は不可)
$_POST['mail'] = str_replace("!id:none", "", $_POST['mail']);
# fusianasanでホスト表示
$_POST['FROM'] = str_replace("fusianasan", "</b>".$HOST."<b>", $_POST['FROM']);
# 県名表示
$_POST['FROM'] = str_replace("!ken", "</b>(".$ken.")<b>", $_POST['FROM']);
# SLIP表示
$_POST['FROM'] = str_replace("!slip", "</b>(".$SLIP_NAME." ".$SLIP_IP.$SLIP_ID."-".$SLIP_TE.$SLIP_AC.")<b>", $_POST['FROM']);
# 本日の利用料金
$bill = preg_replace('/[^0-9]/', '', substr($_SERVER[REMOTE_ADDR], -4)) * 12;
$_POST['FROM'] = str_replace("!bill", "</b>本日の利用料 ".$bill."円<b>", $_POST['FROM']);
# ランダム数字
$_POST['FROM'] = str_replace("!random", "</b>【".mt_rand(0,100)."】<b>", $_POST['FROM']);
# お年玉
$_POST['FROM'] = str_replace("!dama", "</b>【".mt_rand(0,3333)."円】<b>", $_POST['FROM']);
# 県名表示
$_POST['FROM'] = str_replace("!ken", "</b>(".$ken.")<b>", $_POST['FROM']);
# バージョン表示
$_POST['FROM'] = str_replace("!ver", "</b>BBS.CGI:".date("Ymd",filemtime($BBSSERV."bbs.cgi"))."<b>", $_POST['FROM']);

# VIP機能
	$dir = $BBQSERV."omikuji/";
		$omikuji_array = file($dir.'omikuji.txt');
	$i = 0;
	while ($i < 10) {
		$j = $i;
		
			$count = count($omikuji_array) - 1;
			if ((strpos($_POST['FROM'], '!omikuji') !== FALSE) and $i++ < 10) {
				$random = rand(0, $count);
				$_POST['FROM'] = preg_replace("/!omikuji/", "</b>".trim($omikuji_array[$random])."<b>", $_POST['FROM'], 1);
			}	
		if ($i == $j) break;
	}
# IDの空白を削除
$ID = trim($ID);
#====================================================
#　書き込む
#====================================================
#スレッドのデータを読み込む(再読込)
$LOG = file($thread_file);
#スレッドのレス数=現在のレス番を取得
if (!$_POST[subject]) $number = count($LOG) + 1;
else $number = 1;
		#スレッドログに保存
		$fp = fopen($thread_file, "a");	#ログを開く
		fputs($fp, "<>$_POST[FROM]<>$_POST[mail]<>$NOWTIME<>$ID<>$_POST[MESSAGE]<>$info<>$_POST[subject]<><>$_SERVER[HTTP_USER_AGENT]<>$terminal $USER_AGENT<>$phone<>$SID<>$REMOTE_HOST<>$_SERVER[REMOTE_ADDR]<>$_SESSION[REMOTE_ADDR]<><>$PHOEBELV<>\n");	#書き込み
		fclose($fp);
		#スレッドのデータを読み込む(再読込)
		$LOG = file($thread_file);
		#スレ主用
if ($nprocess) {
		list($num,$nam,$mai,$tim,$aid,,$inf,$subject,,$reple,$spa,$sink,$ui,$remothost,$apr,$si,$pv,$phoel,) = explode("<>",$LOG[0]);
		foreach ($SETTING as $key => $value) {
		if ($value) $SETT[$key] = $value;
		$value = 0;
		}
		$threadinfo = serialize($SETT);
		$LOG[0] = "$num<>$nam<>$mai<>$tim<>$aid<>$message<>$inf<>$subject<>$threadinfo<>$reple<>$spa<>$sink<>$ui<>$remothost<>$apr<>$si<>$pv<>$phoel<>\n";
	$fp = '';
	foreach($LOG as $tmp) $fp .= $tmp;
	file_put_contents($thread_file, $fp, LOCK_EX);
}
if ($sage != 'checked' and !$soko and $NOWTIME != filemtime($RESFILE)) {
	#新着ログに保存
	$IP = array();
	$IP = file($RESFILE);
	$count = 0;
	array_unshift($IP, "$subject<>$_POST[bbs]<>$_POST[key]<>$NOWTIME<>".substr(strip_tags($_POST['MESSAGE']), 0, 150)."<>$number<>\n");
	# レスファイル内のレス数を 50 個以内に調整して保存
	if (count($IP) > 100) {
	while (count($IP) > 50) array_pop($IP);
	}
	$IP = array_unique($IP);
	$fp = '';
	foreach($IP as $tmp) $fp .= $tmp;
	@file_put_contents($RESFILE, $fp, LOCK_EX);
}
#スレッドのデータを読み込む(再読込)
$LOG = file($thread_file);
#スレッドのレス数=現在のレス番を取得
if (!$_POST[subject]) $number = count($LOG);
else $number = 1;
if ($save) {
 $fp = '';
 foreach($LOG as $tmp) $fp .= $tmp;
 file_put_contents($backup_file, $fp, LOCK_EX);
}
 if ($SETTING[NOINDEX] != "checked") {
#====================================================
#　スレタイ検索（search）
#====================================================
if ($_POST['subject']) {
	$fp = fopen($BBQSERV."threads.txt", "a");
	fputs($fp, "$_POST[bbs]<>$_POST[key]<>$_POST[subject]<>$BSETTING[BBS_TITLE]<>$_SERVER[HTTP_HOST]<>\n");
	fclose($fp);
}
#====================================================
#　本文検索（find）
#====================================================
	$fp = fopen($BBQSERV."find.txt", "a");
	fputs($fp, "$_POST[bbs]<>$_POST[key]<>$subject<>$BSETTING[BBS_TITLE]<>$_SERVER[HTTP_HOST]<>$_POST[MESSAGE]<>$NOWTIME<>\n");
	fclose($fp);
	$FROG = file($BBQSERV."threads.txt");
	if (count($FROG) > 50000) {
	# 30000 個以内に調整して保存
	while (count($FROG) > 30000) array_shift($FROG);
	$FROG = array_unique($FROG);
	$fp = @fopen($BBQSERV."threads.txt", "w");
	foreach($FROG as $tmp) fputs($fp, $tmp);
	fclose($fp);
	}
#====================================================
#　ハッシュタグ
#====================================================
foreach ($tags as $tmp) {
	$fp = fopen($BBQSERV."hashtag/".$tmp.".txt", "a");
	fputs($fp, "$NOWTIME<>$_POST[bbs]<>$_POST[key]<>$_POST[MESSAGE]<>$subject<>$_SERVER[HTTP_HOST]<>\n");
	fclose($fp);
	$SROG = file($BBQSERV."hashtag/".$tmp.".txt");
	# 300 個以内に調整して保存
	while (count($SROG) > 500) array_shift($SROG);
	$SROG = array_unique($SROG);
	$fp = @fopen($BBQSERV."hashtag/".$tmp.".txt", "w");
	foreach($SROG as $tmp) fputs($fp, $tmp);
	fclose($fp);
}
 }
#====================================================
#　各ディレクトリのスレ一覧
#====================================================
if ($_POST['subject']) {
	if (!is_file($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/subject.txt")) touch($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/subject.txt");
	$IP = array();
	$IP = @file($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/subject.txt");
	array_unshift($IP, "$_POST[key]<>$subject<>$ID<>$_POST[MESSAGE]<>\n");
	$fp = '';
	foreach($IP as $tmp) $fp .= $tmp;
	file_put_contents($BBSSERV.$_POST['bbs']."/".substr($_POST[key], 0, 4)."/".substr($_POST[key], 0, 5)."/subject.txt", $fp, LOCK_EX);
}

#====================================================
#　ファイル操作（subject.txt）
#====================================================
if ($_POST['subject'] or $NOWTIME != filemtime($subjectfile)) {

$PAGEFILE = array();
# サブジェクトファイルを読み込む
# スレッドキー.dat<>タイトル (レスの数)\n
# $PAGEFILE = array('スレッドキー',・・・)
# $SUBJECT = array('スレッドキー'=>'タイトル','レス数','最終更新','>>1のID')
$subr = @file($subjectfile);
if ($subr) {
	foreach ($subr as $tmp){
		$tmp = rtrim($tmp);
		list($tkey, $va, $vb, $vc, $vd, $ve,) = explode("<>", $tmp);
		if (!$tkey || preg_match("/[^0-9]/", $tkey)) continue;
		array_push($PAGEFILE,$tkey);
		$SUBJECT[$tkey] = "$va<>$vb<>$vc<>$vd<>$ve<>";
	}
}
# サブジェクト数を取得
$FILENUM = count($PAGEFILE);
# スレッド数上限
if (!$BSETTING['BBS_THREAD_QUANTITY']) $BSETTING['BBS_THREAD_QUANTITY'] = 600;
# 新規スレッドの場合は1個追加＆IDを入れる
# サブジェクト数がスレッド数上限を超えた場合下から削除（dat落ち）
if ($_POST['subject']) {
$FILENUM++;
$nid = $ID;
 if ($FILENUM > $BSETTING['BBS_THREAD_QUANTITY'] + 20) {
  while (count($PAGEFILE) > $BSETTING['BBS_THREAD_QUANTITY']) array_pop($PAGEFILE);
 }
}
if ($_POST['subject']) $hide = '';
$subtm = "$_POST[key]<>$subject<>$number<>$NOWTIME<>$nid<>$hide<>";
# サブジェクトハッシュを書き換える
$SUBJECT[$_POST[key]] = "$subject<>$number<>$NOWTIME<>$nid<>$hide<>";
# サブジェクトテキストを開く
$fp = '';
#一括書き込み
# soko
if (!$_POST['subject'] and $soko) {
	foreach ($PAGEFILE as $tmp) {
		# $_POST['key']は現在書き込みしたスレッドキー（底）
		if ($tmp != $_POST['key']) {
			$i++;
			$fp .= "$tmp<>$SUBJECT[$tmp]\n";
		}
	}
	$fp .= "$subtm\n";
}
# sageの時は上がらない
elseif (!$_POST['subject'] and $sage) {
	foreach ($PAGEFILE as $tmp) $fp .= "$tmp<>$SUBJECT[$tmp]\n";
}
else {
	# 上がるキーは一番最初に持ってくる
	if (!$_POST['subject']) $fp .= "$subtm\n";
	$i = 1;
	foreach ($PAGEFILE as $tmp) {
		# 新規スレッドの場合は5番目に追加
		if ($_POST['subject'] and $i == 5) {
		$fp .= "$subtm\n";
		$added = true;
		}
		# $_POST['key']は現在書き込みしたスレッドキー（上がっている）
		if ($tmp != $_POST['key']) {
			$i++;
			$fp .= "$tmp<>$SUBJECT[$tmp]\n";
		}
	}
	if ($_POST['subject'] and !$added) $fp .= "$subtm\n";
}
file_put_contents($subjectfile, $fp, LOCK_EX);
if (substr($_POST['key'], 0, 3) != 900 and substr($_POST['key'], 0, 3) != 924 and count($subr) > 15) file_put_contents($BBSSERV.$_POST[bbs]."/subject.cgi", $fp, LOCK_EX);

}
#====================================================
#　書き込み時間を記録
#====================================================
if (!$login) {
$_SESSION['posttime'] = $NOWTIME;
# 中身はsidの内容にする
@file_put_contents($kirokufile, serialize($_SESSION));
}
#############################################################################
# メインルーチン終わり。お疲れ様でした。
#############################################################################
endhtml();

#====================================================
#　書き込み完了画面
#====================================================
function endhtml($error) {
	global $sttime, $NOWTIME, $operatecap, $errorskip, $SID, $Cookname, $Cookmail;
	if ($error) header('X-Chx-Error: '.$error);
	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) setcookie("response", mb_convert_encoding("書きこみました", 'HTML-ENTITIES', 'SJIS-win'), $NOWTIME+5, "/");
	if ($_POST['subject']) $readmode = 'read.html';
	else $readmode = 'read.cgi';
	$endtime = microtime(true);
	$sec = $endtime - $sttime;
	$sec = substr($sec, 0, 8);
	$kakikomigamen = '<html><head><title>書きこみました。</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta content=1;URL=//'.$_SERVER[HTTP_HOST].'/test/read.cgi/'.$_POST[bbs].'/'.$_POST[key].'/l50 http-equiv=refresh></head><body>書きこみが終わりました。 ['.$sec.']<br><br>画面を切り替えるまでしばらくお待ち下さい。<?=$L?></body></html>';
	$set_cookie = '<script type="text/javascript"><!-- 
';
	$set_cookie .= 'cookname = escape("'.addslashes($Cookname).'"); document.cookie = "NAME="+cookname+"; expires='.$exp.'; path=/"; ';
	$set_cookie .= 'cookmail = escape("'.addslashes($Cookmail).'"); document.cookie = "MAIL="+cookmail+"; expires='.$exp.'; path=/"; ';
	$set_cookie .= 'window.location.href="https://'.$_SERVER[HTTP_HOST].'/test/'.$readmode.'/'.$_POST[bbs].'/'.$_POST[key].'/l10/?ls=10"; ';
	$set_cookie .= '//--></script>';
	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) $kakikomigamen .= $set_cookie;
	exit($kakikomigamen);
}
#====================================================
#　エラー画面（エラー処理）
#====================================================
#DispError(TITLE,TOPIC);
function DispError($title,$topic,$error) {
	global $HOST, $NOWTIME, $errorskip, $SIDPATH, $SID, $file_ipaddr, $BBSSERV, $DATE, $number, $BBX, $BBM, $monafile, $terminal, $USER_AGENT, $HASH, $kirokufile, $login;
	if ($errorskip) return;
	if ($error) header('X-Chx-Error: '.$error);
	else header('X-Chx-Error: 9999 Not yet;');
	#不正取得対策
	if (!$_SESSION['firsttime'] or $NOWTIME < $_SESSION['firsttime'] + 300) {
	 if (strpos($topic, 'BBx規制中') !== false) @unlink($SIDPATH.$SID);
	}
	#エラーログに保存
	$errorc = @file_get_contents($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi");
	if (strpos($topic, 'Sorry') === false) {
	 if (!is_file($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi")) $errorc = 1;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 2) {
	  $errorc += 64;
	  $errorc *= 2;
	 }
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 3) $errorc += 128;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 5) $errorc += 64;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 15) $errorc += 32;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 30) $errorc += 16;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 60) $errorc += 8;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 120) $errorc += 4;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 180) $errorc += 2;
	 elseif ($NOWTIME < filemtime($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi") + 1800) $errorc += 1;
	 else {
	  @unlink($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi");
	  $errorc = 0;
	 }
	}
	if ($errorc) @file_put_contents($BBSSERV."/".date('z')."/error_".$file_ipaddr.".cgi", $errorc);
	if ($errorc > 1024) @touch($BBSSERV."/".date('z')."/403_".$file_ipaddr.".cgi");
	$EROG = file($BBSSERV."errors.cgi");
	array_unshift($EROG, $NOWTIME." ".$DATE." IP:".$_SERVER[REMOTE_ADDR]." ".$SESSION[REMOTE_ADDR]." HOST:".$HOST." PLACE:".$_POST[bbs]."/".$_POST[key]."/".$number." Key:".$SID." STATUS:".$topic." UA:".$_SERVER[HTTP_USER_AGENT]." UA2:".$terminal." ".$USER_AGENT." TEXT:".$_POST['subject'].$_POST['FROM'].$_POST['mail'].$_POST['MESSAGE']." HASH:".$HASH."\n");
	# 500 個以内に調整して保存
	while (count($EROG) > 500) array_pop($EROG);
	$EROG = array_unique($EROG);
	$fp = @fopen($BBSSERV."errors.cgi", "w");
	foreach($EROG as $tmp) fputs($fp, $tmp);
	fclose($fp);
	# 中身はsidの内容にする
	if (!$login) @file_put_contents($kirokufile, serialize($_SESSION));
	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) setcookie("response", mb_convert_encoding($topic, 'HTML-ENTITIES', 'SJIS-win'), $NOWTIME+5, "/");
	if (!$login) $loggd = '<br><a href="https://rentalbbs.net/login.html">ログインして書くことができます</a>';
	else $loggd = '';
	?>
<html>
<head>
<title><?=$title?></title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</head>
<body bgcolor="#FFFFFF">
<font size=+1 color=#FF0000><b><?=$topic?><?=$loggd?></b></font>
<ul>
ホスト<b><?=$HOST?></B></B><br><b><?=$_POST['subject']?> </b><br><ul>
名前： <b><?=$_POST['FROM']?></b><br>E-mail： <?=$_POST['mail']?><br>
内容：<br><?=$_POST['MESSAGE']?><br>
</ul></ul>
<hr>
<ul>
<font size=+1 color=#00AA00><b>エラーの原因が分からない？</b></font>
<ul style="line-height:1.5;">
まず確認しよう！<br>
<b>
《<a href="https://rentalbbs.net/faq/">FAQ</a>》<br>
《<a href="../<?=$_POST['bbs']?>/">掲示板へ戻る</a>》<br>
《<a href="../<?=$_POST['bbs']?>/subback.html">スレッド一覧へ戻る</a>》<br>
《<a href="../test/read.cgi/<?=$_POST['bbs']?>/<?=$_POST['key']?>/">スレッドへ戻る</a>》<br>
</b>
</ul><br>
<font size=+1 color=#DD00DD><b>もしかしてアクセス規制ですか？</b></font>
<ul style="line-height:1.5;">
<b>各板の管理者さんが規制を解除するまで規制は続きます。</b><br>
個別の対応・進展については、各板の管理者さんへお尋ねください。<br>
</ul>
</ul></body>
</html><?
	exit;
}
#====================================================
#　エラー画面(仮)
#====================================================
#DispError2(TITLE,TOPIC);
function DispError2($title,$topic,$error) {
	global $BBSSERV,$HOST,$NOWTIME,$login,$DATE,$number,$SID,$terminal,$USER_AGENT,$HASH,$EROG;
	if ($error) header('X-Chx-Error: '.$error);
	else header('X-Chx-Error: 9999 Not yet;');
	$EROG = file($BBSSERV."errors.cgi");
	array_unshift($EROG, $NOWTIME." ".$DATE." IP:".$_SERVER[REMOTE_ADDR]." ".$SESSION[REMOTE_ADDR]." HOST:".$HOST." PLACE:".$_POST[bbs]."/".$_POST[key]."/".$number." Key:".$SID." STATUS:".$topic." UA:".$_SERVER[HTTP_USER_AGENT]." UA2:".$terminal." ".$USER_AGENT." TEXT:".$_POST['subject'].$_POST['FROM'].$_POST['mail'].$_POST['MESSAGE']." HASH:".$HASH."\n");
	# 500 個以内に調整して保存
	while (count($EROG) > 500) array_pop($EROG);
	$EROG = array_unique($EROG);
	$fp = @fopen($BBSSERV."errors.cgi", "w");
	foreach($EROG as $tmp) fputs($fp, $tmp);
	fclose($fp);
	if (strpos($_SERVER['HTTP_USER_AGENT'], 'Mozilla') !== false) setcookie("response", mb_convert_encoding($topic, 'HTML-ENTITIES', 'SJIS-win'), $NOWTIME+5, "/");
	?>
<html>
<head>
<title><?=$title?></title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</head>
<body bgcolor="#FFFFFF">
<font size=+1 color=#FF0000><b><?=$topic?></b></font>
<ul>
ホスト<b><?=$HOST?></B></B><br><b><?=$_POST['subject']?> </b><br><ul>
名前： <b><?=$_POST['FROM']?></b><br>E-mail： <?=$_POST['mail']?><br>
内容：<br><?=$_POST['MESSAGE']?><br>
</ul></ul>
<hr>
<ul>
<font size=+1 color=#00AA00><b>エラーの原因が分からない？</b></font>
<ul style="line-height:1.5;">
まず確認しよう！<br>
<b>
《<a href="https://rentalbbs.net/faq/">FAQ</a>》<br>
《<a href="../<?=$_POST['bbs']?>/">掲示板へ戻る</a>》<br>
《<a href="../<?=$_POST['bbs']?>/subback.html">スレッド一覧へ戻る</a>》<br>
《<a href="../test/read.cgi/<?=$_POST['bbs']?>/<?=$_POST['key']?>/">スレッドへ戻る</a>》<br>
</b>
</ul><br>
<font size=+1 color=#DD00DD><b>もしかしてアクセス規制ですか？</b></font>
<ul style="line-height:1.5;">
<b>各板の管理者さんが規制を解除するまで規制は続きます。</b><br>
個別の対応・進展については、各板の管理者さんへお尋ねください。<br>
</ul>
</ul></body>
</html><?
	exit;
}
#############################################################################
# 確認画面
#############################################################################
function Kakunin() {
?><html><head><title>投稿確認</title></head><body bgcolor=#EEEEEE><br>下記の内容で投稿します。よろしいですか？<br>
<form method="POST" accept-charset="Shift_JIS" action="/test/bbs.cgi?manment=true" id="postForm">
<div class="p"><?=$_POST['subject']?></div><br>
<b>名前：</b><br>
<div class="p"><input name="FROM" size="19" value="<?=$_POST['FROM']?>"></div><br>
<b>Email:</b><br>
<div class="p"><input name="mail" size="19" value="<?=$_POST['mail']?>"></div><br>
<b>本文：</b><br>
<div class="p"><textarea name="MESSAGE"><?=$_POST['MESSAGE']?></textarea></div><br>
<input type="hidden" name="subject" value="<?=$_POST['subject']?>">
<input type="hidden" name="bbs" value="<?=$_POST['bbs']?>">
<input type="hidden" name="key" value="<?=$_POST['key']?>">
<input type="hidden" name="time" value="<?=$_POST['time']?>">
<input type="hidden" name="cert" value="<?=$_POST['cert']?>">
<button class="g-recaptcha" data-sitekey="6Lc-RPUkAAAAAFkxT-Rl63bG8MqlsVIjq6N3gUR5" data-callback="onSubmit" error-callback="onReCaptchaError">書き込む</button>
</form>
</body>
<style>
.p{margin-left:10pt}
</style>
<script>
if (localStorage.getItem('reCAPTCHA') === null) localStorage.setItem('reCAPTCHA', true);
if (localStorage.getItem('reCAPTCHA') == "true") {
var recaptchajs = document.createElement("script");
recaptchajs.src = "https://www.google.com/recaptcha/api.js";
document.body.appendChild(recaptchajs);
document.getElementById('postForm').action = '/test/bbs.cgi';
}
function onSubmit(token) {
 document.getElementById('postForm').submit();
}
function onReCaptchaError() {
 document.getElementById('postForm').action = '/test/bbs.cgi?manment=true';
}
</script><?	# 画面出したら exit してしまう
	exit;
}
#############################################################################
# 投稿確認画面
#############################################################################
function HoutekiToukouKakunin() {
	global $kirokufile;
	setcookie("ToukouKakunin", "pass", $NOWTIME+2592000, "/", "rentalbbs.net");
	header('X-Chx-Error: 0001 Confirmation phase;');
?><html><!-- 2ch_X:cookie --><head><title>■ 書き込み確認 ■</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" /></head><body bgcolor=#EEEEEE><font size=+1 color=#FF0000><b>書きこみ＆クッキー確認</b></font><ul><br><br><b><?=$_POST['subject']?> </b><br>名前： <?=$_POST['FROM']?><br>E-mail： <?=$_POST['mail']?><br>内容：<br><?=$_POST['MESSAGE']?><br><br></ul><b>投稿確認<br><b style="color: #F00; font-size: larger;">この書き込みで本当にいいですか？<br>犯罪予告や犯罪示唆、誹謗中傷、性的な出会いを目的とした書き込みでないか今一度確認してくださいね。</b><br>・投稿者は、投稿に関して発生する責任が全て投稿者に帰すことを承諾します。<br>・投稿者は、話題と無関係な広告の投稿に関して、相応の費用を支払うことを承諾します。<br>・投稿者は、掲示板運営者が指定する第三者に対して、一切の権利（第三者に対して再許諾する権利を含みます）を許諾しないことを承諾します。<br>・投稿者は、掲示板運営者あるいはその指定する者に対して、著作者人格権を一切行使しないことを承諾します。<br></b>変更する場合は戻るボタンで戻って書き直してください。<br><br>現在、荒らし対策でクッキーを設定していないと書きこみできないようにしています。<br><font size=-1>(登録されている情報が変わるとこの画面がでます。)</font><br><b style="color: #F00; font-size: larger;">この画面が繰り返し出る場合はcookieを削除してみてください。</b><br></body><br></html><?
	# 中身はsidの内容にする
	@file_put_contents($kirokufile, serialize($_SESSION));
	exit;
}
#====================================================
#　BBQ登録(proxy60)
#====================================================
function Burned($topic) {
	global $BBSSERV, $BBQSERV, $banfile, $banfile1, $banfilea, $bbx_file, $bbm_file, $bbx_kiroku, $SID, $monafile, $errorskip, $file_ipaddr, $login, $BANF;
	if ($errorskip) return;
		#ログイン時
		if ($login) @file_put_contents($BANF, "Registered:".date("Ymd-His"));
		#BBQ
		$bbqfile = $BBQSERV."/bbq/".$file_ipaddr.".cgi";
		$bbq = @file_get_contents($bbqfile);
		if (!$bbq) $bbq = 1;
		else ++$bbq;
		@file_put_contents($bbqfile, $bbq);
		if ($bbq >= 65) @file_put_contents($banfile, "Registered:".date("Ymd-His")." BBR-".$bbq);
		elseif ($bbq >= 33) @file_put_contents($banfile1, "Registered:".date("Ymd-His")." BBR-".$bbq);
		elseif ($bbq >= 11) @file_put_contents($banfilea, "Registered:".date("Ymd-His")." BBR-".$bbq);
		#BBX
		@file_put_contents($bbx_file, "Registered:".date("Ymd-His")." BBR-".$bbq);
		#BBM
		if ($bbm_file) @file_put_contents($bbm_file, "Registered:".date("Ymd-His"));
		#鍵無効
		$_SESSION['kisei'] = date('z');
		setcookie("TAKO", "ODORI", $NOWTIME+86400, "/");
		setcookie("yuki", "akari", $NOWTIME+86400, "/");
		#規制発動を記録
		$BBXROG = file($bbx_kiroku);
		array_unshift($BBXROG, "IP:".$_SERVER['REMOTE_ADDR']."FIP:".$_SESSION['REMOTE_ADDR'].",SID:".$SID.",Thread:".$_POST[bbs]."/".$_POST[key].",Registered:".date("Ymd-His")."=>ERROR: ".$topic."\n");
		# 500 個以内に調整して保存
		while (count($BBXROG) > 500) array_pop($BBXROG);
		$BBXROG = array_unique($BBXROG);
		$fp = @fopen($bbx_kiroku, "w");
		foreach($BBXROG as $tmp) fputs($fp, $tmp);
		fclose($fp);
		if (is_file($monafile)) @unlink($monafile);
}
#====================================================
#　トリップを変換する関数
#====================================================
function nametrip($tripkey) {
	// check
	preg_match('|^#(.*)$|', $tripkey, $keys);
	if(empty($keys[1])) return false;
	$tripkey = $keys[1];

	// start
    if (strlen($tripkey) >= 12) {
			 // digit 12
			$mark = substr($tripkey, 0, 1);
			if($mark == '#' || $mark == '$'){
				if(preg_match('|^#([[:xdigit:]]{16})([./0-9A-Za-z]{0,2})$|', $tripkey, $str)){
					$trip = substr(crypt(pack('H*', $str[1]), "$str[2].."), -10);
				}else{
					// ext
					$trip = '???';
				}
			}else{
				$trip = substr(base64_encode(sha1($tripkey, TRUE)), 0, 12);
				$trip = str_replace('+', '.', $trip);
			}
    } else { // 10 digits
	$salt = substr($tripkey."H.", 1, 2);
	$salt = preg_replace("/[^\.-z]/", ".", $salt);
	$salt = strtr($salt,":;<=>?@[\\]^_`","ABCDEFGabcdef");
	$trip = substr(crypt($tripkey, $salt),-10);
    }
	$trip = ' </b>◆'.$trip.' <b>';
	return $trip;
}
?>