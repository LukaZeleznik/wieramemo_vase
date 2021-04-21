/**
 * Upscore
 */
(function(u,p,s,c,r){u[r]=u[r]||function(p){(u[r].q=u[r].q||[]).push(p)},u[r].ls=1*new Date();
var a=p.createElement(s),m=p.getElementsByTagName(s)[0];a.async=1;a.src=c;m.parentNode.insertBefore(a,m)
})(window,document,'script','//files.upscore.com/async/upScore.js','upScore');

/**
 * Dotmetrics
 */
(function () {
window.dm=window.dm|| {AjaxData:[]},window.dm.AjaxEvent=function(et,d,ssid){dm.AjaxData.push({et:et,d:d,ssid:ssid}),window.DotMetricsObj&&DotMetricsObj.onAjaxDataUpdate()};
var d=document,
h=d.getElementsByTagName('head')[0],
s=d.createElement('script');
s.type='text/javascript';
s.async=true;
s.src=document.location.protocol + '//script.dotmetrics.net/door.js?id=1804';
h.appendChild(s);
}());

/**
 * Google analytics
 */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date())

/**
 * Service workers
 */
var _ua = navigator.userAgent || navigator.vendor || window.opera || '';
var isFbInAppBrowser = (_ua.indexOf("FBAN") > -1) || (_ua.indexOf("FBAV") > -1);
var isSafari = /^((?!chrome|android).)*safari/i.test(_ua);

if ('serviceWorker' in navigator && !isFbInAppBrowser && !isSafari) {
    navigator.serviceWorker.register('/sw.js');
}
