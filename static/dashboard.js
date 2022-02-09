$(document).ready(function () {
  console.log("dashboard.js loaded");
});


/* globals Chart:false, feather:false */

function old_render_maps_charts(loadHtml, loadJson) {

  if (loadHtml == "dashboard") {
    var total_tags = loadJson.total_tags

    show_dashboard_map(loadJson);
    render_doughnut_graph('rep_Chart_1', loadJson.total_hours_1, total_tags, 'Tags');
  }

  if (loadHtml == "base_stations") {

    show_base_station_map(loadJson);

  }

  if (loadHtml == "report_no_read_tag_hour") {
    var total_tags = loadJson.total_tags

    show_base_station_map(loadJson);
    render_doughnut_graph('rep_Chart_1', loadJson.total_hours_1, total_tags, 'Tags');
    render_doughnut_graph('rep_Chart_2', loadJson.total_days_1, total_tags, 'Tags');
    render_doughnut_graph('rep_Chart_3', loadJson.total_stations_days_1, loadJson.total_stations, 'Base');

  }

  if (loadHtml == "report_no_read_base_hour") {
    var total_tags = loadJson.total_tags

    show_base_station_map(loadJson);
    render_doughnut_graph('rep_Chart_1', loadJson.total_hours_1, total_tags, 'Base');
    render_doughnut_graph('rep_Chart_2', loadJson.total_days_1, total_tags, 'Base');
    render_doughnut_graph('rep_Chart_3', loadJson.total_stations_days_1, loadJson.total_stations, 'Base');

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

function render_doughnut_graph(canvas_id, tags_not_seen, tag_total, base_id) {

  ctx = document.getElementById(canvas_id)

  const data = {
    labels: [
      '' + base_id + ' Read (' + (tag_total - tags_not_seen) + ')',
      '' + base_id + ' not Read (' + tags_not_seen + ')'
    ],
    datasets: [{
      label: base_id,
      data: [(tag_total - tags_not_seen), tags_not_seen],
      backgroundColor: [
        'rgb(0, 255, 0)',
        'rgb(222, 74, 51)'
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


// Add Maps
function show_dashboard_map(loadJson) {

  var total_tag = loadJson.total_tags
  var fillOpacity_value = 0
  var map_dashboard = L.map('div_map_dashboard').setView([loadJson.middle_point.lat, loadJson.middle_point.long], 15);


  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 100,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
  }).addTo(map_dashboard);

  // add tag markers

  tags = loadJson.tags;
  tag_count = loadJson.tags.length

  for (let index = 0; index < loadJson.tags.length; ++index) {

    fillOpacity_value = 0;

    var asset_base_id = tags[index].base_station_id
    var asset_name = tags[index].name
    var asset_type = tags[index].asset_type
    var gps_lat = tags[index].gps_lat
    var gps_long = tags[index].gps_long


    var marker = L.marker([parseFloat(gps_lat), parseFloat(gps_long)]).addTo(map_dashboard);

    // add on click popup
    marker.bindPopup("Name :" + asset_name + "(" + asset_type + ") @" + "GPS: lat " + gps_lat + " / long " + gps_long);

    // Add label
    marker.bindTooltip("" + asset_name + "(" + asset_type + ") : tags (" + tag_count + ")", {
      permanent: true,
      direction: 'right'
    });

    // add circle
    var tagcount = loadJson.tags.length;

    if (parseFloat(tagcount)) {
      fillOpacity_value = parseFloat(tagcount) / parseFloat(total_tag);
    }

    var circle = L.circle([parseFloat(tags[index].gps_lat), parseFloat(tags[index].gps_long)], {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: fillOpacity_value,
      radius: 30
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

  map_dashboard.on('xclick', onMapClick);
}

function show_base_station_map(loadJson) {

  var map_basestation = L.map('div_map_basestation').setView([loadJson.middle_point.lat, loadJson.middle_point.long], 14);

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

    marker = L.marker([parseFloat(stations[index].gps_lat), parseFloat(stations[index].gps_long)]).addTo(map_basestation);

    marker.bindPopup("Marker - 1");

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

  map_basestation.on('xclick', onMapClick);

}