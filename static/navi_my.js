$(document).ready(function () {
    console.log("navi_my.js loaded")
});

function toggle_class_show(id) {

    if ( document.getElementById(id).classList.contains("show") ){
        console.log(id + " - already has class show")
    }
    else {
        document.getElementById(id).classList.add("show");
        console.log(" class show has been added " + id)
    }

}
