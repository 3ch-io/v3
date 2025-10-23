<?php
header("Content-type: text/html; charset=Shift_JIS");
$st = $to = 0;
$nofirst = '';
$ls = 0;
$placeholder = array("あなたが書くのを待っています...", "何をお考えですか？", "言いたいことは？", "ここに書いてください", "何かありましたか？", "コメントする...", "コメントを追加…");
shuffle($placeholder);
#==================================================
#　時刻を設定
#==================================================
$NOW = time();
$today = getdate(); 
$JIKAN = $today['hours']; 
#==================================================
#　リクエスト解析
#==================================================
if ($_SERVER['REQUEST_METHOD'] != 'GET') exit;
$pairs = explode('/',$_SERVER['REQUEST_URI']);
	$bbs = $pairs[3];
	$key = $pairs[4];
	if (!empty($pairs[5])) {
		if (strstr($pairs[5], 'n')) {
			#$nofirst = 'true';
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
	if (!$bbs) exit;
$cgiurl = str_replace("read.html","read.cgi",$_SERVER['REQUEST_URI']);
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
$BBSSERV = "/virtual/oyster356s/public_html/".$_SERVER['HTTP_HOST']."/";	#格納鯖のパス
preg_match("/(.*)(\/test\/read\.cgi)(.*)/", $_SERVER['SCRIPT_NAME'], $match);
$URL = 'https://'.$_SERVER['HTTP_HOST'].$match[1];
$SCRIPT = $match[2];
$BASEURL = "$URL/$bbs/";
if(!file_exists($BBSSERV.$bbs."/")) nodat();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/")) nodat();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/")) nodat();
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
	$s = $LINENUM - $match[1] + 1;
}
if ($s < 1) $s = 1;
if ($s > 1) $mae = $s-1;
$fsize = (int)(filesize($thread_file) / 1024);
list($num,,,,,,,$subject,$threadinfo,) = explode("<>",$LOG[0]);
	if ($num == "saku") nodat();
	if ($num == "del" || strpos($num, "del") !== false) {
		$subject='削除済み';
	}
if (!empty($pairs[5]) and $nofirst and $st == $to and strpos($_SERVER['REQUEST_URI'], "?") === false) $prm = "history.replaceState(null, '".$subject."', '/test/read.html/".$bbs."/".$key."/".$st."/?st=".$st."&to=".$to."&nofirst=true');";
else $prm = "";
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
if (!$isdat) $stop = true;
# 停止済みスレッド
if ($SETTING['THREAD_STOP'] == "yes") $stop = true;
# 即死判定
if (!$SETTING['BBS_TH_LINE']) $SETTING['BBS_TH_LINE'] = 1;
if (!$SETTING['TIME_TO_LIVE']) $SETTING['TIME_TO_LIVE'] = 1209600;
if ($NOW > $key + $SETTING['TIME_TO_LIVE'] and $SETTING['BBS_TH_LINE'] > $LINENUM) $stop = true;
# 突然死判定
if ($live and !$SETTING['BBS_MAX_MODIFIED']) $SETTING['BBS_MAX_MODIFIED'] = 18000;
if ($SETTING['BBS_MAX_MODIFIED'] and $NOW > filemtime($thread_file) + $SETTING['BBS_MAX_MODIFIED']) $stop = true;
# lifetimeルール
if ($SETTING['BBS_THREAD_LIFETIME'] and $NOW > $key + $SETTING['BBS_THREAD_LIFETIME']) $stop = true;
# 最大レス数超え
if ($LINENUM >= $SETTING['MAX_RES']) $maxover = $SETTING['MAX_RES'];
# 最大レス数近い
if ($LINENUM >= $SETTING['MAX_RES'] - 50) $maxout = $SETTING['MAX_RES'] - 50;
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
	$b_file = $BBSSERV."/tmp/".$bbs.date('z')."/b_".$bbs.$key.".cgi";
	if (!is_file($b_file)) @touch($b_file);
	$b = file($b_file);
