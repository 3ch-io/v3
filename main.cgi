<?php
header("Accept-CH: Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Mobile, Sec-CH-UA-Model, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version");
# read.cgi/read.html
if ($bbs == 'test' and $subbbs == 'read.cgi') {
require $BBSSERV.'read.cgi';
exit;
}
if ($bbs == 'test' and $subbbs == 'read.html') {
require $BBSSERV.'read.cgi';
exit;
}
# BBS.CGI
if ($bbs == 'test' and strpos($subbbs, 'bbs.cgi') !== false) {
require $BBSSERV.'bbs.cgi';
}
# メニュー
if ($bbs == 'menu') {
header("Content-type: text/html; charset=Shift_JIS");
require $BBSSERV.'bbsmenu.cgi';
exit;
}
# 削除CGI
if ($bbs == 'test' and $subbbs == 'delete.cgi') {
require $BBSSERV.'delete.cgi';
exit;
}
# 掲示板作成処理
if ($bbs == 'join') {
header("Content-type: text/html; charset=Shift_JIS");
exit(file_get_contents($BBSSERV.'join.html'));
}
# 掲示板作成処理
if ($bbs == 'make') {
header("Content-type: text/html; charset=Shift_JIS");
if ($_POST[agree] != "on") exit("ルールに同意してください");
if (!$_POST[BBS_TITLE]) exit("掲示板名が記入されていません");
if (!$_POST[USER_MAIL]) exit("管理人メールアドレスが記入されていません");
if (!$_POST[PASSWORD]) exit("パスワードが記入されていません");
if (!$_POST[directory]) exit("ディレクトリ名が記入されていません");
if (strlen($_POST[directory]) < 2 or strlen($_POST[directory]) > 16) exit("ディレクトリ名は2文字以上16文字以下で記入して下さい");
if ($_POST[directory] == "test" or $_POST[directory] == "tmp" or $_POST[directory] == "admin" or $_POST[directory] == "join" or $_POST[directory] == "menu" or $_POST[directory] == "images" or $_POST[directory] == "hashtag") exit("このディレクトリ名は使えません");
if (preg_match("/[^a-z0-9]/", $_POST[directory])) exit("ディレクトリ名には半角英数小文字のみ使用できます");
if ($_POST[UI_STYLE] == "simple") $ui = "BBS_TITLE_PICTURE=\nBBS_TITLE_LINK=\nBBS_BG_COLOR=#FFF\nBBS_MAKETHREAD_COLOR=#FFF\nBBS_BG_PICTURE=\nBBS_NONAME_NAME=\nBBS_MENU_COLOR=#FFF\nBBS_THREAD_COLOR=#FFF\nBBS_TEXT_COLOR=#333\nBBS_NAME_COLOR=#333\nBBS_LINK_COLOR=#0000CC\nBBS_ALINK_COLOR=#FF0000\nBBS_VLINK_COLOR=#AA0088\nDELETED_TEXT=この投稿は削除されました。";
elseif ($_POST[UI_STYLE] == "2ch") $ui = "BBS_TITLE_PICTURE=../2ch.gif\nBBS_TITLE_LINK=https://delight.rentalbbs.net/\nBBS_BG_COLOR=#FFFFFF\nBBS_MAKETHREAD_COLOR=#CCFFCC\nBBS_BG_PICTURE=../ba.gif\nBBS_NONAME_NAME=名無しさん\nBBS_MENU_COLOR=#CCFFCC\nBBS_THREAD_COLOR=#EFEFEF\nBBS_TEXT_COLOR=#000000\nBBS_NAME_COLOR=green\nBBS_LINK_COLOR=#0000FF\nBBS_ALINK_COLOR=#FF0000\nBBS_VLINK_COLOR=#660099\nDELETED_TEXT=あぼーん";

$SETTINGTEXT = "BBS_TITLE=".$_POST[BBS_TITLE]."\n".$ui."\nBBS_THREAD_NUMBER=10\nBBS_CONTENTS_NUMBER=10\nBBS_LINE_NUMBER=15\nBBS_SUBJECT_COLOR=#006699\nBBS_PASSWORD_CHECK=\nBBS_UNICODE=checked\nBBS_SUBJECT_COUNT=128\nBBS_NAME_COUNT=64\nBBS_MAIL_COUNT=64\nBBS_MESSAGE_COUNT=2048\nBBS_THREAD_TATESUGI=8\nTHREAD_JUNBAN=32\nTHREAD_INTERVAL=600\nNANASHI_CHECK=\ntimeinterval=10\ntimecount=120\ntimeclose=30\ntimecover=20\nMAX_RES=1000\nBBS_PROXY_CHECK=checked\nBBS_RAWIP_CHECK=\nBBS_SLIP=feature\nBBS_DISP_IP=\nBBS_FORCE_ID=checked\nBBS_NO_ID=\nBBS_JP_CHECK=\nBBS_FOREIGN_PASS=\nBBS_BBX_PASS=\nBBS_HEISA=\nBBS_FORCE_NONAME=\nBBS_DISABLE_NUSI=checked\nBBS_DISABLE_NO=\nBBS_NO_MADAKANA=\nBBS_SOKO=\nBBS_FR_LEVEL=8\nBBS_FR_SECOND=15\nBBS_THREAD_QUANTITY=\nTIME_TO_LIVE=\nBBS_TH_LINE=\nBBS_MAX_MODIFIED=\nBBS_THREAD_LIFETIME=\nBBS_FORCE_SAGE=\nBBS_DUPLICATE=86400\nTHREAD_CHECK=\nBBS_USE_VIPQ2=extend\nJAPANESE_CHECK=checked\nUse_Account=checked\nUse_Banned=checked\ncheck_useragent=checked\nUse_WrtAgreementkey=checked\nmakethread_rangecheck=checked\nchange_sakujyo=checked\naa_check=checked\nRESET_POSTCOUNT=day\nUI_STYLE=".$_POST[UI_STYLE]."\nADMIN_MAIL=".$_POST[USER_MAIL];
$PATH = $BBSSERV.$_POST[directory]."/";
@mkdir($PATH, 0755);
@touch($PATH."subject.txt");
#設定ファイルを読む
$set_file = $PATH."SETTING.TXT";
if (is_file($set_file)) exit("このディレクトリ名は既に使用されています");
file_put_contents($set_file, $SETTINGTEXT);
#パスワードを設定
file_put_contents($PATH."pass.cgi", $_POST[PASSWORD]);
#カテゴリ一覧に追加
if ($_POST[hide] != "on") {
$fp = fopen($BBSSERV.$_POST[USER_COMMUNITY].".cgi", "a");	#ログを開く
fputs($fp, $_POST[directory]."<>".$_POST[BBS_TITLE]."\n");	#書き込み
fclose($fp);
}
#ログ
file_put_contents($PATH."log.cgi", $_SERVER['REMOTE_ADDR']."<>".$_SERVER['REMOTE_PORT']."<>".$_SERVER[HTTP_USER_AGENT]);
#板へ飛ばす
header('Location: https://'.$_SERVER[HTTP_HOST].'/'.$_POST[directory].'/index.html');
exit;
}
# 管理画面
if ($bbs == 'test' and $subbbs == 'admin.cgi') { 
header("Content-type: text/html; charset=Shift_JIS");
if (!$_POST[pass]) exit("パスワードがありません");
if (!$_POST[bbs]) exit("板が指定されていません");
$PATH = $BBSSERV.$_POST[bbs]."/";
$password = file_get_contents($PATH."pass.cgi");
#設定ファイルを読む
$set_file = $PATH . "SETTING.TXT";
if (is_file($set_file)) {
	$set_str = file($set_file);
	foreach ($set_str as $tmp){
		$tmp = trim($tmp);
		list ($name, $value) = explode("=", $tmp);
		$SETTING[$name] = $value;
	}
}
$text = implode('', file($PATH."head.txt"));
$text2 = implode('', file($PATH."kokuti.txt"));
$aku = implode('', file($PATH."madakana.cgi"));
$deny = implode('', file($PATH."denylist.cgi"));
$rock = implode('', file($PATH."rock54.cgi"));
$cap = implode('', file($PATH."cap.cgi"));
$maxmsg = implode('', file($PATH."1000.txt"));
$maxmsg = str_replace("<br>", "\n", $maxmsg);
if ($_POST[pass] != $password) exit("パスワードが一致しません"); ?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>管理画面</title><link href="https://delight.rentalbbs.net/css/a.css" rel="stylesheet" type="text/css"><style>textarea{max-width:100%;}hr{border:0;border-bottom:.5px solid #DCDCDC;margin:.5em;}</style></head><body><form method="post" action="/test/kanri2.cgi"><input type="hidden" name="bbs" value="<?=$_POST[bbs]?>"><input type="hidden" name="PASSWORD" value="<?=$_POST[pass]?>"><span><div><span><div><div><span><div width="650" cellspacing="1" cellpadding="0" border="1"><span><div><div nowrap=""><b>掲示板管理画面</b><div cellspacing="0" cellpadding="0" border="0"><span><div><div nowrap=""></div><td></div></div><div><div></div></div></span></div><br><div><div width="640" cellspacing="0" cellpadding="0" border="0"><span><div><div width="300" valign="top"><div width="300" cellspacing="0" cellpadding="0" border="0"><span><div><div><span><div bgcolor="#E0FFE0"><div><input type="submit" name="subject" class="btn btn-primary btn-lg btn-block" value="スレッド一覧を直接編集"></div><hr><div><input type="submit" name="errorlog" class="btn btn-primary btn-lg btn-block" value="直近のエラーログを閲覧"></div><hr><div colspan="2"><span><input type="submit" name="Submit" class="btn btn-primary btn-lg btn-block" value="適用"></span></div><hr><div bgcolor="#CCFFCC"><div><b>連絡先Email</b></div><div><input type="email" name="ADMIN_MAIL" value="<?=$SETTING[ADMIN_MAIL]?>"></div></div><div valign="top" bgcolor="#E0FFE0"><div><b>パスワード</b></div><div width="150" valign="middle"><div><input type="text" name="PASS" value="<?=$_POST[pass]?>"></div></div></div><hr><div><div><b>掲示板タイトル</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_TITLE" value="<?=$SETTING[BBS_TITLE]?>"></div></div></div><div><div><b>タイトル画像</b><small class="notice mt5">(空欄の場合は非表示)</small></div><div width="150" valign="middle"><div><input type="text" name="BBS_TITLE_PICTURE" value="<?=$SETTING[BBS_TITLE_PICTURE]?>"></div></div></div><div><div><b>背景画像</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_BG_PICTURE" value="<?=$SETTING[BBS_BG_PICTURE]?>"></div></div></div><div><div><b>ホームページURL</b>(タイトル画像のリンク)</div><div width="150" valign="middle"><div><input type="text" name="BBS_TITLE_LINK" value="<?=$SETTING[BBS_TITLE_LINK]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>名前未入力時の名前</b><small class="notice mt5">(省略可)</small></div><div width="150" valign="middle"><div><input type="text" name="BBS_NONAME_NAME" value="<?=$SETTING[BBS_NONAME_NAME]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>削除された投稿に表示される内容</b><small class="notice mt5">(省略可)</small></div><div width="150" valign="middle"><div><input type="text" name="DELETED_TEXT" value="<?=$SETTING[DELETED_TEXT]?>"></div></div></div><div bgcolor="#FFEDDD"><div><b>背景色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_BG_COLOR" value="<?=$SETTING[BBS_BG_COLOR]?>"></div></div></div><div bgcolor="#FFEDDD"><div><b>新規スレッド背景色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_MAKETHREAD_COLOR" value="<?=$SETTING[BBS_MAKETHREAD_COLOR]?>"></div></div></div><div bgcolor="#FFEDDD"><div><b>メニュー背景色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_MENU_COLOR" value="<?=$SETTING[BBS_MENU_COLOR]?>"></div></div></div><div bgcolor="#FFEDDD"><div><b>スレッド背景色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_THREAD_COLOR" value="<?=$SETTING[BBS_THREAD_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>スレッドタイトルの標準色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_SUBJECT_COLOR" value="<?=$SETTING[BBS_SUBJECT_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>テキストの標準色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_TEXT_COLOR" value="<?=$SETTING[BBS_TEXT_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>名前の色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_NAME_COLOR" value="<?=$SETTING[BBS_NAME_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>リンクの標準色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_LINK_COLOR" value="<?=$SETTING[BBS_LINK_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>選択中のリンク色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_ALINK_COLOR" value="<?=$SETTING[BBS_ALINK_COLOR]?>"></div></div></div><div bgcolor="#E0E5FF"><div><b>訪問済みのリンク色</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_VLINK_COLOR" value="<?=$SETTING[BBS_VLINK_COLOR]?>"></div></div></div><hr><div bgcolor="#CCCCCC"><div><b>サードパーティー製アプリ</b>(外部アプリ)</div><div width="150" valign="middle"><input type="radio" name="third_party_apps_post" value="" <? if ($SETTING[third_party_apps_post]=="") echo "checked"; ?>>閲覧を許可<br><input type="radio" name="third_party_apps_post" value="enable" <? if ($SETTING[third_party_apps_post]=="enable") echo "checked"; ?>>閲覧・投稿を許可<br></div></div><div bgcolor="#CCCCCC"><div><b>UNICODE</b>(絵文字等)</div><div width="150" valign="middle"><input type="radio" name="BBS_UNICODE" value="deny" <? if ($SETTING[BBS_UNICODE]=="deny") echo "checked"; ?>>拒否する<br><input type="radio" name="BBS_UNICODE" value="change" <? if ($SETTING[BBS_UNICODE]=="change") echo "checked"; ?>>？に変換<br><input type="radio" name="BBS_UNICODE" value="pass" <? if ($SETTING[BBS_UNICODE]=="pass") echo "checked"; ?>>タイトルのみ？に変換<br><input type="radio" name="BBS_UNICODE" value="checked" <? if ($SETTING[BBS_UNICODE]=="checked") echo "checked"; ?>>許可する</div></div><div bgcolor="#CCCCCC"><div><b>連投規制類</b><span class="notice mt5">(指定した値によって適用される連投規制が変わります。</div><small>指定できる値一覧(初期値:<b>8</b>)<br><b>off</b>：無効<br><b>0</b>：+短時間投稿規制<br><b>1</b>：+連続投稿規制<br><b>2</b>：+マルチポスト規制<br><b>4</b>：+広域連投規制<br><b>8</b>：+新規連投規制</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_FR_LEVEL]?>" name="BBS_FR_LEVEL"></div></div></div><div bgcolor="#CCCCCC"><div><b>短時間投稿規制秒数</b></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_FR_SECOND]?>" name="BBS_FR_SECOND"></div></div></div><div bgcolor="#CCCCCC"><div><b>各スレッド内でのレス間隔制限秒数</b><small class="notice mt5">(他者の投稿を含む)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[timeinterval]?>" name="timeinterval"></div></div></div><div bgcolor="#CCCCCC"><div><b>掲示板全体の連続投稿規制</b></div><div width="150" valign="middle"><div><input type="text" name="timecount" value="<?=$SETTING[timecount]?>">回中<input type="text" name="timeclose" value="<?=$SETTING[timeclose]?>">回以上で規制</div></div></div><div bgcolor="#CCCCCC"><div><b>各スレッド内での連続投稿規制</b></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[timecover]?>" name="timecover"></div></div></div><div bgcolor="#CCCCCC"><div><b>１ページ中のスレッド数</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_THREAD_NUMBER" value="<?=$SETTING[BBS_THREAD_NUMBER]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>PC版の掲示板トップ画面で1スレッド内にに掲載する投稿数</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_CONTENTS_NUMBER" value="<?=$SETTING[BBS_CONTENTS_NUMBER]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>投稿行数制限</b><small class="notice mt5">(ログインユーザーはこの値の3倍値・未ログインユーザーはこの値の2倍値を適用)</small></div><div width="150" valign="middle"><div><input type="text" name="BBS_LINE_NUMBER" value="<?=$SETTING[BBS_LINE_NUMBER]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>スレッドタイトルの文字数制限</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_SUBJECT_COUNT" value="<?=$SETTING[BBS_SUBJECT_COUNT]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>名前の文字数制限</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_NAME_COUNT" value="<?=$SETTING[BBS_NAME_COUNT]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>メールの文字数制限</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_MAIL_COUNT" value="<?=$SETTING[BBS_MAIL_COUNT]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>本文の文字数制限</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_MESSAGE_COUNT" value="<?=$SETTING[BBS_MESSAGE_COUNT]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>同一IP群からのスレッド作成規制数</b></div><div width="150" valign="middle"><div><input type="text" name="BBS_THREAD_TATESUGI" value="<?=$SETTING[BBS_THREAD_TATESUGI]?>"></div></div></div><div bgcolor="#CCCCCC"><div><b>広域スレッド作成規制数</b></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[THREAD_JUNBAN]?>" name="THREAD_JUNBAN"></div></div></div><div bgcolor="#CCCCCC"><div><b>スレッド作成間隔制限秒数</b><small class="notice mt5">(他者のスレ立てを含む)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[THREAD_INTERVAL]?>" name="THREAD_INTERVAL"></div></div></div><div bgcolor="#CCCCCC"><div><b>各スレッドのレス数上限</b><span class="notice mt5">(300～2000)</span></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[MAX_RES]?>" name="MAX_RES"></div></div></div><div bgcolor="#CCCCCC"><div><b>現行スレッド保持数</b><small class="notice mt5">(保持数を超えた場合は最終更新時刻の古い順に過去ログ化します)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_THREAD_QUANTITY]?>" name="BBS_THREAD_QUANTITY"></div></div></div><div bgcolor="#CCCCCC"><div><b>過去ログ化判定秒数</b><small class="notice mt5">(指定秒数後に&lt;過去ログ化判定投稿数&gt;以上投稿のないスレッドは過去ログ化)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[TIME_TO_LIVE]?>" name="TIME_TO_LIVE"></div></div></div><div bgcolor="#CCCCCC"><div><b>過去ログ化判定投稿数</b><small class="notice mt5">(&lt;過去ログ化判定秒数&gt;後に指定レス以上投稿のないスレッドは過去ログ化)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_TH_LINE]?>" name="BBS_TH_LINE"></div></div></div><div bgcolor="#CCCCCC"><div><b>スレッド継続最低秒数</b><small class="notice mt5">(指定秒数更新のないスレッドは過去ログ化)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_MAX_MODIFIED]?>" name="BBS_MAX_MODIFIED"></div></div></div><div bgcolor="#CCCCCC"><div><b>スレッドの有効秒数</b><small class="notice mt5">(最終更新時刻にかかわらず、この秒数を過ぎると強制的に過去ログ化します。空欄で無効化)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_THREAD_LIFETIME]?>" name="BBS_THREAD_LIFETIME"></div></div></div><div bgcolor="#CCCCCC"><div><b>強制sageまでの秒数</b></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_FORCE_SAGE]?>" name="BBS_FORCE_SAGE"></div></div></div><div bgcolor="#CCCCCC"><div><b>同一タイトルでのスレ立てを規制する秒数</b><small class="notice mt5">(offで無効化)</small></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_DUPLICATE]?>" name="BBS_DUPLICATE"></div></div></div><div bgcolor="#CCCCCC"><div><b>連投規制類がリセットされるまでの時間</b></div><div width="150" valign="middle"><div><input type="radio" name="RESET_POSTCOUNT" value="day"<? if ($SETTING[RESET_POSTCOUNT]=="day") echo " checked"; ?>>1日<input type="radio" name="RESET_POSTCOUNT" value="10days"<? if ($SETTING[RESET_POSTCOUNT]=="10days") echo " checked"; ?>>10日<br><input type="radio" name="RESET_POSTCOUNT" value="10hours"<? if ($SETTING[RESET_POSTCOUNT]=="10hours") echo " checked"; ?>>10時間<input type="radio" name="RESET_POSTCOUNT" value="month"<? if ($SETTING[RESET_POSTCOUNT]=="month") echo " checked"; ?>>1ヶ月<br><input type="radio" name="RESET_POSTCOUNT" value="hour"<? if ($SETTING[RESET_POSTCOUNT]=="hour") echo " checked"; ?>>1時間<input type="radio" name="RESET_POSTCOUNT" value="10minutes"<? if ($SETTING[RESET_POSTCOUNT]=="10minutes") echo " checked"; ?>>10分<br><input type="radio" name="RESET_POSTCOUNT" value="year"<? if ($SETTING[RESET_POSTCOUNT]=="year") echo " checked"; ?>>1年<small>(非推奨)</small><br><input type="radio" name="RESET_POSTCOUNT" value="minute"<? if ($SETTING[RESET_POSTCOUNT]=="minute") echo " checked"; ?>>1分<small>(非推奨)</small><br></div></div></div><div bgcolor="#CCCCCC"><div><b>UIスタイル</b></div><div width="150" valign="middle"><div><input type="radio" name="UI_STYLE" value="simple"<? if ($SETTING[UI_STYLE]=="simple") echo " checked"; ?>>シンプル<input type="radio" name="UI_STYLE" value="2ch"<? if ($SETTING[UI_STYLE]=="2ch") echo " checked"; ?>>2ch形式</div></div></div><div bgcolor="#CCCCCC"><div><b>IDの方式</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_SLIP" value="feature" <? if ($SETTING[BBS_SLIP]=="feature") echo "checked"; ?>>新方式：<small>一般回線:ID10桁/モバイル:ID16桁</small><br><input type="radio" name="BBS_SLIP" value="" <? if (!$SETTING[BBS_SLIP]) echo "checked"; ?>>旧方式：<small>ID8桁</small><br><input type="radio" name="BBS_SLIP" value="short" <? if (!$SETTING[BBS_SLIP]) echo "checked"; ?>>短縮表示：<small>ID4桁</small><br><input type="radio" name="BBS_SLIP" value="verbose" <? if ($SETTING[BBS_SLIP]=="verbose") echo "checked"; ?>>ID16桁<input type="radio" name="BBS_SLIP" value="checked" <? if ($SETTING[BBS_SLIP]=="checked") echo "checked"; ?>><a href="https://info.5ch.net/index.php/BBS_SLIP#.E6.96.B0.E6.96.B9.E5.BC.8F.E3.81.A7.E3.81.AE_ID.E6.9C.AB.E5.B0.BE.E8.A1.A8.E7.A4.BA_.E3.81.A8_.E5.90.8D.E5.89.8D.E6.AC.84.E5.86.85.E3.83.8B.E3.83.83.E3.82.AF.E3.83.8D.E3.83.BC.E3.83.A0.E8.A1.A8.E7.A4.BA" target="_blank">ID9桁</a><br><small class="notice mt5">以下全て新方式</small><br><input type="radio" name="BBS_SLIP" value="vvvvv" <? if ($SETTING[BBS_SLIP]=="vvvvv") echo "checked"; ?>><a href="https://info.5ch.net/index.php/BBS_SLIP#KOROKORO" target="_blank">KOROKORO</a><br><input type="radio" name="BBS_SLIP" value="vvvvvv" <? if ($SETTING[BBS_SLIP]=="vvvvvv") echo "checked"; ?>><a href="https://info.5ch.net/index.php/BBS_SLIP#KOROKORO" target="_blank">KOROKORO</a>+IPアドレス</a><br><input type="radio" name="BBS_SLIP" value="vvvv" <? if ($SETTING[BBS_SLIP]=="vvvv") echo "checked"; ?>>IPアドレス<br><input type="radio" name="BBS_SLIP" value="vvv" <? if ($SETTING[BBS_SLIP]=="vvv") echo "checked"; ?>>妙なニックネーム<br></div></div></div><div bgcolor="#CCCCCC"><div><b>発信元表示</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_DISP_IP" value="siberia" <? if ($SETTING[BBS_DISP_IP]=="siberia") echo "checked"; ?>>IPアドレスを表示<br><input type="radio" name="BBS_DISP_IP" value="feature" <? if ($SETTING[BBS_DISP_IP]=="feature") echo "checked"; ?>>IPアドレスの一部を表示<br><input type="radio" name="BBS_DISP_IP" value="checked" <? if ($SETTING[BBS_DISP_IP]=="checked") echo "checked"; ?>>リモートホストを表示<br><input type="radio" name="BBS_DISP_IP" value="browser" <? if ($SETTING[BBS_DISP_IP]=="browser") echo "checked"; ?>>発信元ブラウザ名を表示<br><input type="radio" name="BBS_DISP_IP" value="" <? if (!$SETTING[BBS_DISP_IP]) echo "checked"; ?>>しない<br></div></div></div><div bgcolor="#CCCCCC"><div><b>県名・回線表示</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_JP_CHECK" value="1" <? if ($SETTING[BBS_JP_CHECK]==1) echo "checked"; ?>>県名<input type="radio" name="BBS_JP_CHECK" value="2" <? if ($SETTING[BBS_JP_CHECK]==2) echo "checked"; ?>>市・町<br><input type="radio" name="BBS_JP_CHECK" value="3" <? if ($SETTING[BBS_JP_CHECK]==3) echo "checked"; ?>>県+市・町<br><input type="radio" name="BBS_JP_CHECK" value="4" <? if ($SETTING[BBS_JP_CHECK]==4) echo "checked"; ?>>ISP名<br><input type="radio" name="BBS_JP_CHECK" value="5" <? if ($SETTING[BBS_JP_CHECK]==5) echo "checked"; ?>>県名+ISP名<br><input type="radio" name="BBS_JP_CHECK" value="6" <? if ($SETTING[BBS_JP_CHECK]==6) echo "checked"; ?>>県+市・町+ISP名<br><input type="radio" name="BBS_JP_CHECK" value="checked" <? if ($SETTING[BBS_JP_CHECK]=="checked") echo "checked"; ?>>簡易表示<br><input type="radio" name="BBS_JP_CHECK" value="" <? if (!$SETTING[BBS_JP_CHECK]) echo "checked"; ?>>しない<br></div></div></div><div bgcolor="#CCCCCC"><div><b>個別規制</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_NO_MADAKANA" value="on" <? if ($SETTING[BBS_NO_MADAKANA]=="on") echo "checked"; ?>>しない<small>(リモートホスト強制表示)</small><br><input type="radio" name="BBS_NO_MADAKANA" value="" <? if ($SETTING[BBS_NO_MADAKANA]!="on") echo "checked"; ?>>する<br></div></div></div><div bgcolor="#CCCCCC"><div><b>海外ホストからの投稿を禁止</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_FOREIGN_PASS" value="on" <? if ($SETTING[BBS_FOREIGN_PASS]=="on") echo "checked"; ?>>しない<input type="radio" name="BBS_FOREIGN_PASS" value="" <? if ($SETTING[BBS_FOREIGN_PASS]!="on") echo "checked"; ?>>する<br></div></div></div><div bgcolor="#CCCCCC"><div><b>Proxy・荒らしホスト規制</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_BBX_PASS" value="on" <? if ($SETTING[BBS_BBX_PASS]=="on") echo "checked"; ?>>適用しない<br><input type="radio" name="BBS_BBX_PASS" value="" <? if ($SETTING[BBS_BBX_PASS]!="on") echo "checked"; ?>>適用する<br></div></div></div><div bgcolor="#CCCCCC"><div><b>名前を無効化</b><small>(強制的に名前未入力に変換)</small></div><div width="150" valign="middle"><div><input type="radio" name="BBS_FORCE_NONAME" value="yes" <? if ($SETTING[BBS_FORCE_NONAME]=="yes") echo "checked"; ?>>する<input type="radio" name="BBS_FORCE_NONAME" value="" <? if ($SETTING[BBS_FORCE_NONAME]!="yes") echo "checked"; ?>>しない<br></div></div></div><div bgcolor="#CCCCCC"><div><b>BBS_SOKO</b></div><div width="150" valign="middle"><div><input type="text" value="<?=$SETTING[BBS_SOKO]?>" name="BBS_SOKO"></div></div></div><div bgcolor="#CCCCCC"><div><b>投稿時のログインを必須にする</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_BE_ID" value="1"<? if ($SETTING[BBS_BE_ID]=="1") echo " checked"; ?>>する<input type="radio" name="BBS_BE_ID" value=""<? if (!$SETTING[BBS_BE_ID]) echo " checked"; ?>>しない<br></div></div></div><div bgcolor="#CCCCCC"><div><b>連投規制の緩和</b>(実況モード)</div><div width="150" valign="middle"><div><input type="radio" name="LIVE_THREAD" value="1"<? if ($SETTING[LIVE_THREAD]) echo " checked"; ?>>有効<input type="radio" name="LIVE_THREAD" value=""<? if (!$SETTING[LIVE_THREAD]) echo " checked"; ?>>無効<br></div></div></div><div bgcolor="#CCCCCC"><div><b>スレッド作成主機能</b></div><div width="150" valign="middle"><div><input type="radio" name="BBS_DISABLE_NUSI" value=""<? if (!$SETTING[BBS_DISABLE_NUSI]) echo " checked"; ?>>有効<br><input type="radio" name="BBS_DISABLE_NUSI" value="checked"<? if ($SETTING[BBS_DISABLE_NUSI]=="checked") echo " checked"; ?>>無効<br></div></div></div><div bgcolor="#999999"><div><b>各スレッドでの設定変更コマンド類</b></div><div width="150" valign="middle"><div align="left"><input type="radio" name="BBS_USE_VIPQ2" value="checked"<? if ($SETTING[BBS_USE_VIPQ2] == "checked") echo " checked"; ?>>有効<input type="radio" name="BBS_USE_VIPQ2" value="extend"<? if ($SETTING[BBS_USE_VIPQ2] == "extend") echo " checked"; ?>>!extendのみ<br><input type="radio" name="BBS_USE_VIPQ2" value=""<? if (!$SETTING[BBS_USE_VIPQ2]) echo " checked"; ?>>無効</div></div></div><div bgcolor="#999999"><div><b>ログイン機能を有効化</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="Use_Account" value="checked"<? if ($SETTING[Use_Account]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>アカウントBAN、鍵BAN、蛸BANなどを適用</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="Use_Banned" value="checked"<? if ($SETTING[Use_Banned]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>サードパーティー製アプリの偽造検出</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="check_useragent" value="checked"<? if ($SETTING[check_useragent]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>未ログイン時の投稿に識別認証用鍵<small class="notice mt5">(WrtAgreementkey)</small>を使用する</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="Use_WrtAgreementkey" value="checked"<? if ($SETTING[Use_WrtAgreementkey]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b><small>IPアドレスグループ・UserAgentグループ</small>でのスレッド作成制限を適用</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="makethread_rangecheck" value="checked"<? if ($SETTING[makethread_rangecheck]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b><small>名前欄の「管理」「削除」「sakujyo」を「"管理"」等へ変換（なりすまし防止）</small></b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="change_sakujyo" value="checked"<? if ($SETTING[change_sakujyo]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b><small>AAを自動検出し、フォントを最適化</small></b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="aa_check" value="checked"<? if ($SETTING[aa_check]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>投稿時の名前入力</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" name="NANASHI_CHECK" value="checked"<? if ($SETTING[NANASHI_CHECK]=="checked") echo " checked"; ?>>必須</div></div></div><div bgcolor="#999999"><b>常にIDを非表示</b></div><div width="150" valign="middle"><input type="checkbox" name="BBS_NO_ID" value="checked"<? if ($SETTING[BBS_NO_ID]=="checked") echo " checked"; ?>>する</div></div><div bgcolor="#999999"><b>各スレッドごとにIDを割り当てる</b></div><div width="150" valign="middle"><input type="checkbox" value="checked" name="BBS_ID_CHANGE"<? if ($SETTING[BBS_ID_CHANGE]=="checked") echo " checked"; ?>>する</div></div><div bgcolor="#999999"><div><b>1分ごとにIDを割り当てる</b>(IDを60分割)</div><div width="150" valign="middle"><input type="checkbox" name="BBS_DIVID" value="checked"<? if ($SETTING[BBS_DIVID]=="checked") echo " checked"; ?>>する</div></div><div bgcolor="#999999"><div><b>常にIDを表示</b></div><div width="150" valign="middle"><input type="checkbox" name="BBS_FORCE_ID" value="checked"<? if ($SETTING[BBS_FORCE_ID]=="checked") echo " checked"; ?>>する</div></div><div bgcolor="#999999"><div><b>逆引きできないホストからの投稿を禁止</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="BBS_PROXY_CHECK"<? if ($SETTING[BBS_PROXY_CHECK]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>スレ立て時のタイトルに識別用の数字を含める</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="BBS_BE_TYPE2"<? if ($SETTING[BBS_BE_TYPE2]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>スレッド作成をパスワード制にする</b>(記者制度)</div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="BBS_PASSWORD_CHECK"<? if ($SETTING[BBS_PASSWORD_CHECK]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>スレッド作成時のログイン</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="THREAD_CHECK"<? if ($SETTING[THREAD_CHECK]=="checked") echo " checked"; ?>>必須</div></div></div><div bgcolor="#999999"><div><b>AA用の表示形式を使用</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="BBS_AA"<? if ($SETTING[BBS_AA]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>日本語を含まない投稿</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="JAPANESE_CHECK"<? if ($SETTING[JAPANESE_CHECK]=="checked") echo " checked"; ?>>ログイン時のみ許可</div></div></div><div bgcolor="#999999"><div><b>画像の投稿</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="NOPIC"<? if ($SETTING[NOPIC]=="checked") echo " checked"; ?>>禁止</div></div></div><div bgcolor="#999999"><div><b>リンクの投稿</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="DISABLE_LINK"<? if ($SETTING[DISABLE_LINK]=="checked") echo " checked"; ?>>禁止</div></div></div><div bgcolor="#999999"><div><b>アイコンを無効化</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="DISABLE_ICON"<? if ($SETTING[DISABLE_ICON]=="checked") echo " checked"; ?>>する</div></div></div><div bgcolor="#999999"><div><b>掲示板全体の設定を強制</b><small class="notice mt5">(各スレッド内での設定変更を無効化)</small></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="Forced_Setting"<? if ($SETTING[Forced_Setting]=="checked") echo " checked"; ?>>する<br><small class="notice mt5">各スレッドの設定変更コマンドが使用できなくなります</small></div></div></div><div bgcolor="#999999"><div><b>スレッド検索・本文検索・ハッシュタグ欄</b></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="NOINDEX"<? if ($SETTING[NOINDEX]=="checked") echo " checked"; ?>>掲載しない<br><small class="notice mt5">スレッド検索・本文検索が使用できなくなります</small></div></div></div><div bgcolor="#999999"><div><b>一般からの投稿を停止</b><small class="notice mt5">(キャップ使用時のみ投稿を許可)</small></div><div width="150" valign="middle"><div align="left"><input type="checkbox" value="checked" name="BBS_HEISA"<? if ($SETTING[BBS_HEISA]=="checked") echo " checked"; ?>>する</div></div></div></span></div></div></div></span></div></div><hr><div valign="top"><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>ヘッダー</b><br><small class="notice mt5">掲示板TOP画面に表示されます</small></div></div></span></div><textarea style="font-size:9pt" rows="10" cols="70" name="head" wrap="OFF"><?=$text?></textarea></div></div></span></div></div></div></b></div><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>告知欄</b><br><small class="notice mt5">掲示板TOP画面と各スレッド最下部に表示されます</small></div></div></span></div><textarea style="font-size:9pt" rows="10" cols="70" name="head2" wrap="OFF"><?=$text2?></textarea></div></div></span></div></div></div></b></div><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>レスオーバー時のメッセージ</b><br><small class="notice mt5">改行は自動的に反映されます</small></div></div></span></div><textarea style="font-size:9pt" rows="15" cols="70" name="maxres" wrap="OFF"><?=$maxmsg?></textarea></div></div></span></div></div></div></b></div><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>キャップ</b></div></div></span></div><textarea style="font-size:9pt" rows="5" cols="70" name="cap" wrap="OFF"><?=$cap?></textarea><div style="background:white;font-size:9pt;border:2pt outset white"><span><div><div>
<dl>書き方<br>
<dd class="notice mt5">
・&lt;&gt;が区切り文字、<b>名前</b>&lt;&gt;<b>パスワード</b>&lt;&gt;<b>権限</b>&lt;&gt;<b>ID</b><br>
・権限の欄に<b>saku</b>を入れるとそのパスワードでも削除ページに入れるようになります。(副管理人等)<br>
・権限の欄に<b>sakud</b>を入れると名前表示+削除権限のみとなり、ID等も通常表示されます。(削除人等)<br>
・権限の欄に<b>ncmd</b>を入れると名前表示+規制回避のみとなり、ID等も通常表示されます。(規制回避キャップ等)<br>
・権限の欄に<b>plus</b>を入れると名前表示のみ(規制回避・コマンド類)は一切使用できなくなり、ID等も通常表示されます。※ただし<b>スレッド立てをパスワード制にする(記者制度)</b>のみ回避できます。<br>
・パスワード使用時は <b>Email欄</b>に<b>#パスワード</b>の形で記入してください。<br>
・名前欄に記入したものが投稿時の名前として表示されます。。<br>
・ID欄を設定すると<b>@&#60;設定したID&#62;</b>の形式で表示されます。ID欄が無記入の場合は<b>@CAP_USER</b>が表示されます。<br>
・半角の『#』を含んでいる行はコメント行として扱われます。<br>
・キャップの権限については<a href="https://akari.rentalbbs.net/faq/">FAQ</a>に軽くまとめたものがございます。<br>
</dd>
</dl></div></div></span></div></div></div></b></div><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>投稿規制設定</b></div></div></span></div><textarea style="font-size:9pt" rows="15" cols="70" name="aku" wrap="OFF"><?=$aku?></textarea><div style="background:white;font-size:9pt;border:2pt outset white"><span><div><div>
<dl>書き方<br>
<dd class="notice mt5">
・投稿を規制したいIPアドレス・リモートホスト・Key・UA・PHONE・県名や市名・プロバイダ・header情報などをずらずらと書いてください。<br>
・&lt;&gt;が区切り文字、<b>規制対象(リモートホスト等)</b>&lt;&gt;<b>対象スレッド(省略可)</b>&lt;&gt;<b>発動ワード(省略可)</b>の形で記入してください。<br>
・<b>規制対象(リモートホスト等)</b>では<b>&</b>を用いると複数条件で設定できます 例：<b>\.spmode\.ne\.jp&Chrome</b>とすると<b>.spmode.ne.jpかつChromeからの投稿を規制します</b> 現在、<b>&</b>は1行につき1個のみ使用できます<br>
・<b>対象スレッド</b>に記入されている場合はそのワードが含まれているスレッドでのみ規制。無記入の場合は掲示板内の全スレッドが対象。<br>
・<b>発動ワード</b>に記入されている場合はそのワードが含まれている場合のみ規制。特定範囲にのみ適用されるNGワードとお考えください<br>
・1行につき1つの規制です。<br>
・半角の『#』を含んでいる行はコメント行として扱われます。<br>
・正規表現です。特殊な文字にご注意ください。<br>
・掲示板設定の<b>個別規制</b>を<b>しない</b>にすると規制される代わりにリモートホストが強制表示されます。
</dd>
</dl></div></div></span></div></div></div></span></div></div></div></b></div><div width="400" cellspacing="0" cellpadding="0" border="0"><span><div><div><div width="300" cellspacing="0" cellpadding="0" border="1"><span><div style="font-size:9pt" bgcolor="#CCCCCC"></div><div><div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>スレッド作成規制設定</b></div></div></span></div><textarea style="font-size:9pt" rows="10" cols="70" name="deny" wrap="OFF"><?=$deny?></textarea><div style="background:white;font-size:9pt;border:2pt outset white"><span><div><div>
<dl>書き方<br>
<dd class="notice mt5">
・スレッド作成を禁止したいIPアドレス・リモートホスト・Key・UA・PHONE・県名や市名・プロバイダ・header情報などをずらずらと書いてください。<br>
・&lt;&gt;が区切り文字、<b>規制対象(リモートホスト等)</b>&lt;&gt;<b>発動ワード(省略可)</b>の形で記入してください。<br>
・<b>規制対象(リモートホスト等)</b>では<b>&</b>を用いると複数条件で設定できます 例：<b>\.spmode\.ne\.jp&Chrome</b>とすると<b>.spmode.ne.jpかつChromeからの投稿を規制します</b> 現在、<b>&</b>は1行につき1個のみ使用できます<br>
・<b>発動ワード</b>に記入されている場合はそのワードが含まれている場合のみ規制。特定範囲にのみ適用されるNGワードとお考えください<br>
・1行につき1つの規制です。<br>
・半角の『#』を含んでいる行はコメント行として扱われます。<br>
・正規表現です。特殊な文字にご注意ください。<br>
</dd>
</dl></div></div></span></div></div></div></span></div></div></div></span></div><div style="font-size:9pt;background:#FFE0E0;color:#333"><span><div><div><b>NGワード</b></div></div></span></div><textarea style="font-size:9pt" rows="8" cols="70" name="rock" wrap="OFF"><?=$rock?></textarea><div style="background:white;font-size:9pt;border:2pt outset white"><span><div><div>
<dl>書き方<br>
<dd class="notice mt5">
・1行につき1つです。<br>
・半角の『#』を含んでいる行はコメント行として扱われます。<br>
・正規表現です。特殊な文字にご注意ください。<br>
</dd>
</dl></div></div></span></div></div></div></span></div></div></div></span></div></div></div></span></div></span><hr><input type="submit" name="Submit" class="btn btn-primary btn-lg btn-block" value="適用"></body></html><? exit; 
}
# 管理CGI
if ($bbs == 'test' and $subbbs == 'kanri2.cgi') {
header("Content-type: text/html; charset=Shift_JIS");
if (!$_POST[PASS]) exit("パスワードがありません");
if (!$_POST[bbs]) exit("板が指定されていません");
$PATH = $BBSSERV.$_POST[bbs]."/";
$password = file_get_contents($PATH."pass.cgi");
if ($_POST[PASSWORD] != $password) exit("パスワードが一致しません");
#エラーログ閲覧
if (isset($_POST['errorlog'])) {
 require $BBSSERV.'elog.cgi';
 exit;
}
#subject.txt編集
if (isset($_POST['subject'])) {
 require $BBSSERV.'subject.cgi';
 exit;
}
$SETTINGTEXT = "BBS_TITLE=".$_POST[BBS_TITLE]."\nBBS_TITLE_PICTURE=".$_POST[BBS_TITLE_PICTURE]."\nBBS_TITLE_LINK=".$_POST[BBS_TITLE_LINK]."\nBBS_BG_COLOR=".$_POST[BBS_BG_COLOR]."\nBBS_MAKETHREAD_COLOR=".$_POST[BBS_MAKETHREAD_COLOR]."\nBBS_BG_PICTURE=".$_POST[BBS_BG_PICTURE]."\nBBS_NONAME_NAME=".$_POST[BBS_NONAME_NAME]."\nBBS_MENU_COLOR=".$_POST[BBS_MENU_COLOR]."\nBBS_THREAD_COLOR=".$_POST[BBS_THREAD_COLOR]."\nBBS_TEXT_COLOR=".$_POST[BBS_TEXT_COLOR]."\nBBS_NAME_COLOR=".$_POST[BBS_NAME_COLOR]."\nBBS_LINK_COLOR=".$_POST[BBS_LINK_COLOR]."\nBBS_ALINK_COLOR=".$_POST[BBS_ALINK_COLOR]."\nBBS_VLINK_COLOR=".$_POST[BBS_VLINK_COLOR]."\nDELETED_TEXT=".$_POST[DELETED_TEXT]."\nBBS_THREAD_NUMBER=".$_POST[BBS_THREAD_NUMBER]."\nBBS_CONTENTS_NUMBER=".$_POST[BBS_CONTENTS_NUMBER]."\nBBS_LINE_NUMBER=".$_POST[BBS_LINE_NUMBER]."\nBBS_SUBJECT_COLOR=".$_POST[BBS_SUBJECT_COLOR]."\nBBS_PASSWORD_CHECK=".$_POST[BBS_PASSWORD_CHECK]."\nBBS_UNICODE=".$_POST[BBS_UNICODE]."\nBBS_SUBJECT_COUNT=".$_POST[BBS_SUBJECT_COUNT]."\nBBS_NAME_COUNT=".$_POST[BBS_NAME_COUNT]."\nBBS_MAIL_COUNT=".$_POST[BBS_MAIL_COUNT]."\nBBS_MESSAGE_COUNT=".$_POST[BBS_MESSAGE_COUNT]."\nBBS_THREAD_TATESUGI=".$_POST[BBS_THREAD_TATESUGI]."\nTHREAD_JUNBAN=".$_POST[THREAD_JUNBAN]."\nTHREAD_INTERVAL=".$_POST[THREAD_INTERVAL]."\nNANASHI_CHECK=".$_POST[NANASHI_CHECK]."\ntimeinterval=".$_POST[timeinterval]."\ntimecount=".$_POST[timecount]."\ntimeclose=".$_POST[timeclose]."\ntimecover=".$_POST[timecover]."\nMAX_RES=".$_POST[MAX_RES]."\nBBS_PROXY_CHECK=".$_POST[BBS_PROXY_CHECK]."\nBBS_RAWIP_CHECK=".$_POST[BBS_RAWIP_CHECK]."\nBBS_SLIP=".$_POST[BBS_SLIP]."\nBBS_DISP_IP=".$_POST[BBS_DISP_IP]."\nBBS_DIVID=".$_POST[BBS_DIVID]."\nBBS_FORCE_ID=".$_POST[BBS_FORCE_ID]."\nBBS_NO_ID=".$_POST[BBS_NO_ID]."\nBBS_JP_CHECK=".$_POST[BBS_JP_CHECK]."\nBBS_FOREIGN_PASS=".$_POST[BBS_FOREIGN_PASS]."\nBBS_BBX_PASS=".$_POST[BBS_BBX_PASS]."\nBBS_HEISA=".$_POST[BBS_HEISA]."\nBBS_FORCE_NONAME=".$_POST[BBS_FORCE_NONAME]."\nBBS_DISABLE_NUSI=".$_POST[BBS_DISABLE_NUSI]."\nBBS_DISABLE_NO=".$_POST[BBS_DISABLE_NO]."\nBBS_NO_MADAKANA=".$_POST[BBS_NO_MADAKANA]."\nBBS_SOKO=".$_POST[BBS_SOKO]."\nBBS_FR_LEVEL=".$_POST[BBS_FR_LEVEL]."\nBBS_FR_SECOND=".$_POST[BBS_FR_SECOND]."\nBBS_THREAD_QUANTITY=".$_POST[BBS_THREAD_QUANTITY]."\nTIME_TO_LIVE=".$_POST[TIME_TO_LIVE]."\nBBS_TH_LINE=".$_POST[BBS_TH_LINE]."\nBBS_MAX_MODIFIED=".$_POST[BBS_MAX_MODIFIED]."\nBBS_THREAD_LIFETIME=".$_POST[BBS_THREAD_LIFETIME]."\nBBS_FORCE_SAGE=".$_POST[BBS_FORCE_SAGE]."\nBBS_DUPLICATE=".$_POST[BBS_DUPLICATE]."\nBBS_BE_ID=".$_POST[BBS_BE_ID]."\nBBS_BE_TYPE2=".$_POST[BBS_BE_TYPE2]."\nTHREAD_CHECK=".$_POST[THREAD_CHECK]."\nRES_CHECK=".$_POST[RES_CHECK]."\nBBS_USE_VIPQ2=".$_POST[BBS_USE_VIPQ2]."\nJAPANESE_CHECK=".$_POST[JAPANESE_CHECK]."\nLIVE_THREAD=".$_POST[LIVE_THREAD]."\nBBS_ID_CHANGE=".$_POST[BBS_ID_CHANGE]."\nBBS_AA=".$_POST[BBS_AA]."\nNOPIC=".$_POST[NOPIC]."\nDISABLE_LINK=".$_POST[DISABLE_LINK]."\nDISABLE_ICON=".$_POST[DISABLE_ICON]."\nForced_Setting=".$_POST[Forced_Setting]."\nNOINDEX=".$_POST[NOINDEX]."\nUse_Account=".$_POST[Use_Account]."\nUse_Banned=".$_POST[Use_Banned]."\ncheck_useragent=".$_POST[check_useragent]."\nUse_WrtAgreementkey=".$_POST[Use_WrtAgreementkey]."\nmakethread_rangecheck=".$_POST[makethread_rangecheck]."\nchange_sakujyo=".$_POST[change_sakujyo]."\naa_check=".$_POST[aa_check]."\nRESET_POSTCOUNT=".$_POST[RESET_POSTCOUNT]."\nthird_party_apps_post=".$_POST[third_party_apps_post]."\nUI_STYLE=".$_POST[UI_STYLE]."\nADMIN_MAIL=".$_POST[ADMIN_MAIL];
$set_file = $PATH."SETTING.TXT";
$_POST[maxres] = str_replace(array("\r\n","\r","\n"), "<br>", $_POST[maxres]);
file_put_contents($set_file, $SETTINGTEXT);
file_put_contents($PATH."head.txt", $_POST[head]);
file_put_contents($PATH."kokuti.txt", $_POST[head2]);
file_put_contents($PATH."1000.txt", $_POST[maxres]);
file_put_contents($PATH."madakana.cgi", $_POST[aku]);
file_put_contents($PATH."denylist.cgi", $_POST[deny]);
file_put_contents($PATH."rock54.cgi", $_POST[rock]);
file_put_contents($PATH."cap.cgi", $_POST[cap]);
file_put_contents($PATH."pass.cgi", $_POST[PASS]);
header('Location: https://'.$_SERVER[HTTP_HOST].'/'.$_POST[bbs].'/index.html');
exit;
}
$PATH = $BBSSERV.$bbs."/";
$NOWTIME = time();
#設定ファイルを読む
$set_file = $PATH . "SETTING.TXT";
if (is_file($set_file)) {
	$set_str = file($set_file);
	foreach ($set_str as $tmp){
		$tmp = trim($tmp);
		list ($name, $value) = explode("=", $tmp);
		$SETTING[$name] = $value;
	}
}elseif ($bbs != "test" and $bbs != "auth") notfound();
elseif (!$subbbs or $subbbs == "subback" or $subbbs == "index.html") notfound();
$subjectfile = $BBSSERV.$bbs."/subject.txt";
#ディレクトリ用
$file_ipaddr = str_replace(".", "", $_SERVER['REMOTE_ADDR']);
$file_ipaddr = str_replace(":", "", $file_ipaddr);
#管理人メール
$ADMIN_MAIL = str_replace("@", "＠", $SETTING[ADMIN_MAIL]);
#認証画面
if ($bbs == "auth") {
header("Content-type: text/html; charset=Shift_JIS");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
exit;
 if (isset($_POST['g-recaptcha-response'])) {
    $url = 'https://www.google.com/recaptcha/api/siteverify';
    $param = array(
      'secret' => 'xxx',
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
	exit("reCAPTCHA認証に失敗しました。もう一度やりなおしてください");
    }
	if (strlen($_POST['trip']) < 3 or strlen($_POST['trip']) > 19) exit("認証用トリップが長すぎor短すぎます");
    $monafile = $BBSSERV."/".date('z')."/mn_".$_POST['trip'].".cgi";
    $MONADATA = array();
    $MONADATA['REMOTE_ADDR'] = $_SERVER['REMOTE_ADDR'];
    $MONADATA['expiry'] = $NOWTIME + 604800;
    file_put_contents($monafile, serialize($MONADATA));
    exit('認証しました。<hr>以下のトリップを名前欄にご利用ください。<br>※入力しても、実際のスレッドでは表示されません<input name="mcode" onfocus="this.select()" value="!#'.$_POST[trip].'" style="display:block;margin:auto;width:95%;" readonly=""><hr><a href="#" onclick="window.history.go(-1);">前ページに戻る</a><br><a href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a><a href="https://delight.rentalbbs.net/" target="_top">トップページに戻る</a>');
 }else exit("認証データがありません");
}else {
?>
<HTML>
<HEAD>
<title>CAPTCHA認証</title>
<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
<META HTTP-EQUIV="pragma" CONTENT="no-cache">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<script src="https://www.google.com/recaptcha/api.js"></script>
<script>
function onSubmit(token) {
 document.getElementById('postForm').submit();
}
</script>
</HEAD><body>
<h4>未対応ブラウザ用 CAPTCHA認証</h4>
<form method="POST" accept-charset="Shift_JIS" id="postForm" action="/auth/">
<b>BBS_RAWIP_CHECK=feature</b>の板・スレッドでの書き込みや、特定の環境においては、1日ごとにCAPTCHAを記入する必要があります<br>以下の欄にお好きな認証用トリップ(3byte以上20byte未満)を記入し、認証成功後は名前欄に認証用トリップを入れてお使いください<br>他人と被るとその分だけ規制に巻き込まれやすくなりますから、被らないようなものを推奨します<br>環境によってはCAPTCHAが表示されない場合もありますが、エラーがでなければ、正常に処理されています<br>日付が変わると、再度こちらで認証する必要がありますからご注意ください
<input type="text" name="trip" placeholder="認証用トリップ" style="min-width: 100%;margin: 1px 0 1px 0">
<button class="g-recaptcha" data-sitekey="xxx" data-callback="onSubmit" error-callback="onReCaptchaError">認証</button>
</form>
<?
}
exit;
}
#subject.txt
if ($subbbs == "subject.txt") {
header("Content-type: text/plain; charset=Shift_JIS");
#スレ一覧
$subject_file = $BBSSERV.$bbs."/subject.txt";
 if (is_file($subject_file)) {
	$LOG = file($subject_file);
	foreach($LOG as $tmp){
	list($key,$subject,$res,) = explode("<>",$tmp);
		echo $key.".dat<>".$subject." (".$res.")\n";
	}
 }
exit;
}
#.dat
if (($subbbs == "dat" and strpos($dat, '.dat') !== false) or ($subbbs == "kako" and $html)) {
header("Content-type: text/plain; charset=Shift_JIS");
if (!$html) {
 if ($dat_forbidden == 1) exit("お知らせ ★<><>2017/10/01(日) 00:00:00.00 ID:???<> スレッドの配信仕様が変更されました。 <br> 現在、お客様がご利用されている専用ブラウザは新仕様に対応しておりません。 <br> 最新バージョンをご利用でない場合は、専用ブラウザのアップデートをお願いいたします。 最新バージョンをご利用の場合でもご覧になれない場合、<br> 下記のページから新仕様に対応した5ch専用ブラウザをお選びください。<br> <br> http://www.5ch.net/browsers.html <>5ちゃんねる専用ブラウザをご利用の皆さまへ\n");
 elseif ($dat_forbidden == 2) {
 http_response_code(503);
 exit;
 }
 elseif ($dat_forbidden == 3) exit('NG');
}
#==================================================
#　キャッシュ用ディレクトリ
#==================================================
#-------------------------------dat	
	$datcache = $BBSSERV."/dat/".$bbs.$key.".dat";
#if(!file_exists($BBSSERV.$bbs."/")) notfound();
#if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/")) notfound();
#if(!file_exists($BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/")) notfound();
#スレッドの場所
$thread_file = $BBSSERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi";
if (is_file($thread_file)) {
 if (is_file($datcache)) $cache = file_get_contents($datcache);
# ここから削除
# if (is_file($datcache)) {
# if (count(file($datcache)) == $LINENUM) $cache = file_get_contents($datcache);
#}
$number = 1;
$LOG = file($thread_file);
	list($num,,,,,,,$subject,,) = explode("<>",$LOG[0]);
if ($num == "saku") notfound();
if ($num == "del" || strpos($num, "del") !== false) {
	$subject='削除済み';
}
if (!$cache) {
 foreach($LOG as $tmp){
	list($num,$name,,$time,$id,$message,,,,,) = explode("<>",$LOG[$number-1]);
		# $nameが空の場合は名無しとして扱う
		if (!$name || strpos(substr($name, 0, 3), '</') !== FALSE) $name = $SETTING['BBS_NONAME_NAME'].$name;
if ($time) $DATE = date("y/m/d H:i:s", $time);
else $DATE = '';
	if ($num == "del" || strpos($num, "del") !== false) {
		#レスが削除済みの場合
		$name='';
		$mail='';
		$DATE = 'NG';
		$id = '';
		$message=' 削除済 ';
	}
	if ($number == 1) $data .= $name."<><>".$DATE." ".$id."<>".$message."<hr><br>v2はこちら<br>https://r1.rentalbbs.net/".$bbs."/<>".$subject."\n";	
	else $data .= $name."<><>".$DATE." ".$id."<>".$message."<>\n";
$number += 1;
 }
 file_put_contents($datcache, $data, LOCK_EX);
}else $data = $cache;
#==================================================
#　出力
#==================================================
// bytes=0-
$range = $_SERVER['HTTP_RANGE'];
// 要求の開始、終了バイトを取得
preg_match('/bytes=(\d+)-(\d*)/', $range, $match);
$start = $match[1];
$end = $match[2];
if (empty($start)) {
    $start = 0;
}
// 終了未指定の場合は、開始+1mbとする
if (empty($end) or !$end) {
    $end = $start + (1024 * 1024) - 1;
    $e = strlen($data);
}else $e = $end-$start+1;
$total = strlen($data);
$contents = substr($data, $start, $e);
$content_length = strlen($contents);
if ($total == $content_length) {
    if (!$stop) header('HTTP/1.1 200 OK');
} else {
    header('HTTP/1.1 206 Partial Content');
}
header('Accept-Ranges: bytes');
header('Content-Length: '.strlen($contents));
header('Content-Range: bytes '.$start.'-'.($start+strlen($contents)-1).'/'.$total);
exit($contents);
}else {
notfound();
}
exit;
}
#DAT一覧
if (($subbbs == "dat" and strpos($dat, '.dat') === false) or $subbbs == "kako") {
header("Content-type: text/html; charset=Shift_JIS");
if (!$dat) $dat = substr($NOWTIME, 0, 5);
if ($dat > 99999 or $dat < 10000) notfound();
$B = $BBSSERV;
$path = "/".$bbs."/".substr($dat, 0, 4)."/".$dat."/";
$d = $dat + 1;
?>
<html>
<head><title>KAKOLOG <?=$bbs?>(<?=$dat?>)</title></head>
<body>
<div class="title">
<h1>KAKO LOG</h1>
<h2><?=$bbs?></h2>
<div align="right">
 <form method="GET" action="/<?=$bbs?>/subject.html" accept-charset="Shift_JIS">
  <input type="text" name="t" size="40" value="<?=$t?>"><input type="submit" value="スレッド検索"><input type="hidden" name="n" value="<?=$dat?>">
 </form>
</div>
<h3><?=$dat?></h3>
<p><span class="gotop"><a href="/<?=$bbs?>/">Go board top</a></span></p>
<a href="/<?=$bbs?>/subject.html?p=<?=$dat?>">Go THREAD List</a><hr><pre>
Back: <a href="/<?=$bbs?>/kako/<?=$d?>/">/<?=$bbs?>/kako/<?=$d?>/</a>
<a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<?
$files = glob($B.$path."*.cgi");
rsort($files);
foreach ($files as $k => $value) {
list(,$value) = explode($dat."/",$value);
$value = str_replace('.cgi', '', $value);
echo $value.'   <a href="/'.$bbs.'/dat/'.$value.'.dat">'.$value.'.dat</a>   <a href="/test/read.html/'.$bbs.'/'.$value.'/">read.html</a>   <a href="/test/read.cgi/'.$bbs.'/'.$value.'/">read.cgi</a>   '.date("y/m/d H:i:s", $value).' - '.date("y/m/d H:i:s", filemtime($B.$path.$value.".cgi")).'   '.filesize($B.$path.$value.".cgi")."\n";
}
$dat--;
?>Finish.
Next1: <a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<? $dat--; ?>
Next2: <a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<? $dat--; ?>
Next3: <a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<? $dat--; ?>
Next4: <a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<? $dat--; ?>
Next5: <a href="/<?=$bbs?>/kako/<?=$dat?>/">/<?=$bbs?>/kako/<?=$dat?>/</a>
<? $dat--; ?></pre><hr></body></html>
<?
exit;
}
#SETTING.TXT
if ($subbbs == "SETTING.TXT") {
header("Content-type: text/plain; charset=Shift_JIS");
$text = @file_get_contents($BBSSERV.$bbs."/SETTING.TXT");
echo $text;
exit;
}
#head.txt
if ($subbbs == "head.txt") {
header("Content-type: text/plain; charset=Shift_JIS");
$text = @file_get_contents($BBSSERV.$bbs."/head.txt");
echo $text;
exit;
}
#1000.txt
if ($subbbs == "1000.txt") {
header("Content-type: text/plain; charset=Shift_JIS");
$text = @file_get_contents($BBSSERV.$bbs."/1000.txt");
echo $text;
exit;
}
#index.html
if ($bbs and (!$subbbs or strpos($subbbs, 'index') !== false) and !$dat) {
header("Content-type: text/html; charset=Shift_JIS");
 if (is_file($BBSSERV.$bbs."/iten.txt")) {
 $iten = @file_get_contents($BBSSERV.$bbs."/iten.txt");
 exit($iten);
 }
$head = @file_get_contents($BBSSERV.$bbs."/head.txt");
$kokuti = @file_get_contents($BBSSERV.$bbs."/kokuti.txt");
$headed = @file_get_contents("/virtual/banana356s/public_html/rentalbbs.net/headed.txt");
if ($SETTING[BBS_BG_PICTURE]) $BG = ' background="'.$SETTING[BBS_BG_PICTURE].'"';
?>
<HTML>
<HEAD>
<title><?=$SETTING['BBS_TITLE']?>のスレッド一覧</title>
<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
<META HTTP-EQUIV="pragma" CONTENT="no-cache">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
</HEAD>
<body>
<? if ($SETTING[BBS_TITLE_PICTURE]) { ?><div align=center><a href="<?=$SETTING[BBS_TITLE_LINK]?>" border=0><img class="aimg" src="<?=$SETTING[BBS_TITLE_PICTURE]?>" border=0></a></div><? } ?>
<td><font size="+1"><b><?=$SETTING['BBS_TITLE']?></b></font></td>
<div><?=$head?></div>
あなたも掲示板を作りませんか？→ <b><a href="https://delight.kakiko.org/" target="_blank">無料レンタル掲示板delight</a>
<div id="threadlist" style="margin: 0; padding: 0 0 0 0.5em; padding: 0 0 1.0em 0.5em; height: 25em; overflow-y: scroll;word-break: break-all;"><div><b>最新スレッド</b></div><?
if (!$SETTING['MAX_RES']) $MAX_RES = 999;
else $MAX_RES = $SETTING['MAX_RES'] - 1;
if ($MAX_RES > 1999) $MAX_RES = 1999;
if ($MAX_RES < 299) $MAX_RES = 299;
$s = 1;
#スレ一覧
$subject_file = $BBSSERV.$bbs."/subject.txt";
	if (is_file($subject_file)) {
	$LOG = file($subject_file);
$subsa = @file($BBSSERV.$bbs."/subject.cgi");
$subdata = @file_get_contents($BBSSERV.$bbs."/subject.cgi");
if (count($LOG) < 15 and count($subsa) > 16) @file_put_contents($subject_file, $subdata, LOCK_EX);
	foreach($LOG as $tmp){
	list($key,$subject,$res,$time,$id,$hide,) = explode("<>",$tmp);
$d = substr(str_replace('ID:', '', $id), 0, 8);
# 時間
if ($time) {
$time = substr($time, 0, 10);	#unixtime
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

$time = "<font color=\"#000\">".$time."</font>";
$ikioi = "<font color=\"#ff9025\">".$ikioi."</font>";
$DATE = date("m/d H:i", $key);
		if ($even) $even = '';
		else $even = ' hhead hhead-bg';
		if (preg_match("/[0-9]/", $key) and !preg_match("/[^0-9]/", $key) and $subject and preg_match("/[0-9]/", $res) and !preg_match("/[^0-9]/", $res) and $res > 0 and $res < 1999 and $res < $MAX_RES) {
		if ($s < $SETTING['BBS_THREAD_NUMBER'] + 1) {
		echo "<div class=\"l-$key id-$d".$even."\"><a href=\"#t-$s\">$s:</a> <a href=\"../test/read.html/$bbs/$key/l10/?ls=10\">$subject ($res)</a> <span style=\"color:#666666;\">$time $ikioi $DATE $id</span><br></div>\n";
		$tlist[$s] = $key."<>".$subject;
		}
		else echo "<div class=\"l-$key id-$d".$even."\"><a href=\"../test/read.html/$bbs/$key/l10/?ls=10\">$s: $subject ($res)</a> <span style=\"color:#666666;\">$time $ikioi $DATE $id</span><br></div>\n";
		++$s;
		if ($s == $SETTING['BBS_THREAD_NUMBER'] + 1) echo '<div><hr><b>その他のスレッド</b></div>';
		}
	}
}
?></div></font>

<form method="POST" action="/test/bbs.cgi?guid=ON" style="margin: 0 0 0 2em;">
タイトル：<input type="text" name="subject" size="40"><input type="submit" value="新規スレッド作成" name="submit"><br>
名前：<input type="text" name="FROM" size="24"> E-mail：<input type="text" name="mail" size="24" value="<?=$_COOKIE["MAIL"]?>"><div class="backmsg" style="display: inline-block;"><input value="on" type="checkbox" id="seticon" name="icon" checked=""><a href="/test/icon.cgi">アイコン</a></div><br>
<textarea id="bbs-textarea" rows="8" cols="80" name="MESSAGE" wrap="OFF"></textarea><input type="hidden" name="bbs" value="<?=$bbs?>"><input type="hidden" name="time" value="<?=$NOWTIME?>"><br>画像：<input id="uploadImage" type="file" name="file" size="50" onchange="upload();"><span id="imgnotic">
</form>
<br>
<form method="POST" action="/test/delete.cgi">
<input type="hidden" name="bbs" value="<?=$bbs?>">
<input type="submit" name="submit" value="削除画面">
</form>

<form method="POST" action="/test/admin.cgi">
<input type="hidden" name="bbs" value="<?=$bbs?>">
<input type="submit" name="submit" value="管理者メニュー">
<input type="password" size="20" name="pass" value="">
</form>

管理者：<?=$ADMIN_MAIL?><br>
<small>スパム対策のため「@」を全角の「＠」に置き換えて表記しています。</small>
<div class="footer">delightly v1 - bbs.cgi Ver.1.1(2023/07/09)<br>旧dream.rentalbbs.net過去ログ</div>
</body></html>
<?
exit;
}
#subject.html
if ($bbs and strpos($subbbs, 'subject.html') !== false) {
header("Content-type: text/html; charset=Shift_JIS");
$r = explode('subject.html?',$_SERVER['REQUEST_URI']);
$a = explode('&',$r[1]);
if (strpos($a[0], 'p=') !== false) {
$p = explode('=',$a[0]);
$t = explode('=',$a[1]);
}
elseif (strpos($a[0], 't=') !== false) {
$t = explode('=',$a[0]);
$p = explode('=',$a[1]);
}
$n = $p[1];
$t = urldecode($t[1]);
if (is_utf8($t) === true) $t = mb_convert_encoding($t, 'SJIS-win', 'UTF-8');
if (!$n) $no = true;
if ($no) {
?>
<HTML>
<HEAD>
<meta property="og:title" content="<?=$SETTING['BBS_TITLE']?>＠スレッド一覧 - レンタル掲示板delight">
<meta name="og:description" content="スレッドフロート式高機能無料レンタル掲示板：delight。">
<meta property="og:url" content="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="レンタル掲示板delight">
<link rel="apple-touch-icon" href="https://delight.kakiko.org/icon.png">
<link rel="icon" href="https://delight.kakiko.org/favicon.ico">
<title><?=$SETTING['BBS_TITLE']?>＠スレッド一覧 | レンタル掲示板delight</title>
<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
<META HTTP-EQUIV="pragma" CONTENT="no-cache">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script>
<link href="https://delight.kakiko.org/css/lightbox.css" rel="stylesheet">
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
<script language="JavaScript"><!-- 
function next(n) {
	let p;
	if (location.search) p = location.search+'&p='+n;
	else p = '?p='+n;
    $.ajax({
        type: "GET",
 
        url: "./subject.html"+p,
 
        cache: true,

        success: function (data) {
        	document.getElementById('main').innerHTML = document.getElementById('main').innerHTML+data;
        },

        error: function () {
		return;
        }
    });
 
}
//--></script>
</HEAD>
<BODY TEXT="#000000" BGCOLOR="#FFFFFF" link="#0000FF" alink="#FF0000" vlink="#660099" background="https://delight.rentalbbs.net/static/ba.gif">
<div align="right">
        <form method="GET" action="./subject.html" accept-charset="Shift_JIS">
          <input type="text" name="t" size="40" value="<?=$t?>"><input type="submit" value="スレッド検索">
        </form>
      </div>
<a name="top"></a><a href="./index.html">板のトップ</a> <a href="#bottom">▼</a>
<div id="main" align=center>
<?
}
if (!$n) $n = substr($NOWTIME, 0, 5);
$s = 1;
while ($i < 100) {
if ($s > 500) break;
$sub_file = $BBSSERV.$bbs."/".substr($n, 0, 4)."/".substr($n, 0, 5)."/subject.txt";
 if (is_file($sub_file)) {
 $SUB = file($sub_file);
 if (!$linked) {
	echo "$n- スレッド一覧 <a href=\"?p=$n&t=$t\">この範囲のみ読む</a> <a href=\"/$bbs/kako/$n/\">KAKOLOG</a>";
	$linked = true;
 }
foreach($SUB as $tmp){
	list($key,$subject,$id,$msg,) = explode("<>",$tmp);
	if ($t and stristr($subject, $t) === false and stristr($msg, $t) === false) continue;
if ($time) {
$time = substr($time, 0, 10);	#unixtime
$today = getdate($time);
$JIKAN = $today['hours'];
$DATE = date("y/m/d H:i:s", $time);
}else $DATE = '';
	$msg = str_replace("<br>", " <br> ", $msg);
	$msg = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $msg);
	$msg = preg_replace_callback('/https?:\S+/', function ($m) {
  	  $url = $m[0];
	$url = preg_replace("/(ttps?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "$1://$2", $url);
   	       if (preg_match('/https?:\S+\.(gif|jpg|jpeg|tiff|png)/', $url)) {
   	     return "<a href=\"$url\" data-lightbox=\"image\">$url<br><img class=\"image\" src=\"$url\" width=\"65\" height=\"65\"></a>";
  	  }elseif(strpos($url, 'youtube.com/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "=")+1));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"320\" height=\"180\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
  	  }elseif(strpos($url, 'm.youtube.com/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "=")+1));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"320\" height=\"180\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
  	  }elseif(strpos($url, 'youtu.be/') !== false){
	$youtubeurl = substr($url, (strpos($url, "youtu.be/")+9));
	$youtubeurl = substr($youtubeurl, 0, 11);
  	      return "<iframe width=\"320\" height=\"180\" src=\"https://www.youtube.com/embed/$youtubeurl\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(strpos($url, 'nicovideo.jp/watch') !== false){
	$youtubeurl = substr($url, (strpos($url, "watch/")+6));
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"320\" height=\"180\" src=\"https://embed.nicovideo.jp/watch/$youtubeurl?persistence=1&amp;oldScript=1&amp;referer=https%3A%2F%2Fbex.jp%2F&amp;from=0&amp;allowProgrammaticFullScreen=1\" style=\"max-width: 100%;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(strpos($url, 'nico.ms/') !== false){
	$youtubeurl = substr($url, (strpos($url, "nico.ms/")+8));
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"320\" height=\"180\" src=\"https://embed.nicovideo.jp/watch/$youtubeurl?persistence=1&amp;oldScript=1&amp;referer=https%3A%2F%2Fbex.jp%2F&amp;from=0&amp;allowProgrammaticFullScreen=1\" style=\"max-width: 100%;\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(strpos($url, 'twitcasting.tv/') !== false){
	$youtubeurl = substr($url, (strpos($url, "twitcasting.tv/")+15));
  	      return "<iframe allowfullscreen=\"allowfullscreen\" allow=\"autoplay\" frameborder=\"0\" width=\"320\" height=\"180\" src=\"https://twitcasting.tv/$youtubeurl/embeddedplayer/live?auto_play=false&default_mute=false\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(strpos($url, 'www.tiktok.com/') !== false){
	$youtubeurl = substr($url, (strpos($url, "video/")+6));
  	      return "<iframe class=\"viewon\" width=\"320\" height=\"550\" src=\"https://www.tiktok.com/embed/$youtubeurl\" _src=\"https://www.tiktok.com/embed/$youtubeurl\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" data-ruffle-polyfilled=\"\"></iframe><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(preg_match('/https?/', $url) and strpos($url, 'www.instagram.com/p/') !== false){
  	      return "<iframe class=\"instagram-media instagram-media-rendered\" id=\"instagram-embed-12\" src=\"{$url}embed/?cr=1&amp;\" allowtransparency=\"true\" allowfullscreen=\"true\" frameborder=\"0\" height=\"500\" data-instgrm-payload-id=\"instagram-media-payload-12\" scrolling=\"no\" style=\"background-color: white; border-radius: 3px; border: 1px solid rgb(219, 219, 219); box-shadow: none; display: block; margin: 0px 0px 12px; min-width: 326px; padding: 0px;\" data-ruffle-polyfilled=\"\"></iframe><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(strpos($url, 'http') !== false and strpos($url, 'twitter.com/') !== false and strpos($url, '/status/') !== false) {
   	     return "<a href=\"$url\" target=\"_blank\">$url</a><blockquote class=\"twitter-tweet\"><a href=\"$url\" target=\"_blank\">$url</a></blockquote>";
  	  }elseif(preg_match('/https?:\S+\.mp4/', $url)){
  	      return "<video src=\"$url\" width=\"320\" height=\"170\" playsinline=\"\" controls=\"\"></video><br><a href=\"$url\" target=\"_blank\">$url</a>";
	}elseif(preg_match('/https?/', $url)){
		$url = preg_replace("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"$1://$2\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
  	  }else {
	    	$url = preg_replace("/(ttps?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", "<a href=\"h$1://$2\" target=\"_blank\">$1://$2</a>", $url);
  	      return $url;
}
	}, $msg);
#レスアンカーをリンクに変換
$msg = preg_replace_callback('/&gt;&gt;([0-9]+)(?![-\d])/', function ($m) {
	global $bbs, $key;
	return "<a href=\"https://$_SERVER[HTTP_HOST]/test/read.html/$bbs/$key/$m[1]\">&gt;&gt;$m[1]</a>";
	}, $msg);
$msg = preg_replace_callback('/&gt;&gt;([0-9]+)\-([0-9]+)/', function ($m) {
	return "<a href=\"https://$_SERVER[HTTP_HOST]/test/read.html/$bbs/$key/$m[1]-$m[2]/?st=$m[1]&to=$m[2]\">&gt;&gt;$m[1]-$m[2]</a>";
	}, $msg);
	$data .= "<table style=\"margin-bottom:10px;word-break:break-all;\" width=\"95%\" cellspacing=\"0\" cellpadding=\"5\" border=\"0\" bgcolor=\"#EFEFEF\" align=\"center\"><tbody><tr><td><dl><a name=\"$s\"></a><b><a class=\"t\" href=\"/test/read.html/$bbs/$key/\" style=\"text-decoration:none\"><font class=\"subject\" size=\"3\" color=\"#FF0000\"><t>$subject</t></font></a></b><div><dt>1：$DATE $id</dt><dd>$msg<br></dd></div></dl><div style=\"font-size:10pt\"><b><a href=\"../test/read.html/$bbs/$key/\" target=\"_blank\">全部読む</a> <a href=\"../test/read.html/$bbs/$key/l50/?ls=50\" target=\"_blank\">最新50</a> <a href=\"../test/read.html/$bbs/$key/-100/?to=100\" target=\"_blank\">1-100</a> <a href=\"./index.html\">板のトップ</a> <a href=\"./subject.html\">リロード</a></b></div></dd></td></tr></tbody></table>";
	++$s;
	}
 }
$i++;
$n--;
}
if ($data) echo $data;
else echo "<div class=\"notfound\">該当するスレッドは見つかりませんでした。<div class=\"notfound_hint\">検索のヒント:</div><ul><li>キーワードを短くしてみたり、数を減らしてみてください。</li><li>鯖の移転や板の引越、分割などがあった時には、移行を反映するまでしばらく時間(少なくとも数時間)がかかります。</li><li>明らかに結果がおかしい場合は運用スレッドに書き込んでくださると助かります。</li></ul></div>";
if ($data) echo "<button onclick=\"next($n)\">続きを読む</button> <a href=\"?p=$n&t=$t\">次</a><script src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>
<script src=\"https://delight.kakiko.org/js/lightbox.js\"></script>";
if ($no) {
?>
</div><a name="bottom"></a><a href="#top">▲</a></body></html>
<?
}
exit;
}
if ($bbs == 'test' and strpos($subbbs, 'icon.cgi') !== false) {
header("HTTP/1.1 200 OK");
header("Content-type: text/html; charset=Shift_JIS");
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>アイコン設定</title><link href="https://delight.kakiko.org/css/a.css" rel="stylesheet" type="text/css">
<script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script></head><body><div id="container"><section><h1 class="section-title">アイコン設定</h1><div class="contents"><img id="iconimg" style="padding: 3px;  margin-right: 3px;  border-radius: 45px;  display: block;  padding-bottom: 5px;  margin-left: -.1em;" width="45" height="45" align="left">：現在のアイコン<input id="imgurl" type="text" class="form-control" name="key" placeholder="画像URL"><p class="notice mt5">アイコンに設定するURLを入力してください</p></div><div class="contents">直接画像を選択：<input id="uploadImage" type="file" name="file" size="50" onchange="upload();"><p class="notice mt5">こちらでファイルを選択すると自動的にURLが入力されます。※imgur.comにアップロードされます</p></div><div class="contents"><input id="homepage" type="text" class="form-control" name="key" placeholder="ホームページURL"><p class="notice mt5">入力したURLがアイコンのリンク先となります</p></div><div class="contents"><button onclick="setimg()" class="btn btn-primary btn-lg btn-block">設定</button><br><br><button onclick="delimg()" class="btn btn-primary btn-lg btn-block">削除</button><h3 id="ntxt"></h3></div></section></div>
<hr><a href="#" onclick="window.history.go(-1);">前ページに戻る</a><br><a href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a><br><a href="https://delight.rentalbbs.net/">トップページに戻る</a>
<script>
if (getCookie("icon")) {
 document.getElementById('imgurl').value = getCookie("icon");
 document.getElementById('iconimg').src = getCookie("icon");
}
if (getCookie("homepage")) {
 document.getElementById('homepage').value = getCookie("homepage");
}
function setimg() {
 let cookname = escape(document.getElementById('imgurl').value); 
 document.cookie = "icon="+cookname+"; Max-Age=315360000; path=/";
 let cookhome = escape(document.getElementById('homepage').value); 
 document.cookie = "homepage="+cookhome+"; Max-Age=315360000; path=/";
 document.getElementById('ntxt').innerHTML = '設定完了';
}
function delimg() {
 document.cookie = "icon=; Max-Age=0; path=/";
 document.cookie = "homepage=; Max-Age=0; path=/";
 document.getElementById('ntxt').innerHTML = '削除完了';
}
function upload() {
  const preview = document.querySelector('img');
  const file = document.querySelector('input[type=file]').files[0];
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    base64Url = reader.result;
    base64 = base64Url.replace(new RegExp('data.*base64,'), '');
	imgur();
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
	/// APIに渡すときは先頭の data:~~~base64 を除外

function imgur() {
$.ajax({
  url: 'https://api.imgur.com/3/image',
  method: 'POST',
  headers: {
	"Authorization": 'Client-ID x'
  },
  data: {
    image: base64,
    type: 'base64'
  },
  success: function(r){
	imgurlink = r.data.link
	document.getElementById('imgurl').value = imgurlink; 
  },

  error: function () {
	document.getElementById('ntxt').innerHTML = '画像アップロードに失敗　ページをリロードしてください';
  }
});

}

}
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
</script>
</body></html>
<?
exit;
}
if ($bbs == 'test' and strpos($subbbs, 'backimg.cgi') !== false) {
header("HTTP/1.1 200 OK");
header("Content-type: text/html; charset=Shift_JIS");
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html lang="ja"><head><meta http-equiv="content-type" content="text/html; charset=Shift_JIS"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>スレッド背景画像の設定</title><link href="https://delight.kakiko.org/css/a.css" rel="stylesheet" type="text/css">
<script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script></head><body><div id="container"><section><h1 class="section-title">スレッド背景画像の設定</h1><div class="contents"><input id="imgurl" type="text" class="form-control" name="key" placeholder="画像URL"><p class="notice mt5">背景画像に設定するURLを入力してください</p></div><div class="contents">直接画像を選択：<input id="uploadImage" type="file" name="file" size="50" onchange="upload();"><p class="notice mt5">こちらでファイルを選択すると自動的にURLが入力されます。※imgur.comにアップロードされます</p></div><div class="contents"><button onclick="setimg()" class="btn btn-primary btn-lg btn-block">設定</button><br><br><button onclick="delimg()" class="btn btn-primary btn-lg btn-block">削除</button><h3 id="ntxt"></h3></div></section></div>
<hr><a href="#" onclick="window.history.go(-1);">前ページに戻る</a><br><a href="#" onclick="window.history.go(-2);">2つ前のページに戻る</a><br><a href="https://delight.rentalbbs.net/">トップページに戻る</a>
<script>
if (localStorage.getItem('backimg')) document.getElementById('imgurl').value = localStorage.getItem('backimg');
function setimg() {
	localStorage.setItem('backimg', document.getElementById('imgurl').value);
	document.getElementById('ntxt').innerHTML = '設定完了';
}
function delimg() {
	localStorage.removeItem('backimg');
	document.getElementById('ntxt').innerHTML = '削除完了';
}
function upload() {
  const preview = document.querySelector('img');
  const file = document.querySelector('input[type=file]').files[0];
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    base64Url = reader.result;
    base64 = base64Url.replace(new RegExp('data.*base64,'), '');
	imgur();
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
	/// APIに渡すときは先頭の data:~~~base64 を除外

function imgur() {
$.ajax({
  url: 'https://api.imgur.com/3/image',
  method: 'POST',
  headers: {
	"Authorization": 'Client-ID x'
  },
  data: {
    image: base64,
    type: 'base64'
  },
  success: function(r){
	imgurlink = r.data.link
	document.getElementById('imgurl').value = imgurlink; 
  },

  error: function () {
	document.getElementById('ntxt').innerHTML = '画像アップロードに失敗　ページをリロードしてください';
  }
});

}

}
</script>
</body></html>
<?
exit;
}
if ($bbs == 'test' and strpos($subbbs, 'morelist.php') !== false) {
header("HTTP/1.1 200 OK");
header("Content-type: text/plain; charset=Shift_JIS");
$p = explode('morelist.php?',$_SERVER['REQUEST_URI']);
$a = explode('&',$p[1]);
$a = explode('=',$a[0]);
$b = $a[1];
if (!$b) exit;
$BBQSERV = "/virtual/banana356s/public_html/rentalbbs/";	#格納鯖のパス
#人気スレ一覧
$file = $BBQSERV."threads.txt";
$LOG = file($file);
krsort($LOG);
$s = 1;
$t = 1;
$all = count($LOG);
$ninkilist = '';
foreach($LOG as $tmp){
	list($bbs,$key,$title,$board,$d) = explode("<>",$tmp);
	if (!$d) $d = $_SERVER[HTTP_HOST];
	$BBASERV = "/virtual/banana356s/public_html/".$d."/";	#格納鯖のパス
	$DATE = date("Y/m/d H:i:s", $key);
	$res = count(file($BBASERV.$bbs."/".substr($key, 0, 4)."/".substr($key, 0, 5)."/".$key.".cgi"));
	# 勢い
	#$a = $NOWTIME - $key;
	#$b = $res / $a;
	#$ikioi = round($b * 86400,1);
	#if ($ikioi > 99) $ikioi = floor($ikioi);
	if ($b == $bbs and $res > 20 and $res < 950) {
	 $ninkilist .= '<a href="https://'.$d.'/test/read.html/'.$bbs.'/'.$key.'/l10/?ls=10">'.$title.'</a> <small>'.$res.'コメント</small><br>';
	 ++$s;
	}
	if ($s > 5 or $t > 1000) break;
	++$t;
}
if ($s > 1) echo '<div>■ 今話題の人気スレッド</div><div>'.$ninkilist.'</div>';
exit;
}
if ($bbs == 'test' and strpos($subbbs, 'headline.php') !== false) {

exit;

header("HTTP/1.1 200 OK");
header("Content-type: text/plain; charset=Shift_JIS");
$p = explode('headline.php?',$_SERVER['REQUEST_URI']);
$a = explode('&',$p[1]);
$a = explode('=',$a[0]);
$b = $a[1];
if (!$b) exit;
#スレ一覧
$res_file = $BBSSERV.$b."/res.cgi";
	if (is_file($res_file)) {
	$LOG = file($res_file);
	foreach($LOG as $tmp){
	list($subject,$bbs,$key,$time,$msg,$num,) = explode("<>",$tmp);
if ($time) {
$time = substr($time, 0, 10);	#unixtime
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
	$msg = preg_replace("/\[(.+)\]\(https?:\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)\)/", "<a href=\"//$2\" rel=\"nofollow noopener\" target=\"_blank\" title=\"//$2\">$1</a>", $msg);
	$msg = preg_replace_callback("/(https?):\/\/([\w;\/\?:\@&=\+\$,\-\.!~\*'\(\)%#]+)/", function ($m) {
  	  $url = $m[1]."://".$m[2];
   	       if (preg_match('/https?:\S+\.(gif|jpg|jpeg|tiff|png)/', $url)) {
   	     return "<a href=\"$url\" data-lightbox=\"image\">$url</a>";
  	  }else return "<a href=\"$url\" target=\"_blank\">$url</a>";
	}, $msg);
$msg = preg_replace_callback('/&gt;&gt;([0-9]+)(?![-\d])/', function ($m) {
	global $bbs, $key;
	return "<a href=\"/test/read.html/$bbs/$key/$m[1]\" target=\"_blank\">&gt;&gt;$m[1]</a>";
	}, $msg);
		echo "<span class=\"l-$key\"><div class=\"hhead hhead-bg\"><div><a href=\"/test/read.html/$bbs/$key/l10/?ls=10\">$subject ($num)</a> <font color=\"#666666\" size=\"-1\">$time</font></div></div>&emsp;<span>$msg</span><br></span>";
	}
}
exit;
}
if ($bbs and $subbbs == "subback.html") {
header("Content-type: text/html; charset=Shift_JIS");
?><base href="https://<?=$_SERVER[HTTP_HOST]?>/<?=$bbs?>/">
<script>
document.write('<style type="text/css">body { background-color: honeydew; }a { margin-right: 1em; }div.floated { border: 1px outset honeydew; float: left; height: 20em; line-height: 1em; margin: 0 0 .5em 0; padding: .5em; }div.floated, div.block { background-color: honeydew; }div.floated a, div.block a { display: block; margin-right: 0; text-decoration: none; white-space: nowrap; }div.floated a:hover, div.block a:hover { background-color: cyan; }div.floated a:active, div.block a:active { background-color: gold; }div.right { clear: left; text-align: right; }div.right a { margin-right: 0; }div.right a.js { background-color: dimgray; border: 1px outset dimgray; color: palegreen; text-decoration: none; }</style><div class="right"><small><a href="./subject.html"><b>過去ログ倉庫はこちら</b></a> <a href="./"><b>板TOPはこちら</b></a></small></div></div><div><small id="trad">');
</script>
<?
if (!$SETTING['MAX_RES']) $MAX_RES = 999;
else $MAX_RES = $SETTING['MAX_RES'] - 1;
if ($MAX_RES > 1999) $MAX_RES = 1999;
if ($MAX_RES < 299) $MAX_RES = 299;
$s = 1;
#スレ一覧
$subject_file = $BBSSERV.$bbs."/subject.txt";
	if (is_file($subject_file)) {
	$LOG = file($subject_file);
$subsa = @file($BBSSERV.$bbs."/subject.cgi");
$subdata = @file_get_contents($BBSSERV.$bbs."/subject.cgi");
if (count($LOG) < 15 and count($subsa) > 16) @file_put_contents($subject_file, $subdata, LOCK_EX);
echo '<div><b>最新スレッド</b></div>';
	foreach($LOG as $tmp){
	list($key,$subject,$res,$time,$id,$hide,) = explode("<>",$tmp);
# 即死判定
if (!$SETTING['BBS_TH_LINE']) $SETTING['BBS_TH_LINE'] = 1;
if (!$SETTING['TIME_TO_LIVE']) $SETTING['TIME_TO_LIVE'] = 1209600;
if ($NOWTIME > $key + $SETTING['TIME_TO_LIVE'] and $SETTING['BBS_TH_LINE'] > $res) continue;
# 突然死判定
if ($SETTING['BBS_MAX_MODIFIED'] and $NOWTIME > substr($time, 0, 10) + $SETTING['BBS_MAX_MODIFIED']) continue;
# lifetimeルール
if ($SETTING['BBS_THREAD_LIFETIME'] and $NOWTIME > $key + $SETTING['BBS_THREAD_LIFETIME']) continue;
# 停止済みスレッド
if ($hide == "hide") continue;
$d = substr(str_replace('ID:', '', $id), 0, 8);
# 時間
if ($time) {
$time = substr($time, 0, 10);	#unixtime
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

$time = "<font color=\"#000\">".$time."</font>";
$ikioi = "<font color=\"#ff9025\">".$ikioi."</font>";
$DATE = date("m/d H:i", $key);
		if ($even) $even = '';
		else $even = ' hhead hhead-bg';
		if (preg_match("/[0-9]/", $key) and !preg_match("/[^0-9]/", $key) and $subject and preg_match("/[0-9]/", $res) and !preg_match("/[^0-9]/", $res) and $res > 0 and $res < 1999 and $res < $MAX_RES) {
		if ($s < $SETTING['BBS_THREAD_NUMBER'] + 1) {
		echo "<div class=\"l-$key id-$d".$even."\"><a href=\"#t-$s\">$s:</a> <a href=\"../test/read.html/$bbs/$key/l10/?ls=10\">$subject ($res)</a> <span style=\"color:#666666;\">$time $ikioi $DATE $id</span><br></div>\n";
		$tlist[$s] = $key."<>".$subject;
		}
		else echo "<div class=\"l-$key id-$d".$even."\"><a href=\"../test/read.html/$bbs/$key/l10/?ls=10\">$s: $subject ($res)</a> <span style=\"color:#666666;\">$time $ikioi $DATE $id</span><br></div>\n";
		++$s;
		if ($s == $SETTING['BBS_THREAD_NUMBER'] + 1) echo '<div><hr><b>その他のスレッド</b></div>';
		}
	}
}
exit;
}
#モバイル用スレ一覧
if ($bbs and $subbbs == "subback") {
header("Content-type: text/html; charset=Shift_JIS");
?>
<HTML>
<HEAD>
<meta property="og:title" content="<?=$SETTING['BBS_TITLE']?> - レンタル掲示板delight">
<meta name="og:description" content="スレッドフロート式高機能無料レンタル掲示板：delight。">
<meta property="og:url" content="https://<?=$_SERVER['HTTP_HOST']?>/<?=$bbs?>/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="レンタル掲示板delight">
<meta name="application-name" content="delight">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="apple-touch-icon" href="https://delight.kakiko.org/icon.png">
<link rel="icon" href="https://delight.kakiko.org/favicon.ico">
<title><?=$SETTING['BBS_TITLE']?> | レンタル掲示板delight</title>
<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
<META HTTP-EQUIV="pragma" CONTENT="no-cache">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<script type="text/javascript" src="https://delight.kakiko.org/js/jquery-1.11.3.min.js"></script>
<script>
function isSmartPhone() {
let v = false;
  if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
    v = true;
  } else {
    v = false;
  }
 if (localStorage.getItem('viewer') == 'sp') v = true;
 else if (localStorage.getItem('viewer') == 'pc') v = false;
 if (localStorage.getItem('subback') == "true") v = true;
 if (localStorage.getItem('subback') == "false") v = false;
 if (location.search.indexOf('v=sp') != -1) v = true;
 if (location.search.indexOf('v=pc') != -1) v = false;
	return v;
}
if (isSmartPhone() == false) location.href = '../index.html?v=pc';
</script>
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
<link href="https://delight.kakiko.org/css/s.css" rel="stylesheet" type="text/css">
<style>
#headline{margin-bottom:10px;font-size:10pt;overflow-y:scroll;height:150px;border-radius:3px;word-break:break-all;border:0.1px solid rgba(0,0,0,.5);padding:5px}.hide{display:none}.menu{line-height:30px}.bg{background:#ddd}.bg1{background:eee}.clear{clear:both}.hhead-bg{background:rgba(150,150,150,.1);}
</style>
<style>
body {
	font-family: ArialMT, "Hiragino Kaku Gothic ProN", "ヒラギノ角ゴ ProN W3";
	background-color: #fafafa;
	color: #000;
	font-size: 14px;
}
a {
	text-decoration: none;
	color: #1a98ff;
}
.threads {
	word-break: break-all;
	white-space: normal;
	margin-top: 5px;
	border-bottom: .5px solid #DCDCDC;
	padding-bottom: 5px;
}
.t {
	color: #000;
}
.right {
	right: 10px;
	position: absolute;
	color: #757a80;
	font-size: 10px;
}
.title {
	margin-left: 8px;
	margin-top: 1px;
	margin-bottom: 1px;
	margin-right: 20px;
}
.date {
	display: block;
	font-size: 80%;
	margin-left: 5px;
	font-size: 10px;
}
.speed {
	color: #cc3d3d;
}
.modified {
	color: #ff9025;
}
.created {
	color: #ccc;
}
.m {
	text-align: center;
	margin-top: .5em;
	padding-bottom: .5em;
	color: #1a98ff !important;
}
.postbutton {
	z-index:1500;
	display: block !important;
	border: 0px solid black;
	right: 10px;
	bottom: 10px;
	position: fixed;
	margin-bottom: 10px;
	background: rgb(29, 155, 240);
	border-radius: 30px 30px 30px 30px;
	box-sizing: border-box;
	box-shadow: 5px 3px 2px rgba(0, 0, 0, .3);
}
.postbutton a {
	width: 3.5em;
	display: block;
	height: 3.5em;
	color: rgb(255, 255, 255);
}
.postopen {
	fill: currentcolor;
	width: 1.5em;
	height: 1.5em;
	padding: 13px 0px 0px 13px;
}
.postopen g {
	color: rgb(255, 255, 255);
}
path {
	color: rgb(255, 255, 255);
}
.new {
accent-color: auto;align-content: normal;align-items: center;animation-delay: 0s;animation-direction: normal;animation-duration: 0s;animation-fill-mode: none;animation-iteration-count: 1;animation-name: none;animation-play-state: running;animation-timing-function: ease;appearance: none;aspect-ratio: auto;backdrop-filter: none;backface-visibility: visible;background-attachment: scroll;background-blend-mode: normal;background-clip: border-box;background-color: rgb(29, 155, 240);background-image: none;background-origin: padding-box;background-position-x: 0%;background-position-y: 0%;background-repeat: repeat;background-size: auto;block-size: 19px;border-block-end-color: rgb(255, 255, 255);border-block-end-style: solid;border-block-end-width: 1px;border-block-start-color: rgb(255, 255, 255);border-block-start-style: solid;border-block-start-width: 1px;border-bottom-color: rgb(255, 255, 255);border-bottom-left-radius: 9999px;border-bottom-right-radius: 9999px;border-bottom-style: solid;border-bottom-width: 1px;border-collapse: separate;border-end-end-radius: 9999px;border-end-start-radius: 9999px;border-image-outset: 0;border-image-repeat: stretch;border-image-slice: 100%;border-image-source: none;border-image-width: 1;border-inline-end-color: rgb(255, 255, 255);border-inline-end-style: solid;border-inline-end-width: 1px;border-inline-start-color: rgb(255, 255, 255);border-inline-start-style: solid;border-inline-start-width: 1px;border-left-color: rgb(255, 255, 255);border-left-style: solid;border-left-width: 1px;border-right-color: rgb(255, 255, 255);border-right-style: solid;border-right-width: 1px;border-spacing: 0px 0px;border-start-end-radius: 9999px;border-start-start-radius: 9999px;border-top-color: rgb(255, 255, 255);border-top-left-radius: 9999px;border-top-right-radius: 9999px;border-top-style: solid;border-top-width: 1px;bottom: auto;box-decoration-break: slice;box-shadow: none;box-sizing: content-box;break-after: auto;break-before: auto;break-inside: auto;caption-side: top;caret-color: rgb(255, 255, 255);clear: none;clip: auto;clip-path: none;clip-rule: nonzero;color: rgb(255, 255, 255);color-interpolation: srgb;color-interpolation-filters: linearrgb;color-scheme: normal;column-count: auto;column-fill: balance;column-gap: normal;column-rule-color: rgb(255, 255, 255);column-rule-style: none;column-rule-width: 0px;column-span: none;column-width: auto;contain: none;contain-intrinsic-block-size: none;contain-intrinsic-height: none;contain-intrinsic-inline-size: none;contain-intrinsic-width: none;container-name: none;container-type: normal;content: normal;counter-increment: none;counter-reset: none;counter-set: none;cursor: pointer;cx: 0px;cy: 0px;d: none;direction: ltr;display: flex;dominant-baseline: auto;empty-cells: show;fill: rgb(0, 0, 0);fill-opacity: 1;fill-rule: nonzero;filter: none;flex-direction: row;flex-wrap: nowrap;float: none;flood-color: rgb(0, 0, 0);flood-opacity: 1;font-family: "Segoe UI", Meiryo, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;font-feature-settings: normal;font-kerning: auto;font-language-override: normal;font-optical-sizing: auto;font-palette: normal;font-size: 10px;font-size-adjust: none;font-stretch: 100%;font-style: normal;font-synthesis-small-caps: auto;font-synthesis-style: auto;font-synthesis-weight: auto;font-variant-alternates: normal;font-variant-caps: normal;font-variant-east-asian: normal;font-variant-ligatures: normal;font-variant-numeric: normal;font-variant-position: normal;font-variation-settings: normal;font-weight: 700;height: 19px;hyphenate-character: auto;hyphens: manual;image-orientation: from-image;image-rendering: auto;ime-mode: auto;inline-size: 19px;inset-block-end: auto;inset-block-start: auto;inset-inline-end: auto;inset-inline-start: auto;isolation: auto;justify-content: center;left: auto;letter-spacing: normal;lighting-color: rgb(255, 255, 255);line-break: auto;line-height: 15px;list-style-image: none;list-style-position: outside;list-style-type: disc;margin-block-end: 0px;margin-block-start: 0px;margin-bottom: 0px;margin-inline-end: 0px;margin-inline-start: 11px;margin-left: 11px;margin-right: 0px;marker-end: none;marker-mid: none;marker-start: none;mask-clip: border-box;mask-composite: add;mask-image: none;mask-mode: match-source;mask-origin: border-box;mask-position-x: 0%;mask-position-y: 0%;mask-repeat: repeat;mask-size: auto;mask-type: luminance;max-block-size: none;max-height: none;max-inline-size: none;max-width: none;min-block-size: auto;min-height: auto;min-inline-size: 19px;min-width: 19px;mix-blend-mode: normal;object-fit: fill;object-position: 50% 50%;offset-anchor: auto;offset-distance: 0px;offset-path: none;offset-rotate: auto;opacity: 1;outline-color: rgb(255, 255, 255);outline-offset: 0px;outline-style: none;outline-width: 0px;overflow-anchor: auto;overflow-block: visible;overflow-clip-margin: 0px;overflow-inline: visible;overflow-wrap: break-word;overflow-x: visible;overflow-y: visible;overscroll-behavior-block: auto;overscroll-behavior-inline: auto;overscroll-behavior-x: auto;overscroll-behavior-y: auto;padding-block-end: 0px;padding-block-start: 0px;padding-bottom: 0px;padding-inline-end: 0px;padding-inline-start: 0px;padding-left: 0px;padding-right: 0px;padding-top: 0px;page: auto;paint-order: normal;perspective: none;perspective-origin: 10.5px 10.5px;pointer-events: auto;print-color-adjust: economy;quotes: auto;r: 0px;resize: none;rotate: none;row-gap: normal;ruby-align: space-around;ruby-position: alternate;rx: auto;ry: auto;scale: none;scroll-behavior: auto;scroll-margin-block-end: 0px;scroll-margin-block-start: 0px;scroll-margin-bottom: 0px;scroll-margin-inline-end: 0px;scroll-margin-inline-start: 0px;scroll-margin-left: 0px;scroll-margin-right: 0px;scroll-margin-top: 0px;scroll-snap-align: none;scroll-snap-stop: normal;scroll-snap-type: none;scrollbar-color: rgb(185, 202, 211) rgb(247, 249, 249);scrollbar-gutter: auto;scrollbar-width: auto;shape-image-threshold: 0;shape-margin: 0px;shape-outside: none;shape-rendering: auto;stop-color: rgb(0, 0, 0);stop-opacity: 1;stroke: none;stroke-dasharray: none;stroke-dashoffset: 0px;stroke-linecap: butt;stroke-linejoin: miter;stroke-miterlimit: 4;stroke-opacity: 1;stroke-width: 1px;tab-size: 8;text-align-last: auto;text-anchor: start;text-combine-upright: none;text-decoration-color: rgb(255, 255, 255);text-decoration-line: none;text-decoration-skip-ink: auto;text-decoration-style: solid;text-decoration-thickness: auto;text-emphasis-color: rgb(255, 255, 255);text-emphasis-position: over;text-emphasis-style: none;text-indent: 0px;text-justify: auto;text-orientation: mixed;text-rendering: auto;text-shadow: none;text-transform: none;text-underline-offset: auto;text-underline-position: auto;top: auto;touch-action: auto;transform: none;transform-box: border-box;transform-origin: 10.5px 10.5px;transform-style: flat;transition-delay: 0s;transition-duration: 0s;transition-property: all;transition-timing-function: ease;translate: none;unicode-bidi: isolate;user-select: none;vector-effect: none;visibility: visible;white-space: nowrap;will-change: auto;word-break: normal;word-spacing: 0px;writing-mode: horizontal-tb;x: 0px;y: 0px;z-index: auto;-moz-box-align: center;-moz-box-direction: normal;-moz-box-flex: 0;-moz-box-ordinal-group: 1;-moz-box-orient: horizontal;-moz-box-pack: center;-moz-float-edge: content-box;-moz-force-broken-image-icon: 0;-moz-image-region: auto;-moz-orient: inline;-moz-text-size-adjust: auto;-moz-user-focus: none;-moz-user-input: auto;-moz-user-modify: read-only;-moz-window-dragging: default;-webkit-line-clamp: none;-webkit-text-fill-color: rgb(255, 255, 255);-webkit-text-stroke-color: rgb(255, 255, 255);-webkit-text-stroke-width: 0px;text-align: right;position: absolute;right: 10px;margin-top: 12px;width: 3em;height: 1em;
}
</style>
<script type="text/javascript" src="https://delight.kakiko.org/js/t2.js"></script>
<script>
$(document).ready(function(){
	$('#linkToTop').on('click',function(e){
		e.preventDefault();
		$('html,body').scrollTop(0);
	});	

	$(document).on("click",".up",function(e){
		$("html,body").animate({scrollTop:$("#header").scrollTop()},{duration:500});
		e.preventDefault();
	});

	$(document).on("click",".down",function(e){
		$("html,body").animate({scrollTop:$(".footer").position().top},{duration:500});
		e.preventDefault();
	});

	$("body").append(
		'<div class="up_down_div" style="z-index:10000;position: fixed; bottom: 220px; right: 10px; top: 333px;">'+
		'<div style="position:relative">'+
		'<div style="font-size:16px;position:absolute;top:-30px;right:0px">'+
		'<a href="#" class="up" style="color: rgba(0, 0, 0, 0.3); "><div class="fas fa-chevron-circle-up">▲</div></a>'+
		'</div>'+
		'<div style="font-size:16px;position:absolute;top:+30px;right:0px">'+
		'<a href="#" class="down" style="color: rgba(0, 0, 0, 0.3); "><div class="fas fa-chevron-circle-down">▼</div></a>'+
		'</div>'+
		'</div>'+
		'</div>'
	);
});
</script>
</head>
<body>
<script>
	if (localStorage.getItem('darkmode') === null) localStorage.setItem('darkmode', false);
	darkmode = localStorage.getItem('darkmode');
	if (darkmode == "true") document.body.innerHTML += '<link href="https://delight.kakiko.org/css/dark.css" rel="stylesheet">';
</script>
<script>
function load() {
	 window.location.reload(true);
}
function make() {
	document.getElementById('makethread').style.display = 'block';
}
function rclose() {
	document.getElementById('makethread').style.display = 'none';
}
function LR() {
	document.getElementById('localrule').style.display = 'block';
}
function lclose() {
	document.getElementById('localrule').style.display = 'none';
}
</script>
<script>
function imgur(s) {
$.ajax({
  url: 'https://api.imgur.com/3/image',
  method: 'POST',
  headers: {
	"Authorization": 'Client-ID x'
  },
  data: {
    image: base64,
    type: 'base64'
  },
  success: function(r){
	imgurlink = r.data.link
	document.getElementById("sp-textarea").value += '\n'+imgurlink;
	document.getElementById("spimgnotic").innerHTML = '画像をアップロードしました';
  },

  error: function () {
	document.getElementById("spimgnotic").innerHTML = 'アップロードできません';
  }
});

}
</script>
<form method="GET" action="/search/" accept-charset="Shift_JIS"><div id="header" class="search-header" style="display:block;"><div class="search-left"><div class="search-logo" style="font-size:15px !important;"><?=$SETTING['BBS_TITLE']?></div><div class="search-input"><input value="" id="search-text" type="text" name="q" placeholder="キーワードを入力" style="height:25pt"><button id="search-button"><img src="https://delight.rentalbbs.net/static/magni.png" style="height:12px;width:12px;margin-right:3px">検索</button></div></div><div class="search-right"><a href="https://delight.rentalbbs.net/login.html"><div class="search-setting dropdown"><img class="dropBtnSetting settingDrop" src="https://delight.rentalbbs.net/static/icon_login.png" style="margin-right:2px;vertical-align:middle;height:22px;width:auto;"><span class="dropBtnSetting settingDrop">ログイン</span></div></a></div><div class="search-clear"></div></div></form>
<div id="main">
<div class="threads"><div id="headline" inview="inview"></div></div>
<a href="javascript:void(0);" onclick="LR()"><div class="m threads">ローカルルールを表示</div></a>
<div class="newposts"><center><a href="javascript:load()">リロード<img alt="再読み込み" loading="lazy" decoding="async" data-nimg="1" style="color: transparent;" src="//www.rentalbbs.net/static/reload.svg" width="16" height="16"></a></center><hr></div>
<div class="threads"><b>最新スレッド</b></div>
<?
if (!$SETTING['MAX_RES']) $MAX_RES = 999;
else $MAX_RES = $SETTING['MAX_RES'] - 1;
if ($MAX_RES > 1999) $MAX_RES = 1999;
if ($MAX_RES < 299) $MAX_RES = 299;
$s = 1;
#スレ一覧
$subject_file = $BBSSERV.$bbs."/subject.txt";
	if (is_file($subject_file)) {
	$LOG = file($subject_file);
$subsa = @file($BBSSERV.$bbs."/subject.cgi");
$subdata = @file_get_contents($BBSSERV.$bbs."/subject.cgi");
if (count($LOG) < 15 and count($subsa) > 16) @file_put_contents($subject_file, $subdata, LOCK_EX);
	foreach($LOG as $tmp){
	list($key,$subject,$res,$time,,$hide,) = explode("<>",$tmp);
# 即死判定
if (!$SETTING['BBS_TH_LINE']) $SETTING['BBS_TH_LINE'] = 1;
if (!$SETTING['TIME_TO_LIVE']) $SETTING['TIME_TO_LIVE'] = 1209600;
if ($NOWTIME > $key + $SETTING['TIME_TO_LIVE'] and $SETTING['BBS_TH_LINE'] > $res) continue;
# 突然死判定
if ($SETTING['BBS_MAX_MODIFIED'] and $NOWTIME > substr($time, 0, 10) + $SETTING['BBS_MAX_MODIFIED']) continue;
# lifetimeルール
if ($SETTING['BBS_THREAD_LIFETIME'] and $NOWTIME > $key + $SETTING['BBS_THREAD_LIFETIME']) continue;
# 停止済みスレッド
if ($hide == "hide") continue;
# 時間
if ($time) {
$time = substr($time, 0, 10);	#unixtime
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

$DATE = date("Y/m/d H:i:s", $key);
		if (preg_match("/[0-9]/", $key) and !preg_match("/[^0-9]/", $key) and $subject and preg_match("/[0-9]/", $res) and !preg_match("/[^0-9]/", $res) and $res > 0 and $res < 1999 and $res < $MAX_RES) {
		echo "<div class=\"l-$key threads\"><a class=\"t\" href=\"/test/read.html/$bbs/$key/l10/?ls=10\"><span class=\"right\">$res</span><span id=\"n-$key\"></span><div id=\"t-$key\" class=\"title\">$subject</div><span class=\"date\"><span class=\"right\"><span class=\"speed\">$ikioi/日</span></span><span class=\"created\">$DATE</span> <span class=\"modified\">$time</span></span></a></div>\n";
		++$s;
		if ($s == $SETTING['BBS_THREAD_NUMBER'] + 1) echo '<div class="threads"><b>その他のスレッド</b></div>';
		}
	}
}
$head = @file_get_contents($BBSSERV.$bbs."/head.txt");
$kokuti = @file_get_contents($BBSSERV.$bbs."/kokuti.txt");
?>
<div class="m threads"><b><a href="../subject.html">過去ログ倉庫はこちら</a></b></div>
</div>
<script>
function headline() {
    $.ajax({
        type: "GET",
 
        url: "/test/headline.php?bbs=<?=$bbs?>",
 
        cache: true,

        success: function (data) {
        	document.getElementById('headline').innerHTML = data;
        },

        error: function () {
		return;
        }
    });
 
}
headline();
setInterval(headline, 5000);
</script>
<script>
	let ntjson;
	let ntlist = [];
	ntjson = localStorage.getItem('ngtitle');
	if (ntjson) {
	ntlist = JSON.parse(ntjson);
	ntlist = ntlist.filter(Boolean);
	}
	let kjson;
	let klist = [];
	kjson = localStorage.getItem('klist');
	if (kjson) {
	klist = JSON.parse(kjson);
	klist = klist.filter(Boolean);
	}
			let mute = '<style>';
			let threadlist = document.getElementById('main');
			let data = threadlist.innerHTML.split('\n');
			data.forEach(function(value) {
			if (value.indexOf('<div class="l-') == -1) return;
			let key = value.match(/<div class="l-([0-9]+) threads"><a class="t" href=/);
			if (!key) return;
			key = key[1];
			let res = value.match(/<span class="right">([0-9]+)<\/span>/);
			if (!res) return;
			res = res[1];
			if (localStorage.getItem('<?=$bbs?>'+key)) document.getElementById('t-'+key).style.fontWeight = 'bold';
			if (localStorage.getItem('<?=$bbs?>'+key) && res > localStorage.getItem('<?=$bbs?>'+key)) {
			 let nres = res - localStorage.getItem('<?=$bbs?>'+key);
			 document.getElementById('n-'+key).innerHTML = '<div class="new">'+nres+'</div>';
			}
			let title = value.match(/ class=\"title\">(.+)<\/div><span class="date">/);
			if (!title) return;
			title = title[1];
			let NG;
	if (ntlist) {
			 for (let i = 0; i < ntlist.length; i++) {
			 if (!ntlist[i]) continue;
			  if (title.indexOf(ntlist[i]) != -1) {
			  mute += '.l-'+key+'{display:none;}';
			  break;
			  }
			 }
	}
			});
			mute += '</style>';
			document.body.innerHTML += mute;
</script>
<div class="menu">
あなたも掲示板を作りませんか？<br><b><a href="https://delight.kakiko.org/" target="_blank">無料レンタル掲示板delight</a><br><a href="https://akari.kakiko.org/faq/" target="_blank">FAQ</a></b><br><b><a href="/find/">本文検索</a></b><br><b><a href="../index.html?v=pc">PC版はこちら</a></b><font size="2"><center><a href="/" target="_blank">■<b>掲示板一覧</b>■</a><br>他の仲間掲示板へのリンクです</center></font><br>
<div class="footer">
<form method="POST" action="/test/delete.cgi">
<input type="hidden" name="bbs" value="<?=$bbs?>">
<input type="submit" name="submit" value="削除画面">
</form>

<form method="POST" action="/test/admin.cgi">
<input type="hidden" name="bbs" value="<?=$bbs?>">
<input type="submit" name="submit" value="管理者メニュー">
<input type="password" size="20" name="pass" value="">
</form>

管理者：<?=$ADMIN_MAIL?><br>
<small>スパム対策のため「@」を全角の「＠」に置き換えて表記しています。</small><br>
bbs.cgi Ver.1.1(2023/07/09)
</div>
<div class="postbutton"><a href="javascript:void(0);" onclick="make()" style="color: rgb(255, 255, 255) !important;"> <svg viewBox="0 0 24 24" aria-hidden="true" class="postopen"><g><path d="M23 3c-6.62-.1-10.38 2.421-13.05 6.03C7.29 12.61 6 17.331 6 22h2c0-1.007.07-2.012.19-3H12c4.1 0 7.48-3.082 7.94-7.054C22.79 10.147 23.17 6.359 23 3zm-7 8h-1.5v2H16c.63-.016 1.2-.08 1.72-.188C16.95 15.24 14.68 17 12 17H8.55c.57-2.512 1.57-4.851 3-6.78 2.16-2.912 5.29-4.911 9.45-5.187C20.95 8.079 19.9 11 16 11zM4 9V6H1V4h3V1h2v3h3v2H6v3H4z"></path></g></svg> </a></div>
<div id="makethread" style="display:none;">
<div style="position:fixed;top:0px;left:0px;z-index:2000;width:100%;height:100%;text-align:center;background-color:rgba(0, 0, 0, 0.4);overflow:auto">
<div style="margin-top:10px;border-radius:3px;background:#eeeeee;box-shadow: 1px 1px 2px gray;width:95%;display:inline-block;text-align:left" class="wi">
<form method="POST" action="/test/bbs.cgi?guid=ON" style="margin:0;padding:0;line-height:3px">
<div style="border-radius:3px 3px 0 0;color:#666;padding:3px;">
<span style="padding-top: 10px;display: inline-block;padding-left: 10px;" onclick="rclose()">キャンセル</span>
<span style="color:#000;float:right;font-size:28px;font-weight:bold;cursor:pointer;display:inline-block;padding-right:5px;"><input type="submit" name="submit" style="cursor: pointer;border: none; background: rgb(29, 155, 240);color: #ffffff;" value="新規スレッド作成"></span>
</div>
<div style="padding:10px">
<div><input name="subject" style="width:100%;margin:2px;border-radius: 0px 0px 5px 5px;" placeholder="スレッドタイトル"></div>
<div>
<input style="width: 100%;margin: 2px;border-radius: 0px 0px 5px 5px;" size="8" name="FROM" placeholder="名前"><input style="width: 100%;margin: 2px;border-radius: 0px 0px 5px 5px;" size="8" name="mail" placeholder="E-mail" value="<?=$_COOKIE["MAIL"]?>"><div class="backmsg" style="display: inline-block;"><a href="<?=$_COOKIE[homepage]?>" target="_blank"><img src="<?=$_COOKIE[icon]?>" class="icon" width="50" height="50" align="left" style="padding: 3px;  margin-right: 3px;  border-radius: 45px;  display: block;  padding-bottom: 5px;  margin-left: -.1em;"></a><input value="on" type="checkbox" id="seticon" name="icon" checked=""><a href="/test/icon.cgi">アイコン</a></div>
</div>
<div>
<textarea id="sp-textarea" name="MESSAGE" style="font-variant: inherit;font-weight: inherit;font-stretch: inherit;border-radius: 0px 0px 5px 5px;padding: 0px;word-break: break-all;overflow: auto;width: 100%;margin: 2px;font-size:16px" rows="5" placeholder="言いたいことは？"></textarea>
</div>
<div style="margin-top: 10px;">画像：<input id="spImage" type="file" name="file" size="50" onchange="spupload();"></div><div id="spimgnotic">
<script>
function spupload() {
  const preview = document.querySelector('img');
  const file = document.querySelector('#spImage').files[0];
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    base64Url = reader.result;
    base64 = base64Url.replace(new RegExp('data.*base64,'), '');
	imgur("sp");
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
	/// APIに渡すときは先頭の data:~~~base64 を除外
}
</script>
</div>
<input type="hidden" name="bbs" value="<?=$bbs?>"><input type="hidden" name="time" value="<?=$NOWTIME?>">
</div>
</form>
</div>
</div>
</div>
<div id="localrule" style="display:none;">
<div style="position:fixed;top:0px;left:0px;z-index:2000;width:100%;height:100%;text-align:center;background-color:rgba(0, 0, 0, 0.4);overflow:auto">
<div style="margin-top:50px;border-radius:3px;background:#eeeeee;box-shadow: 1px 1px 2px gray;width:90%;display:inline-block;text-align:left" class="wi">
<span style="color:#000;float:right;font-size:28px;font-weight:bold;cursor:pointer;display:inline-block;padding-right:5px;" class="rclose" onclick="lclose()">×</span>
<div style="padding: 1em 1em 1em 1em;"><?=$head?></div><hr><div style="padding: 1em 1em 1em 1em;"><?=$kokuti?></div>
</div>
</div>
</div>
</body></html>
<?
exit;
}
#その他の場合は404
notfound();

# UTF-8か判定する関数
function is_utf8($str)
{
    $len = strlen($str);
    for ($i = 0; $i < $len; $i++) {
        $c = ord($str[$i]);
        if ($c > 128) {
            if (($c > 247)) {
                return false;
            } elseif ($c > 239) {
                $bytes = 4;
            } elseif ($c > 223) {
                $bytes = 3;
            } elseif ($c > 191) {
                $bytes = 2;
            } else {
                return false;
            }
            if (($i + $bytes) > $len) {
                return false;
            }
            while ($bytes > 1) {
                $i++;
                $b = ord($str[$i]);
                if ($b < 128 || $b > 191) {
                    return false;
                }
                $bytes--;
            }
        }
    }
    return true;
}
?>
<? exit; ?>