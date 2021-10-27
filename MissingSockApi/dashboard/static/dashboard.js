/* globals Chart:false, feather:false */



function loadGraph() {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

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

function render_doughnut_graph(canvas_id, tags_seen, tag_total, base_id ){
  
  ctx = document.getElementById(canvas_id)

  const data = {
    labels: [
      'Total Tags('+tag_total+')',
      ''+ base_id +' Reads('+tags_seen+')'
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
 
  var myChart = new Chart(ctx, config )

}

// load bar chart 
if ( document.getElementById('myChart') ) {
  loadGraph()
}

// basestations.html render
if ( document.getElementById('myBaseStationsChart') ) {
  render_doughnut_graph('myBaseStationsChart',10,100, 'Base')
}

//  dashboard.html  render
function load_dashboard() {
console.log("start load dashboard ")

if ( document.getElementById('ChartBaseStations') ) {
  render_doughnut_graph('ChartBaseStations',10,100, 'Base')
}

if ( document.getElementById('ChartTags') ) {
  render_doughnut_graph('ChartTags',10,100, 'Base')
}
}
