<?php
header("Content-Type: text/html; charset=Shift_JIS");
	$file_name = $BBSSERV.$_POST[bbs]."/subject.txt";
	$comment = '';
	if (isset($_POST['subjecttext']) and $_POST['smode'] == 'write') {
		if (get_magic_quotes_gpc()) $_POST['subjecttext'] = stripslashes($_POST['subjecttext']);
		$fp = fopen($file_name, "w");
		fputs($fp, $_POST['subjecttext']);
		fclose($fp);
		$comment = "スレ一覧を更新しました。";
	}
	$text = implode('', file($file_name));
	?>
<html>
<head>
<title>スレ一覧編集</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" href="main.css" type="text/css">
</head>
<body>
<h3>スレ一覧編集</h3>
<hr>
<font color="red"><?=$comment?></font><br>
<b>subject.txt</b>を編集しています
<div>hideが含まれているスレッドは過去ログです(一覧に表示されません)</div>
<div>1行につき1つのスレッドです。</div>
<div>行を削除するとそのスレッドは一覧に表示されなくなり、過去ログ扱いとなります</div>
<br>
<form action="" method="POST">
<input type="hidden" name="bbs" value="<?=$_POST[bbs]?>"><input type="hidden" name="PASSWORD" value="<?=$_POST[PASSWORD]?>"><input type="hidden" name="PASS" value="<?=$_POST[PASSWORD]?>"><input type="hidden" name="smode" value="write">
<input type="submit" name="subject" value="変更">
<input type="reset" name="reset" value="リセット"><br>
<textarea rows="30" cols="80" name="subjecttext"><?=$text?></textarea>
</form>
<hr>
<div><a href="/<?=$_POST[bbs]?>/index.html">板TOPへ戻る</a></div>
</body>
</html>
<?php
	exit;
?>