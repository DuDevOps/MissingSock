function show_map(map_div_id, map_lat, map_long, zoom=15, tags, json_total_tags) {

    var total_tag = json_total_tags
    var fillOpacity_value = 0
    var map_dashboard = L.map(map_div_id).setView([map_lat, map_long], zoom);
  
  
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 100,
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1
    }).addTo(map_dashboard);
  
    // add tag markers
  
    tags = tags;
    tag_count = tags.length
  
    for (let index = 0; index < tags.length; ++index) {
  
      fillOpacity_value = 0;
  
      var gps_lat = tags[index].gps_lat
      var gps_long = tags[index].gps_long
  
  
      var marker = L.marker([parseFloat(gps_lat), parseFloat(gps_long)]).addTo(map_dashboard);
  
      // add on click popup
      //marker.bindPopup("Name :" + asset_name + "(" + asset_type + ") @" + "GPS: lat " + gps_lat + " / long " + gps_long);
  
      // Add label
    //   marker.bindTooltip("" + asset_name + "(" + asset_type + ") : tags (" + tag_count + ")", {
    //     permanent: true,
    //     direction: 'right'
    //   });
  
      // add circle
    //   var tagcount = loadJson.tags.length;
  
    //   if (parseFloat(tagcount)) {
    //     fillOpacity_value = parseFloat(tagcount) / parseFloat(total_tag);
    //   }
  
    //   var circle = L.circle([parseFloat(tags[index].gps_lat), parseFloat(tags[index].gps_long)], {
    //     color: 'red',
    //     fillColor: '#f03',
    //     fillOpacity: fillOpacity_value,
    //     radius: 30
    //   }).addTo(map_dashboard);
    } // end add tag markers
} // end show_map