<?php
$BBSSERV = "./";
# /test/read.cgi/bbs/key/num
# /bbs/dat/key.dat
$pairs = explode('/',$_SERVER['REQUEST_URI']);
$bbs = $pairs[1];
$subbbs = $pairs[2];
$dat = $pairs[3];
$key = str_replace(".dat", "", $dat);

@include $BBSSERV."main.cgi";
exit("何かが変だ、またの機会にしてくれ index.cgi");

function notfound() {
    header("Content-type: text/pian; charset=utf-8");
    exit("404");
}
?>