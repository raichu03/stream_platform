function elementFromHtml(html) {

  const template = document.createElement('template');
  template.innerHTML = html.trim();
  return template.content.firstElementChild;
}

function create_html(total){

  const feed = document.querySelector('.container')

  for (var i = 0; i < total; i++) {
    const myHtml = elementFromHtml(`
      <div class="level-showcase" onclick="singleFeed(event)">
        <dev class="video-hadler">
          <div class="video-item">
            <img src="http://127.0.0.1:8000/video/${i}">
          </div>
        </dev>
      </div>
  `);
    feed.appendChild(myHtml);
  }

};

window.onload = function () {

  let p = fetch('http://127.0.0.1:8000/stream_number')
  p.then(response => {
    return response.json();
  }).then(data => {
    create_html(data);
  });
};

function singleFeed(event) {

  const img = event.target.src;
  var imgTag = `<img src="${img}">`
  var encodedImg = encodeURIComponent(imgTag)
  window.location.href = "singleFeed.html?img=" + encodedImg;

}