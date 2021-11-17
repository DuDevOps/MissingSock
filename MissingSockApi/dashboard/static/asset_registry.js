$(document).ready(function () {
    console.log("asset_registry.js loaded")
});

function crud_asset_registry(action, id, tableID) {

    var url = "/asset_registry"
    var data_in = []

    var tableForm = document.getElementById(id);
    var tableRow = tableForm.closest('tr')

    

    console.log(data_in)

    var data_json = JSON.stringify(data_in)
    errMsg = "oh no"

    $.ajax({
        type: action,
        url: url,
        data: data_json,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log("success for " + data_in);
        },
        failure: function (errMsg) {
            console.log("error ajax call : " + errMsg);
        }
    });

}

// Add / remove row from table

function addRow_asset_registry(tableID, list_of_cols) {

    var table = document.getElementById(tableID);

    var rowCount = table.rows.length;
    var row = table.insertRow(0);

    // create row specific for each page
    if (tableID == "tab_asset_registry") {
        // ins button
        var cell1 = row.insertCell(0);
        var element1 = document.createElement("button");
        element1.type = "submit";
        element1.id = "insertBtn" + rowCount;
        element1.innerHTML = "Insert";
        element1.classList.add("btn");
        element1.classList.add("btn-danger");
        element1.classList.add("btn-sm");
        element1.onclick = function () {

            crud_asset_registry("PUT", "input_text_ins_id_" + rowCount , tableID );
        }
        cell1.appendChild(element1);

        // reset button
        var cell1 = row.insertCell(0);
        var element1 = document.createElement("button");
        element1.type = "submit";
        element1.id = "resetBtn_" + rowCount;
        element1.innerHTML = "Reset";

        element1.classList.add("btn");
        element1.classList.add("btn-info");
        element1.classList.add("btn-sm");
        element1.onclick = function () {
            element1.classList.add("active-reset");
            delete_Rowasset_registry(tableID);
        }
        cell1.appendChild(element1);

        var col_counter = 2

        for (col in  list_of_cols) {

        var cell = row.insertCell(col_counter);
        var element = document.createElement("input");
        element.type = "text";
        element.name = "txtbox_asset_registry_id";
        element.placeholder = "" + list_of_cols[col] ;
        element.id = "input_text_ins_" +col +"_" +rowCount ; // unique id - _ins_ added
        cell.appendChild(element);

        col_counter = col_counter + 1

        }


        var cell = row.insertCell(col_counter);
        cell.innerHTML = "! NEW ROW "

    }


}

function delete_Rowasset_registry(tableID) {
    try {
        var table = document.getElementById(tableID);
        var rowCount = table.rows.length;

        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var class_active_reset = row.cells[0].getElementsByClassName("active-reset").length;
            if (class_active_reset != 0) {
                table.deleteRow(i);
                rowCount--;
                i--;
            }


        }
    } catch (e) {
        alert(e);
    }
}