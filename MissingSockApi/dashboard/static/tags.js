$(document).ready(function () {  
    console.log("tags.js loaded")
     }) ;

    function crud_tag(action, id, tag_id, nickname_id) {

        var url = "/tags"
        var data_in = []

        if (action == "DELETE") {
            data_in = {
                "id": id
            }
        } else {
            if (nickname_id == "useID_to_get_value") {
                nickname_id = "intxt_tag_nickname_" + id
                nickname = document.getElementById(nickname_id).value

                tag_id_id = "txtbox_tag_id_" + id
                tag_id_val = document.getElementById(tag_id_id).value
            } else {
                // When called from called back function id for input text is set to rec count
                // when called from html id is set to basestation.id
                nickname = nickname_id
                tag_id_val = tag_id
            }
            data_in = {
                "id": id,
                "nickname": nickname,
                "tag_id": tag_id_val
            }
        }

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

    function addRowTags(tableID) {

        var table = document.getElementById(tableID);

        var rowCount = table.rows.length;
        var row = table.insertRow(0);

        // create row specific for each page
        if (tableID == "tab_tags") {
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

                rowNumber = this.id.substring(9);

                // get id of inputbox for base id

                tag_id = "txtbox_tag_id_" + rowNumber
                tag_id_val = document.getElementById(tag_id).value

                // get id of inputbox for nickname

                nickname_id = "txtbox_nick_" + rowNumber
                nickname = document.getElementById(nickname_id).value

                crud_basestations("PUT", 'NoID', tag_id_val, nickname);
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
                deleteRowtag(tableID);
            }
            cell1.appendChild(element1);

            var cell3 = row.insertCell(2);
            var element2 = document.createElement("input");
            element2.type = "text";
            element2.name = "txtbox_tag_id";
            element2.placeholder = "tag id";
            element2.id = "txtbox_tag_id_" + rowCount;
            cell3.appendChild(element2);

            var cell4 = row.insertCell(3);
            var element3 = document.createElement("input");
            element3.type = "text";
            element3.name = "txtbox_nickname";
            element3.placeholder = "nick name";
            element3.id = "txtbox_nick_" + rowCount;
            cell4.appendChild(element3);

            var cell5 = row.insertCell(4);
            cell5.innerHTML = "! NEW ROW "

        }


    }

    function deleteRowtag(tableID) {
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
