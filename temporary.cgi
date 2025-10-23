<?php
header("Content-type: text/html; charset=iso-8859-1");
$sttime = microtime(true);
$buffer = $_SERVER['REQUEST_URI'];
$pairs = explode('/',$buffer);
$bbs = $pairs[1];
if (!$bbs) {
?><html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
</body></html>
<? exit;
}
?><!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL <?=$_SERVER["REQUEST_URI"]?> was not found on this server.</p>
<hr>
<address>Apache Server at turing1000.nttec.com Port 80</address>
</body></html>

