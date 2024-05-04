

window.onload = function() {

    /////// create a map and set the view to a specific location //////
    var map = L.map('map').setView([27.647621, 85.620282], 14);
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
            marker = L.marker([element['lat'], element['long']], {alt: 'locator'}).addTo(map)
            .bindPopup(`${element['classe']} was detected at ${element['date']}`);
        });
    })


}