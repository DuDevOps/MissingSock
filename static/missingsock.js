$(document).ready(function () {
    console.log("missing_sock.js loaded");
});


/* globals Chart:false, feather:false */

function render_maps_charts(loadHtml, loadJson) {

    loadJson = JSON.parse(loadJson)

    if (loadHtml == "dashboard") {
        show_map("div_map_rep_dashboard",
            loadJson.tags[0].gps_lat,
            loadJson.tags[0].gps_long,
            13, loadJson.tags,
            loadJson.total_tags)

        render_doughnut_graph("rep_dashboard_Chart_1",
            loadJson.tags_read,
            loadJson.total_tags)

        render_doughnut_graph("rep_dashboard_Chart_2",
            loadJson.tags_read_48,
            loadJson.total_tags)

    } else if (loadHtml == "report_overview") {

        show_map("div_map_rep_overview",
            loadJson.tags[0].gps_lat,
            loadJson.tags[0].gps_long,
            13, loadJson.tags,
            loadJson.total_tags)

        render_doughnut_graph("rep_overview_Chart_1",
            loadJson.tags_read,
            loadJson.total_tags)

        render_doughnut_graph("rep_overview_Chart_2",
            loadJson.tags_read_48,
            loadJson.total_tags)


    } else if (loadHtml == "report_tags") {
        show_map("div_map_rep_tags",
            loadJson.tags[0].gps_lat,
            loadJson.tags[0].gps_long,
            13, loadJson.tags,
            loadJson.total_tags)

        render_doughnut_graph("rep_tags_Chart_1",
            loadJson.tags_read,
            loadJson.total_tags)


        render_doughnut_graph("rep_tags_Chart_2",
            loadJson.tags_read_48,
            loadJson.total_tags)
    } else if (loadHtml == "report_base_station") {
        show_map("div_map_rep_base_station",
            loadJson.base_stations[0].gps_lat,
            loadJson.base_stations[0].gps_long,
            13, loadJson.base_stations,
            loadJson.total_tags)

        render_doughnut_graph("rep_base_station_Chart_1",
            loadJson.total_base_stations,
            loadJson.total_tags)


        render_doughnut_graph("rep_base_station_Chart_2",
            loadJson.tags_read_48_all_base_stations,
            loadJson.total_tags)
    } else {
        console.log("loadHtml is missing or not matched in loadJson")
        console.log(loadJson)
    }

}

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

function toggle_class_show(div_id){
    $("#"+div_id).toggle() ;
}