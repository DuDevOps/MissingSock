$(document).ready(function () {  
    console.log("asset.js loaded")
     }) ;

    function crud_assets(action, id, asset_id, asset_desc_id) {

        var url = "assets"
        var data_in = []

        if (action == "DELETE") {
            data_in = {
                "id": id
            }
        } else {
            if (asset_desc_id == "useID_to_get_value") {
                asset_id_id = "intxt_asset_id_" + id
                asset_id_val = document.getElementById(asset_id_id).value

                asset_desc_id = "intxt_asset_desc_" + id
                asset_desc = document.getElementById(asset_desc_id).value
            } else {
                // When called from called back function id for input text is set to rec count
                // when called from html id is set to basestation.id
                asset_desc = asset_desc_id
                asset_id_val = asset_id
            }
            data_in = {
                "id": id,
                "asset_desc": asset_desc,
                "asset_id": asset_id_val
            }
        }

        console.log(data_in)

        var data_json = JSON.stringify(data_in)
        errMsg = "oh no"

        $.ajax({
            type: action,
            url: url,
            data: data_json,
            contentType: "application/json; charset=utf-16",
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

    function addRowAssets(tableID) {

        var table = document.getElementById(tableID);

        var rowCount = table.rows.length;
        var row = table.insertRow(0);

        // create row specific for each page
        if (tableID == "tab_assets") {
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

                // get rowcount from element.id
                rowNumber = this.id.substring(9);

                // get id of inputbox for base id

                asset_id = "txtbox_asset_id_" + rowNumber
                asset_id_val = document.getElementById(asset_id).value

                // get id of inputbox for nickname

                asset_desc_id = "txtbox_asset_desc_id_" + rowNumber
                asset_desc_val = document.getElementById(asset_desc_id).value

                crud_assets("PUT", 'NoID', asset_id_val, asset_desc_val);
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
                deleteRowTags(tableID);
            }
            cell1.appendChild(element1);

            var cell3 = row.insertCell(2);
            var element2 = document.createElement("input");
            element2.type = "text";
            element2.name = "txtbox_asset_id";
            element2.placeholder = "asset name";
            element2.id = "txtbox_asset_id_" + rowCount;
            cell3.appendChild(element2);

            var cell4 = row.insertCell(3);
            var element3 = document.createElement("input");
            element3.type = "text";
            element3.name = "txtbox_asset_desc";
            element3.placeholder = "Description";
            element3.id = "txtbox_asset_desc_id_" + rowCount;
            cell4.appendChild(element3);

            var cell5 = row.insertCell(4);
            cell5.innerHTML = "! NEW ROW "

        }


    }

    function deleteRowTags(tableID) {
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
