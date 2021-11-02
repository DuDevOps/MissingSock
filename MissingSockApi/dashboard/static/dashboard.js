/* globals Chart:false, feather:false */

function render_maps_charts(loadHtml, loadJson) {

  if (loadHtml == "dashboard") {
    show_dashboard_map(loadJson);
    render_doughnut_graph('rep_Chart_1', 10, 20, 'chart 1');
    render_doughnut_graph('rep_Chart_2', 10, 20, 'chart 2');
    render_doughnut_graph('rep_Chart_3', 10, 20, 'chart 3');
  }

  if (loadHtml == "base_stations") {

    show_base_station_map(loadJson);

  }

}

function loadGraph() {
  'use strict'

  feather.replace({
    'aria-hidden': 'true'
  })

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#99ccff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}

function render_doughnut_graph(canvas_id, tags_seen, tag_total, base_id) {

  ctx = document.getElementById(canvas_id)

  const data = {
    labels: [
      'Total Tags(' + tag_total + ')',
      '' + base_id + ' Reads(' + tags_seen + ')'
    ],
    datasets: [{
      label: 'Tags Read',
      data: [tag_total, tags_seen],
      backgroundColor: [
        'rgb(54, 162, 235)',
        'rgb(0, 255, 0)'
      ],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  var myChart = new Chart(ctx, config)

}

// load bar chart 
if (document.getElementById('myChart')) {
  loadGraph()
}

// basestations.html render
if (document.getElementById('myBaseStationsChart')) {
  render_doughnut_graph('myBaseStationsChart', 10, 100, 'Base')
}

//  dashboard.html  render
function load_dashboard() {
  console.log("start load dashboard ")

  if (document.getElementById('ChartBaseStations')) {
    render_doughnut_graph('ChartBaseStations', 10, 100, 'Base')
  }

  if (document.getElementById('ChartTags')) {
    render_doughnut_graph('ChartTags', 10, 100, 'Base')
  }
}

// Add Maps
function show_dashboard_map(loadJson) {

  var map_dashboard = L.map('div_map_dashboard').setView([loadJson.middle_point.lat, loadJson.middle_point.long], 17);

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 100,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
  }).addTo(map_dashboard);

  // add base station markers

  stations = loadJson.base_stations

  for (let index = 0; index < loadJson.base_stations.length; ++index) {

    L.marker([parseFloat(stations[index].gps_lat), parseFloat(stations[index].gps_long)]).addTo(map_dashboard);

    // add circle
    var circle = L.circle([parseFloat(stations[index].gps_lat), parseFloat(stations[index].gps_long)], {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5,
      radius: 20
    }).addTo(map_dashboard);
  }

  // add popup on click
  var popup = L.popup();

  function onMapClick(e) {
    popup
      .setLatLng(e.latlng)
      .setContent("You clicked the map at " + e.latlng.toString())
      .openOn(map_dashboard);

    L.marker([e.latlng["lat"], e.latlng["lng"]]).addTo(map_dashboard);

  }

  map_dashboard.on('click', onMapClick);
}

function show_base_station_map(loadJson) {

  var map_basestation = L.map('div_map_basestation').setView([loadJson.middle_point.lat, loadJson.middle_point.long], 17);

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 100,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
  }).addTo(map_basestation);

  // add base station markers

  stations = loadJson.base_stations

  for (let index = 0; index < loadJson.base_stations.length; ++index) {

    L.marker([parseFloat(stations[index].gps_lat), parseFloat(stations[index].gps_long)]).addTo(map_basestation);

    // add circle
    var circle = L.circle([parseFloat(stations[index].gps_lat), parseFloat(stations[index].gps_long)], {
      color: 'white',
      fillColor: '#f0f5f1',
      fillOpacity: 0.2,
      radius: 20
    }).addTo(map_basestation);
  }

  // add popup on click
  var popup = L.popup();

  function onMapClick(e) {
    popup
      .setLatLng(e.latlng)
      .setContent("You clicked the map at " + e.latlng.toString())
      .openOn(map_basestation);

    L.marker([e.latlng["lat"], e.latlng["lng"]]).addTo(map_basestation);

  }

  map_basestation.on('click', onMapClick);

}