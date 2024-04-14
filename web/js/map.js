window.onload = function() {
    L.mapquest.key = '8nIoYUx9GyjZsdehJySzjprSvZIqgM42';

    var map = L.mapquest.map('map', {
      center: [27.648863, 85.623033],
      layers: L.mapquest.tileLayer('map'),
      zoom: 14
    });

    map.addControl(L.mapquest.control());
  }