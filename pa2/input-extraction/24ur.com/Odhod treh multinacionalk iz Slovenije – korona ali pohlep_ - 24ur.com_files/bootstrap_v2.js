/**
 * Our current app version
 */
var appVersion = 0;

try {
    var scriptTag = document.getElementById('bootstrap-script');
    if (scriptTag) {
        appVersion = parseInt(scriptTag.getAttribute("data-appversion"), 10);
        if (isNaN(appVersion)) {
            appVersion = 0;
        }
    }
} catch (e) {
    console.log(e);
    appVersion = 0;
}

/**
 * This one gets set to true when sso_container loads.
 * At that point we're ready for logins
 */
var isSSOReady = false;

/**
 * Redirect for old browsers.
 * UAParser is not defined when rendering SSR version with node.
 */
var oldBrowsersPage = '/assets/old-browser/index.html';

var videojs = null;

if (typeof UAParser !== 'undefined') {
    var uaResult = (new UAParser()).getResult();

    if (uaResult && uaResult.browser && uaResult.browser.name && uaResult.browser.major) {
        var browser = uaResult.browser.name;
        var major = parseInt(uaResult.browser.major, 10);

        if ((browser === 'IE') && !isNaN(major) && (major <= 10)) {
            document.location.href = oldBrowsersPage;
        }
    }
}

/**
 * SSO iframes
 *
 * If iframes were created in index.html and if we add onload handler here,
 * iframe could already be loaded. This onload handler added here would
 * never be called.
 */
var ssoContainer = document.getElementById('sso_container');
if (ssoContainer) {
    var ssoIFrame = document.createElement('iframe');
    ssoIFrame.onload = function () { isSSOReady = true; };
    ssoIFrame.src = 'https://www.24ur.com/assets/sso.html?v=5';
    ssoIFrame.style = 'display:none';
    ssoIFrame.id = 'sso';
    ssoContainer.appendChild(ssoIFrame);
}

var ssoDevContainer = document.getElementById('sso_container_dev');
if (ssoDevContainer) {
    var ssoDevIFrame = document.createElement('iframe');
    ssoDevIFrame.onload = function() { isSSOReady = true; };
    ssoDevIFrame.src = 'http://localhost:3000/assets/sso.html?v=5';
    ssoDevIFrame.style = 'display:none';
    ssoDevIFrame.id = 'sso_dev';
    ssoDevContainer.appendChild(ssoDevIFrame);
}

/**
 * Takeover must be exported - we use it in node SSR also.
 */
var TAKEOVER = {
    init: function() {
        if (typeof this.onInit === "function") {
            this.onInit();
        }
    },
    destroy: function(id) {
        if (typeof this.onDestroy === "function") {
            this.onDestroy();
            this.onDestroy = null;
            this.onInit = null;
            var scriptToRemove = document.getElementById("takeover_" + id);

            if (scriptToRemove) {
                scriptToRemove.parentNode.removeChild(scriptToRemove);
            }
        }
    },
    cookies: {
        set: function(options) {
            var d = new Date();
            d.setTime(d.getTime() + (1000*options.TTL));
            var secure = window.location.protocol === 'http:' ? '' : '; secure';
            document.cookie = options.name + "=" + options.name + "; expires=" + d.toUTCString() + "; path=/; samesite: None" + secure;
        },
        get: function(cname) {
            var name = cname + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i <ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }

                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }

            return "";
        }
    }
};

try {
    module.exports = {
        TAKEOVER: TAKEOVER
    };
} catch (e) {}

/**
 * Ponyfill for IE11 css variables. Duuuuh.
 * CSS vars are used in settings and login / registrations.
 */
const hasNativeSupport = ((window || {}).CSS || {}).supports && window.CSS.supports('(--a: 0)');

if (!hasNativeSupport) {
    document.write('<script src="/assets/js/css-vars-ponyfill.min.js"><\/script>');
    setTimeout(function () {
        if (typeof cssVars === 'function') {
            cssVars();
        }
    }, 5000);
}
