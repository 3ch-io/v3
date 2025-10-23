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
if ($_SERVER['REQUEST_METHOD'] != 'GET') exit;
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
	if (!$bbs) notfound();
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
$BBSSERV = "/virtual/banana356s/public_html/".$_SERVER['HTTP_HOST']."/";	#格納鯖のパス
preg_match("/(.*)(\/test\/read\.cgi)(.*)/", $_SERVER['SCRIPT_NAME'], $match);
$URL = 'https://'.$_SERVER['HTTP_HOST'].$match[1];
$SCRIPT = $match[2];
$BASEURL = "$URL/$bbs/";
if(!file_exists($BBSSERV.$bbs."/")) notfound();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/")) notfound();
if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/")) notfound();
#スレッドの場所
$thread_file = $BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi";
if (!is_file($thread_file)) notfound();
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
	if ($num == "saku") notfound();
	if ($num == "del" || strpos($num, "del") !== false) {
		$subject='削除済み';
	}
#スレッド設定をSETTINGに反映
$SETT = unserialize($threadinfo);
foreach ($SETT as $keys => $value) $SETTING[$keys] = $value;
if (!$SETTING[DELETED_TEXT]) $SETTING[DELETED_TEXT] = "この投稿は削除されました。";
#==================================================
#　出力
#==================================================
$i = 0;
$ncolor = '';
if (!$st) $st = $s;
if (!$to) $to = $LINENUM;
while ($s <= $END) {
	$ncolor = '';
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
	$message = str_replace('<img src="https://', '<img src="//', $message);
	$message = str_replace('<img src="http://', '<img src="//', $message);
	$message = str_replace('<a href="https://', '<a href="//', $message);
	$message = str_replace('<a href="http://', '<a href="//', $message);
	$message = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $message);
	$message = preg_replace_callback('/https?:([a-zA-z0-9\/\._\-&\?#=%]+)/', function ($m) {
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
	}elseif(preg_match('/https?/', $url) and preg_match('/rentalbbs\.net/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" rel=\"nofollow noopener\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }
	}, $message);
	$message = str_replace('<img src="//', '<img src="https://', $message);
	$message = str_replace(' rel="nofollow noopener" target="_blank" title="//', ' rel="nofollow noopener" target="_blank" title="https://', $message);
	$message = str_replace("<br>", " <br> ", $message);
	$message = preg_replace("/sssp:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<img class=\"image img-$s\" src=\"https://$1\">", $message);
#レスアンカーをリンクに変換
$message = preg_replace_callback('/&gt;&gt;([0-9]+),?([0-9]+)?,?([0-9]+)?,?([0-9]+)?,?([0-9]+)?(?![-\d])/', function ($m) {
	global $s,$bbs,$key;
	$anka = "<a class=\"ank rep-$s\" href=\"/test/read.html/$bbs/$key/$m[1]\">&gt;&gt;$m[1]</a>";
	if ($m[2]) $anka .= ",<a class=\"ank rep-$s\" href=\"/test/read.html/$bbs/$key/$m[2]\">&gt;&gt;$m[2]</a>";
	if ($m[3]) $anka .= ",<a class=\"ank rep-$s\" href=\"/test/read.html/$bbs/$key/$m[3]\">&gt;&gt;$m[3]</a>";
	if ($m[4]) $anka .= ",<a class=\"ank rep-$s\" href=\"/test/read.html/$bbs/$key/$m[4]\">&gt;&gt;$m[4]</a>";
	if ($m[5]) $anka .= ",<a class=\"ank rep-$s\" href=\"/test/read.html/$bbs/$key/$m[5]\">&gt;&gt;$m[5]</a>";
	return $anka;
	}, $message);
$message = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	global $s;
	return "<a href=\"javascript:ResAnchor2('$m[1],$m[2],$s');\" class=\"ank2 rep-".$s."\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $message);
	$mailto = $mail ? "<a href=\"mailto:$mail\"><b>$name</b></a>" : "<b>$name</b>";
	# 名前の色
	if (!$SETTING['BBS_NAME_COLOR']) $SETTING['BBS_NAME_COLOR'] = "#008800";
	if (strpos($DATE, "02/14") !== false) $ncolor = "#785f01";	#バレンタインデー
	elseif (!$ncolor) $ncolor = $SETTING['BBS_NAME_COLOR'];
	# レス出力
	echo "<div class=\"post\" id=\"$s\" data-date=\"NG\" data-userid=\"$id\" data-id=\"$s\"".$n."><div id=\"name-$s\" style=\"color: $ncolor;\">$mailto</div><div id=\"date-$s\">$DATE $id</div><div class=\"message\" id=\"msg-$s\">$message</div></div>\n";
	$s++;
}
 exit;
?>