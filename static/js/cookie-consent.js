const CONSENT_KEY = 'motiknit_cookie_consent';

function loadPinterestTag() {
    if (window.pintrkLoaded) return;
    window.pintrkLoaded = true;
    !function(e){if(!window.pintrk){window.pintrk = function () {
    window.pintrk.queue.push(Array.prototype.slice.call(arguments))};var
      n=window.pintrk;n.queue=[],n.version="3.0";var
      t=document.createElement("script");t.async=!0,t.src=e;var
      r=document.getElementsByTagName("script")[0];
      r.parentNode.insertBefore(t,r)}}("https://s.pinimg.com/ct/core.js");
    pintrk('load', '2613768165803');
    pintrk('page');
}

function grantConsent() {
    gtag('consent', 'update', {
        'ad_storage': 'granted',
        'ad_user_data': 'granted',
        'ad_personalization': 'granted',
        'analytics_storage': 'granted'
    });
    loadPinterestTag();
}

document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('cookieConsent');
    const acceptButton = document.getElementById('cookieAccept');
    const declineButton = document.getElementById('cookieDecline');
    const consent = localStorage.getItem(CONSENT_KEY);

    if (consent === 'accepted') {
        grantConsent();
    } else if (consent !== 'declined') {
        banner.style.display = 'flex';
    }

    acceptButton.addEventListener('click', function() {
        localStorage.setItem(CONSENT_KEY, 'accepted');
        banner.style.display = 'none';
        grantConsent();
    });

    declineButton.addEventListener('click', function() {
        localStorage.setItem(CONSENT_KEY, 'declined');
        banner.style.display = 'none';
    });
});
