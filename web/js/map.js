

window.onload = function() {

    /////// create a map and set the view to a specific location //////
    var map = L.map('map').setView([51.505, -0.09], 13);
    var marker;

    /////// add a tile layer to the map //////
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    /////// fetch locations from the server and add them to the map //////
    let p = fetch('http://127.0.0.1:8000/locations')
    p.then(responses => {
        return responses.json();
    }).then(data => {

        data.forEach(element => {
            // console.log(element[0]);
            marker = L.marker([element[0], element[1]], {alt: 'locator'}).addTo(map)
            .bindPopup('This is a auto-generated location');
        });
    })


}