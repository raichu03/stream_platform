window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    var imgTag = decodeURIComponent(urlParams.get('img'));
    document.getElementById('imageContainer').innerHTML = imgTag;
};