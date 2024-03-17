function elementFromHtml(html) {

  const template = document.createElement('template');
  template.innerHTML = html.trim();
  return template.content.firstElementChild;
};

function create_html(data){
  
  const feed = document.querySelector('.conatainer')

  for (var i = 0; i < data.length; i++) {
        
    loc = data[i].location;
    url = data[i].url;
    date = data[i].date;
    id = data[i].id;

    const myHtml = elementFromHtml(`
      <div class="data-holder">
        <div class="holder" id="location" contenteditable="true">${loc}</div>
        <div class="holder" id="url" contenteditable="true">${url}</div>
        <div class="holder" id="date" contenteditable="true">${date}</div>
        <div class="holder" id="id">${id}</div>
        <div class="save-button" onclick="update_data(this)">Save</div>
        <div class="delete-button" onclick="delete_data(this)">Delete</div>
      </div>
    `);
      feed.appendChild(myHtml);
    } 
};

window.onload = function () {
  let p = fetch('http://127.0.0.1:8000/streams')
  p.then(response => {
    return response.json();
  }).then(data => {
    create_html(data);
  });
};

function addNew(){

  const feed = document.querySelector('.add-conatainer')
  console.log("addData");
  const myHtml = elementFromHtml(`
      <div class="data-holder">
        <div class="holder" id="location" contenteditable="true">add location</div>
        <div class="holder" id="url" contenteditable="true">add video</div>
        <div class="holder" id="date" contenteditable="true">add date</div>
        <div class="save-button" onclick="addData(this)">Save</div>
      </div>
    `);
      feed.appendChild(myHtml);

};

function put_data(data, id){

  url = `http://127.0.0.1:8000/streams/${id}`
  
  const options = {
    method : 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body : JSON.stringify(data)
  }

  fetch(url, options)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    window.location.reload();
  })

};

function update_data(element) {
  const data = element.parentElement;
  const location = data.querySelector('#location').textContent;
  const url = data.querySelector('#url').textContent;
  const date = data.querySelector('#date').textContent;
  const id = data.querySelector('#id').textContent;

  const upload = {
    "url": url,
    "location": location,
    "date": date
  }
  put_data(upload, id);
};

function post_data(data){
  url = `http://127.0.0.1:8000/streams`

  const options = {
    method : 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body : JSON.stringify(data)
  }

  fetch(url, options)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    window.location.reload();
  })

};


function addData(element) {
  const data = element.parentElement;
  const location = data.querySelector('#location').textContent;
  const url = data.querySelector('#url').textContent;
  const date = data.querySelector('#date').textContent;

  const upload = {
    "url": url,
    "location": location,
    "date": date
  }
  post_data(upload);

};



function delete_data(element){
  const data = element.parentElement;
  const id = data.querySelector('#id').textContent;
  console.log(id);

  url = `http://127.0.0.1:8000/streams/${id}`
  
  const options = {
    method : 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
  }

  fetch(url, options)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    window.location.reload();
  })
};
