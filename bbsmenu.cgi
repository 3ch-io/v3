<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<TITLE><?=$_SERVER[HTTP_HOST]?>の掲示板一覧</TITLE>
<BASE TARGET="_top">
</HEAD>
<BODY BGCOLOR="SEASHELL" TEXT="#E60565" LINK="#444494" ALINK="#a99999" VLINK="#444494">
<font size=2>
<a href="https://delight.kakiko.org/" target="_top">無料レンタル掲示板</a><br>
<a href="https://delight.kakiko.org/what.html">無料レンタル掲示板とは</a><br>
<a href="/join/"><B>掲示板を作る</B></a><br>
<a href="/menu/"><B>BBSMENU</B></a><br>
<a href="https://delight.kakiko.org/yakusoku.html"><B>【お約束】</B></a><br>
<a href="/find/">本文検索</a><br>
<form method="GET" action="/search/" accept-charset="Shift_JIS" style="margin:0;"><input type="text" name="q" style="width: 80px;"><br><button type="submit">スレタイ検索</button></form>
<? 
$file = $BBSSERV.'etc5.cgi';
if (is_file($file)) {
	echo "<br><br><B>案内</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}
$file = $BBSSERV.'eq.cgi';
if (is_file($file)) {
	echo "<br><br><B>地震</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}
$file = $BBSSERV.'news.cgi';
if (is_file($file)) {
	echo "<br><br><B>ニュース</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";} 
$file = $BBSSERV.'world.cgi';
if (is_file($file)) {
	echo "<br><br><B>世界情勢</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}
$file = $BBSSERV.'etc.cgi';
if (is_file($file)) {
	echo "<br><br><B>馴れ合い</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}
$file = $BBSSERV.'AA.cgi';
if (is_file($file)) {
	echo "<br><br><B>AA</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'society.cgi';
if (is_file($file)) {
	echo "<br><br><B>社会</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
	echo "\n";
}

$file = $BBSSERV.'company.cgi';
if (is_file($file)) {
	echo "<br><br><B>会社職業</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'tmp.cgi';
if (is_file($file)) {
	echo "<br><br><B>裏社会</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'culture.cgi';
if (is_file($file)) {
	echo "<br><br><B>文化</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'culture.cgi';
if (is_file($file)) {
	echo "<br><br><B>学問理系</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'science.cgi';
if (is_file($file)) {
	echo "<br><br><B>学問文系</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'electronics.cgi';
if (is_file($file)) {
	echo "<br><br><B>家電製品</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'economy.cgi';
if (is_file($file)) {
	echo "<br><br><B>政治経済</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'food.cgi';
if (is_file($file)) {
	echo "<br><br><B>食文化</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'life.cgi';
if (is_file($file)) {
	echo "<br><br><B>生活</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'etc1.cgi';
if (is_file($file)) {
	echo "<br><br><B>ネタ雑談</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'etc2.cgi';
if (is_file($file)) {
	echo "<br><br><B>カテゴリ雑談</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'school.cgi';
if (is_file($file)) {
	echo "<br><br><B>受験学校</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'hobby.cgi';
if (is_file($file)) {
	echo "<br><br><B>趣味</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'sports.cgi';
if (is_file($file)) {
	echo "<br><br><B>スポーツ一般</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'ball.cgi';
if (is_file($file)) {
	echo "<br><br><B>球技</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'combative.cgi';
if (is_file($file)) {
	echo "<br><br><B>格闘技</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'travel.cgi';
if (is_file($file)) {
	echo "<br><br><B>旅行外出</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'tv.cgi';
if (is_file($file)) {
	echo "<br><br><B>テレビ等</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'Enter.cgi';
if (is_file($file)) {
	echo "<br><br><B>芸能</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'gamble.cgi';
if (is_file($file)) {
	echo "<br><br><B>ギャンブル</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'game.cgi';
if (is_file($file)) {
	echo "<br><br><B>ゲーム</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'netgame.cgi';
if (is_file($file)) {
	echo "<br><br><B>ネットゲーム</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'comic.cgi';
if (is_file($file)) {
	echo "<br><br><B>漫画小説等</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'music.cgi';
if (is_file($file)) {
	echo "<br><br><B>音楽</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'love.cgi';
if (is_file($file)) {
	echo "<br><br><B>心と身体</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'pc.cgi';
if (is_file($file)) {
	echo "<br><br><B>ＰＣ等</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'net.cgi';
if (is_file($file)) {
	echo "<br><br><B>ネット関係</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'etc3.cgi';
if (is_file($file)) {
	echo "<br><br><B>雑談系２</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'live.cgi';
if (is_file($file)) {
	echo "<br><br><B>実況ch</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'mati.cgi';
if (is_file($file)) {
	echo "<br><br><B>地域</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'etc8.cgi';
if (is_file($file)) {
	echo "<br><br><B>大使館</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'anarchy.cgi';
if (is_file($file)) {
	echo "<br><br><B>荒野</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}

$file = $BBSSERV.'etc4.cgi';
if (is_file($file)) {
	echo "<br><br><B>隔離</B>";
	$str = file($file);
	foreach ($str as $tmp){
		echo "<br>\n";
		$tmp = trim($tmp);
		list ($dir, $name) = explode("<>", $tmp);
		echo "<A HREF=https://$_SERVER[HTTP_HOST]/$dir/>$name</A>";
	}
echo "\n";}
?><br><br><B>他のサイト</B><br>
<a href="https://www2.5ch.net/5ch.html">
『５ちゃんねる』板一覧</a><br>
<a href="https://www.bbspink.com/">
PINKちゃんねる</a><br><BR><HR size="1">
</BODY>
</HTML>