<div> <!-- Stat Div produce -->
    <h6 class=" pm-2 "> <i class="fa fa-baby"></i>Produce {{asset.asset_produce|length}} </h6>
    <form>
        <div class="form-row">

            <div class="table-responsive overflow-auto" style="max-height: 100px ;">

            <table class="table table-info table-striped">
                <thead>
                    <th>timestamp</th>
                    <th>Type of Produce</th>
                    <th>Yield</th>
                    <th>Measurement </th>
                    <th>Notes</th>
                    
                </thead>

                {% for rec in asset.asset_produce %}
                <tr>
                    <td class="">
                        <div class="form-group ">
                            <input type="text" class="form-control" id="timestamp"
                                value="{{rec.timestamp}}">
                        </div>
                    </td>

                    <td class="">
                        <div class="form-group ">
                            <input type="text" class="form-control" id="type"
                                value="{{rec.type}}">
                        </div>
                    </td>

                    <td class="">
                        <div class="form-group ">
                            <input type="text" class="form-control" id="produce_yield"
                                value="{{rec.produce_yield}}">
                        </div>
                    </td>

                    <td class="">
                        <div class="form-group ">
                            <input type="text" class="form-control" id="measurement"
                                value="{{rec.measurement}}">
                        </div>
                    </td>

                    <td class="">
                        <div class="form-group ">
                            <input type="text" class="form-control" id="note"
                                value="{{rec.note}}">
                        </div>
                    </td>
                </tr>

                {% endfor %}
                <!-- end produce rec -->

            </table>
        </div> <!-- end div table -->

</div> <!-- end form row-->

</form>
</div> <!-- end div produce -->