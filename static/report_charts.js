function render_doughnut_graph(canvas_id, tags_read, total_tags) {

    ctx = document.getElementById(canvas_id)
  
    const data = {
      labels: [
        ' Read (' + tags_read + ')',
        ' not Read (' + (total_tags - tags_read) + ')'
      ],
      datasets: [{
        label: "base_id",
        data: [tags_read, (total_tags - tags_read)],
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