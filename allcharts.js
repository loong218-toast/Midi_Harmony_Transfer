import Chart from 'chart.js/auto';
import $ from 'jquery'


var myChart
var velocityChart

export default class chart_class {

    notes_chart(){
    
        let ctx = document.getElementById('myChart').getContext('2d');

        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'],
                datasets: [{
                    label: 'Notes Distribution',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(210, 100, 200, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(210, 100, 200, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(210, 100, 200, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(210, 100, 200, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(210, 100, 200, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 159, 64, 1)',
                        'rgba(200, 130, 200, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(200, 130, 200, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(200, 130, 200, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(200, 130, 200, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(200, 130, 200, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Notes'
                          }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Distribution'
                          },
                        beginAtZero: true,
                        ticks: {
                            format: {
                                style: 'percent'
                            }
                        }
                    },
                    
                }
            }
        });
    }

    velocity_chart(){
        let ctx = document.getElementById('velocity-canvas').getContext('2d');

        velocityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Velocity',
                    data: [],
                    backgroundColor: [
                        'rgba(130, 180, 220, 0.2)'
                    ],
                    borderColor: [
                        'rgba(130, 180, 220, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time(sec)'
                          }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Velocity'
                          },
                        
                        beginAtZero: true,
                    },
                    
                }
            }
        });
        ctx.canvas.width = 300;
        ctx.canvas.height = 300;
    }

    update_notes_chart(json){
        $("#key-text").text(json[1].key + json[2].key2)
        $("#tempo-text").text(json[3].tempo)
        $("#timelength-text").text(json[4].time_length)

        let pitch_dist_arr = []
        for(let i = 0 ;i < 12 ;i++){
            pitch_dist_arr.push(Object.values(json[0].pitch_dist)[i] / 100)
        }
        
        myChart.data.datasets[0].data = pitch_dist_arr
        velocityChart.data.labels = Object.keys(json[5])
        velocityChart.data.datasets[0].data = Object.values(json[5])
        
        myChart.update();
        velocityChart.update();

    }

}