function isSmartPhone() {
  if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
    return true;
  } else {
    return false;
  }
}
window.addEventListener('load', function () {
if (document.getElementById("js--banners--bottom") != null) {
let bottom = document.getElementById("js--banners--bottom");
if (isSmartPhone() === false) bottom.innerHTML = '<iframe scrolling="no" style="width: 100%;height: auto; margin: 0px;" src="https://www.3chan.jp/static/ad.htm" frameborder="no"></iframe>';
else bottom.innerHTML = '<iframe scrolling="no" style="width: 100%;height: auto; margin: 0px;" src="https://www.3chan.jp/static/ad2.htm" frameborder="no"></iframe>';
}else {
var ad2 = document.createElement('div');
if (isSmartPhone() === false) ad2.innerHTML = '<div class="js--ad--bottom" style="padding-top:5px;padding-bottom:5px;padding-left:30px;"><iframe scrolling="no" style="width: 100%;height: auto; margin: 0px;" src="https://www.3chan.jp/static/ad.htm" frameborder="no"></iframe></div><div class="push" style="clear:both;"></div>';
else ad2.innerHTML = '<iframe scrolling="no" style="width: 100%;height: auto; margin: 0px;" src="https://www.3chan.jp/static/ad2.htm" frameborder="no"></iframe>';
if (document.getElementsByClassName("thread")[0] != null) document.getElementsByClassName("thread")[0].appendChild(ad2);
else if (document.getElementById("main") != null) document.getElementById("main").appendChild(ad2);
}
});