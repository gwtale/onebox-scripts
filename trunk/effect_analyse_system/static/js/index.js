function get_click_and_search_amounts(data){
	$(".hero-unit .day").fadeIn(800)
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_click',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Click Amounts',
                x: -20 //center
            },
            subtitle: {
                text: 'daily',
                x: -20
            },
            xAxis: {
                categories: data.during
            },
            yAxis: {
                title: {
                    text: 'Amounts'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y ;
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Onebox',
                data: data.click_result.onebox
            }, {
                name: 'Baidu',
                data: data.click_result.baidu
            },{
                name: 'Google',
                data: data.click_result.google
            },{
                name: 'QSS',
                data: data.click_result.qss
            },{
                name: 'Other',
                data: data.click_result.other
            }]
        });

        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_search',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Search Amounts',
                x: -20 //center
            },
            subtitle: {
                text: 'daily',
                x: -20
            },
            xAxis: {
                categories: data.during
            },
            yAxis: {
                title: {
                    text: 'Amounts'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y;
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Onebox',
                data: data.search_result.onebox
            }, {
                name: 'Baidu',
                data: data.search_result.baidu
            },{
                name: 'Google',
                data: data.search_result.google
            },{
                name: 'QSS',
                data: data.search_result.qss
            },{
                name: 'Other',
                data: data.search_result.other
            }]
        });


}
$(document).ready(function(){
	    $('#reportrange').daterangepicker(
    {
        ranges: {
            'Last 7 Days': [Date.today().add({ days: -6 }), 'today'],
            'Last 30 Days': [Date.today().add({ days: -29 }), 'today'],
            'This Month': [Date.today().moveToFirstDayOfMonth(), Date.today().moveToLastDayOfMonth()],
            'Last Month': [Date.today().moveToFirstDayOfMonth().add({ months: -1 }), Date.today().moveToFirstDayOfMonth().add({ days: -1 })]
        }
    }, 
    function(start, end) {
        $('#reportrange span').html(start.toString('yyyy-MM-d') + ' -> ' + end.toString('yyyy-MM-d'));
         $.getJSON("/overview/get_click_and_search_amounts",  
                  {from:start.toString('yyyy-MM-d'),to:end.toString('yyyy-MM-d')
                  },  
                   function(data){
                   get_click_and_search_amounts(data)
        }); 

    }
    );
	
});
var window_overview;
$(document).ready(function() {

    window_overview = new Highcharts.Chart({
                
        chart: {
            renderTo: 'chart_overview',
            polar: true,
            type: 'line'
        },
        
        title: {
            text: 'Onebox vs QSS',
            x: -80
        },
        
        pane: {
            size: '80%'
        },
        
        xAxis: {
            categories: ['总点击次数', '总搜索次数', '点击率', '无点击率', 
                    'Top3点击率', '翻页率','有翻页的搜索比例','query更改率'],
            tickmarkPlacement: 'on',
            lineWidth: 0
        },
            
        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0
        },
        
        tooltip: {
            shared: true,
            valuePrefix: '$'
        },
        
        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 100,
            layout: 'vertical'
        },
        
        series: [{
            name: 'Onebox',
            data: [43000, 19000, 600,400, 35,4000, 17000, 10000],
            pointPlacement: 'on'
        }, {
            name: '很挫的QSS',
            data: [50000, 39000, 42000, 310,400, 24,6000, 14000],
            pointPlacement: 'on'
        }]
    
    });
}

    var chart1;
    $(document).ready(function() {
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_click',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Click Amounts',
                x: -20 //center
            },
            subtitle: {
                text: 'daily',
                x: -20
            },
            xAxis: {
                categories: JSON.parse(document.getElementById("during").value.replace(/'/g, '"'))
            },
            yAxis: {
                title: {
                    text: 'Amounts'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y ;
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Onebox',
                data: JSON.parse(document.getElementById("click_onebox").value)
            }, {
                name: 'Baidu',
                data: JSON.parse(document.getElementById("click_baidu").value)
            },{
                name: 'Google',
                data: JSON.parse(document.getElementById("click_google").value)
            },{
                name: 'QSS',
                data: JSON.parse(document.getElementById("click_qss").value)
            },{
                name: 'Other',
                data: JSON.parse(document.getElementById("click_other").value)
            }]
        });
    });
    
    var chart2;
    $(document).ready(function() {
        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_search',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Search Amounts',
                x: -20 //center
            },
            subtitle: {
                text: 'daily',
                x: -20
            },
            xAxis: {
                categories: JSON.parse(document.getElementById("during").value.replace(/'/g, '"'))
            },
            yAxis: {
                title: {
                    text: 'Amounts'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y;
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Onebox',
                data: JSON.parse(document.getElementById("search_onebox").value)
            }, {
                name: 'Baidu',
                data: JSON.parse(document.getElementById("search_baidu").value)
            },{
                name: 'Google',
                data: JSON.parse(document.getElementById("search_google").value)
            },{
                name: 'QSS',
                data: JSON.parse(document.getElementById("search_qss").value)
            },{
                name: 'Other',
                data: JSON.parse(document.getElementById("search_other").value)
            }]
        });
    });

    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart3;
        chart3 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_click_realtime',
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function() {
    
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
                            var x = (new Date()).getTime(), // current time
                                y = Math.random();
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Total Click Realtime'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Random data',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
    
                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                })()
            }]
        });
    });
    

    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart4;
        chart4 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_total_search_realtime',
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function() {
    
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
                            var x = (new Date()).getTime(), // current time
                                y = Math.random();
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Total Search Realtime'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Random data',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
    
                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                })()
            }]
        });
    });
    


