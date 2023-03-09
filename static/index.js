chartRange = 720; // Number of visible points on chart = 60min * 60sec / 5


window.onload = () => {
    let data_points = [];
    fetch("/cpu_load").then(
        (response) => {
            response.json().then(
                (data) => {
                    for (let i = 0; i < data.length; i++) {
                        data[i]["x"] = new Date(data[i]["x"]);
                    }
                    data_points = data;
                    let chart = new CanvasJS.Chart("mainChartContainer", {
                        animationEnabled: true,
                        theme: "light2",
                        title:{
                            text: "CPU load"
                        },
                        data: [{        
                            type: "spline",
                            xValueFormatString: "hh:mm:ss",
                            indexLabelFontSize: 16,
                            dataPoints: data_points
                        }]
                    });


                    chart.render();

                    let updateChart = function() {
                        fetch("cpu_load_latest").then(
                            (response) => {
                                response.json().then(
                                    (new_point) => {
                                        console.log(new_point);
                                        new_point["x"] = new Date(new_point["x"]);
                                        data_points.push(new_point);
                                        if (data_points.length > chartRange){
                                            data_points.shift();
                                        }
                                        chart.render();
                                    }
                                );
                            }
                        );
                    }
                    setInterval(function(){ updateChart() }, 5000);
                }
            );
            
        });

        let avg_data_points = [];
    fetch("/cpu_load_avg").then(
        (response) => {
            response.json().then(
                (data) => {
                    for (let i = 0; i < data.length; i++) {
                        data[i]["x"] = new Date(data[i]["x"]);
                    }
                    avg_data_points = data;
                    let avg_chart = new CanvasJS.Chart("avgChartContainer", {
                        animationEnabled: true,
                        theme: "light2",
                        title:{
                            text: "Average CPU load"
                        },
                        data: [{        
                            type: "spline",
                            xValueFormatString: "hh:mm:ss",
                            indexLabelFontSize: 16,
                            dataPoints: avg_data_points
                        }]
                    });


                    avg_chart.render();

                    let updateAvgChart = function() {
                        fetch("cpu_load_avg_latest").then(
                            (response) => {
                                response.json().then(
                                    (new_point) => {
                                        console.log(new_point);
                                        new_point["x"] = new Date(new_point["x"]);
                                        avg_data_points.push(new_point);
                                        if (avg_data_points.length > 60){
                                            avg_data_points.shift();
                                        }
                                        avg_chart.render();
                                    }
                                );
                            }
                        );
                    }
                    
                    setInterval(function(){ updateAvgChart() }, 120000);
                }
            );
        });

    

}