if ($_COOKIE['b']) {
list($bb,$bk,$bs,$bt,$be) = explode("<>",$_COOKIE['b']);
 if ($bb and $bk and $bs and $bt and $be) {
	if ($bk != $key and $bb == $bbs) {
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
	if ($b[0]) $bh = "\n■ このスレを見ている人はこんなスレも見ています。<br>\n";
	$fp = '';
	foreach($b as $tmp) {
	list($bba,$bka,$bsa,$bta,$bea) = explode("<>",$tmp);
	$bh .= "<a href=\"https://$bea/test/read.html/$bba/$bka/l10/?ls=10\" title=\"$bsa\">$bsa</a><br>\n";
	$fp .= $tmp;
	}
if ($_COOKIE['b']) @file_put_contents($b_file, $fp, LOCK_EX);
if (!$stop and !$maxover and $SETTING[NOINDEX] != "checked") setcookie("b", $bbs."<>".$key."<>".$subject."<>".$SETTING['BBS_TITLE']."<>".$_SERVER['HTTP_HOST'], $NOW+3600*24, "/", "delight.rentalbbs.net");
#==================================================
#　出力
#==================================================
?><!DOCTYPE HTML>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><meta property="og:title" content="<?=$subject?> - <?=$SETTING[BBS_TITLE]?> - レンタル掲示板delight"><meta name="og:description" content="スレッドフロート式高機能無料レンタル掲示板：delight。"><meta property="og:url" content="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/"><meta property="og:type" content="website"><meta property="og:site_name" content="レンタル掲示板delight"><link rel="apple-touch-icon" href="https://delight.rentalbbs.net/icon.png"><link rel="icon" href="https://delight.rentalbbs.net/favicon.ico">
<noscript>
<meta http-equiv="refresh" content="0; URL=https://<?=$_SERVER['HTTP_HOST']?><?=$cgiurl?>">
</noscript>
<script>
if (navigator.userAgent.search(/bot/) != -1) location.href = 'https://<?=$_SERVER['HTTP_HOST']?>/test/read.cgi/<?=$bbs?>/<?=$key?>/';
<?=$prm?>
</script>
<script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script><script type="text/javascript" src="https://delight.kakiko.org/js/ad.js"></script><script type="text/javascript" src="https://delight.kakiko.org/js/index.js"></script><title><?=$subject?></title><link href="https://delight.kakiko.org/css/ad.css" rel="stylesheet" type="text/css"><link href="https://delight.kakiko.org/css/st.css" rel="stylesheet" type="text/css"><link href="https://delight.kakiko.org/css/milligram.css" rel="stylesheet" type="text/css"><link href="https://delight.kakiko.org/css/s.css" rel="stylesheet" type="text/css"><link href="https://delight.kakiko.org/css/read.css" rel="stylesheet" type="text/css">
</head><body><section class="section"><div id="body">
<script type="text/javascript" src="https://delight.kakiko.org/js/thread.js"></script>
<div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="font-size:15px !important;"><?=$SETTING['BBS_TITLE']?></div><div class="search-input"><input id="search-text" type="text" placeholder="キーワードを入力" style="height:25pt"><button id="search-button"><img src="https://delight.rentalbbs.net/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><a class="number" href="javascript:MenuClick('setting')"><div class="search-setting dropdown"><img class="dropBtnSetting settingDrop" src="https://delight.rentalbbs.net/static/icon_settings.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop"><span class="dropBtnSetting">設定</span><img class="dropBtnSetting" src="https://delight.rentalbbs.net/static/icon_extend.png" style="margin-left:5px;margin-bottom:2px;"></span></div></a></div><div class="search-clear"></div></div><div class="topmenu"><a class="menuitem" href="https://delight.rentalbbs.net/">delight</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?><?=$cgiurl?>">read.cgiに切替える</a><a id="back" class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/">全部</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/-100/?to=100">1-</a><?php for ($iCnt = 100; $iCnt <= $LINENUM; $iCnt += 100){
	$iTo = $iCnt + 99;
	echo "<a class=\"menuitem\" href=\"/test/read.html/$bbs/$key/$iCnt-$iTo/?st=$iCnt&to=$iTo\">$iCnt-</a>";
} ?><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/l50/?ls=50">最新50</a></div><? if ($maxover) { ?><div class="stoplight">レス数が<?=$maxover?>を超えています。これ以上書き込みはできません。</div><?php }elseif ($stop) { ?><div class="stoplight">■ このスレッドは過去ログ倉庫に格納されています</div><?php }elseif ($maxout) { ?><div class="stoplight">レス数が<?=$maxout?>を超えています。<?=$SETTING[MAX_RES]?>を超えると書き込みができなくなります。</div><?php } ?><h1 class="title"><?=$subject?></h1><div class="pagestats"><?=$LINENUM?>コメント/<?=$fsize?>KB</div><div class="thread" id="thread">
<?php
$e = $END + 1;
$t = $END + 100;
$f = $s - 1;
$u = $f - 100;
if ($f < 1) $f = 1;
if ($u < 1) $u = 1;
$cert = hash('sha256', $BBSSERV.$_SERVER['HTTP_HOST'].$bbs.$key.$NOW.$subject.$_SERVER['REMOTE_ADDR'].$_SERVER[HTTP_USER_AGENT].$_SERVER[HTTP_ACCEPT_LANGUAGE]);
?></div><div class="pagestats"><?=$LINENUM?>コメント/<?=$fsize?>KB</div><? if ($maxover) { ?><div class="stoplight">レス数が<?=$maxover?>を超えています。これ以上書き込みはできません。</div><?php }elseif ($stop) { ?><div class="stoplight">■ このスレッドは過去ログ倉庫に格納されています</div><? }else { ?><hr><div class="newposts"><center><a href="javascript:reload()">リロード</a> <a href="/test/read.html/<?=$bbs?>/<?=$key?>/<?=$END?>-n/?st=<?=$END?>&nofirst=true">新着レスの表示</a></center></div><hr><? } ?><div class="bottommenu"><a id="bback" class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/">全部</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/<?=$u?>-<?=$f?>/?st=<?=$u?>&to=<?=$f?>">前100</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/<?=$e?>-<?=$t?>/?st=<?=$e?>&to=<?=$t?>">次100</a><a class="menuitem" href="https://<?=$_SERVER['HTTP_HOST']?>/test/read.html/<?=$bbs?>/<?=$key?>/l50/?ls=50">最新50</a></div><div class="formbox"><form method="POST" accept-charset="Shift_JIS" action="//<?=$_SERVER['HTTP_HOST']?>/test/bbs.cgi" <? if ($stop or $maxover) echo 'style="display:none;"'; ?>><hr><div class="fbox" style="max-width: 600px;"><span class="fhead"><span class="spformhead" style="display:none;border-radius:3px 3px 0 0;color:#666;padding:3px;"><span style="padding-top: 10px;display: inline-block;" onclick="fclose()">キャンセル</span></span><span class="submitbtn"><input type="submit" value="書き込む" name="submit" onclick="Post()"></span></span><span class="input"><input name="FROM" size="19" placeholder="名前"></span><span class="input"><input name="mail" size="19" value="<?=$_COOKIE["MAIL"]?>" placeholder="E-mail"></span><div class="backmsg" style="display: inline-block;"><a href="<?=$_COOKIE[homepage]?>" target="_blank"><img src="<?=$_COOKIE[icon]?>" class="icon" width="50" height="50" align="left"></a><input value="on" type="checkbox" id="seticon" name="icon" checked><a href="/test/icon.cgi">アイコン</a> <a href="javascript:BackMSG()">下書きを復元</a></div><textarea rows="5" cols="70" wrap="off" name="MESSAGE" placeholder="<?=$placeholder[0]?>"></textarea><input type="hidden" name="bbs" value="<?=$bbs?>"><input type="hidden" name="key" value="<?=$key?>"><input type="hidden" name="time" value="<?=$NOW?>"><input type="hidden" name="cert" value="<?=$cert?>"><br>画像：<input id="uploadImage" type="file" name="file" size="50" onchange="upload();"><br></div></form></div>
<div id="hidemetoo" class="side p85 slightpad nobullets">
<div style="min-height:50px">■ 告知欄<br><?=$kokuti?></div><?=$bh?><div id="hline" style="display:none"><div id="more"></div>■ 新着書き込み<div id="headline"></div></div>
</div>
<style>
body{background-color:<?=$SETTING['BBS_THREAD_COLOR']?>;color:<?=$SETTING['BBS_TEXT_COLOR']?>;}a{color:<?=$SETTING['BBS_LINK_COLOR']?>;}a:visited{color:<?=$SETTING['BBS_VLINK_COLOR']?>;}a:hover{color:<?=$SETTING['BBS_ALINK_COLOR']?>;}.message{color:<?=$SETTING['BBS_TEXT_COLOR']?>;}
</style>
<script type="text/javascript" src="https://delight.kakiko.org/js/read.js"></script>
</div></section>
</body></html><? exit;
function nodat() {
	global $bbs;
	?><!DOCTYPE HTML>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script><script type="text/javascript" src="https://delight.kakiko.org/js/ad.js"></script><title>datが存在しません。削除されたかURL間違ってますよ。</title><link href="https://delight.kakiko.org/css/ad.css" rel="stylesheet" type="text/css"><link href="https://delight.kakiko.org/css/read.css" rel="stylesheet" type="text/css"></head><body><section class="section"><div id="body"><script type="text/javascript" src="https://delight.kakiko.org/js/sp.js"></script><div class="return"><a href="//<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">■掲示板に戻る■</a></div><div class="errorCode">datが存在しません。削除されたかURL間違ってますよ。</div></div></section></body></html><? exit;
}
?>