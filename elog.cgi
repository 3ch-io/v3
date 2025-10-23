<?php
header("Content-type: text/html; charset=Shift_JIS");
$NOWTIME = time();
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>エラーログ閲覧</title><link href="https://rentalbbs.net/css/a.css" rel="stylesheet" type="text/css"></head><body><div id="container"><section><h1 class="section-title">エラーログ閲覧</h1><div>1行につき一つのエラーです</div>
<hr>
<div><?=$_POST[bbs]?>板のエラーログ：</div>
<?
$file = $BBSSERV."errors.cgi";
$LOG = file($file);
foreach($LOG as $tmp){
	if (stristr($tmp, "PLACE:".$_POST[bbs]."/") === false) continue;
	echo '<div>'.$tmp.'</div><br>';
}
?>
<hr>
<div><a href="/<?=$_POST[bbs]?>/index.html">板TOPへ戻る</a></div>
<small><div>注：以下のエラーなど一部の投稿規制は表示されません</div></small><div>ERROR: 別の人が同時刻にスレッドを立てようとしています。<br>偽造ブラウザ検出規制<br>"ERROR: 新仕様に対応した専用ブラウザをご利用ください。","E3001 Unavailable an old dedicated browser.;"の一部<br>ERROR: 未登録のバージョンです。<br><br>Ruthless Angel</div>
</section></body></html><? exit;
?>