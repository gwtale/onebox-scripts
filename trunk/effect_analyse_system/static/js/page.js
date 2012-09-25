function get_hour_data(data){
	$(".hero-unit .day").fadeIn(800)
        chart_hour = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_hour',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: document.getElementById("page_title").value,
                x: -20 //center
            },
            subtitle: {
                text: 'hourly',
                x: -20
            },
            xAxis: {
                categories: data.during
            },
            yAxis: {
                title: {
                    text: 'Rate'
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
                data: data.return_dict.onebox
            }, {
                name: 'Baidu',
                data: data.return_dict.baidu
            },{
                name: 'Google',
                data: data.return_dict.google
            },{
                name: 'QSS',
                data: data.return_dict.qss
            },{
                name: 'Other',
                data: data.return_dict.other
            }]
        });

}
function get_page_data(data){
	$(".hero-unit .day").fadeIn(800)
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: document.getElementById("page_title").value,
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
                    text: 'Rate'
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
                data: data.return_dict.onebox
            }, {
                name: 'Baidu',
                data: data.return_dict.baidu
            },{
                name: 'Google',
                data: data.return_dict.google
            },{
                name: 'QSS',
                data: data.return_dict.qss
            },{
                name: 'Other',
                data: data.return_dict.other
            }]
        });

}
$(document).ready(function(){
			$("#change_hour").click(function(){
				$.getJSON("/overview/get_hour_data",  
                  {key:document.getElementById("key_name").value,from:$("#hour_from").val(),to:$("#hour_to").val()
                  },  
                   function(data){
                   get_hour_data(data)
        }); 

			})
            $('.timepicker-1').timepicker({
                minuteStep: 1,
                template: 'modal',
                showSeconds: false,
                showMeridian: false
            });
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
         $.getJSON("/overview/get_page",  
                  {key:document.getElementById("key_name").value,from:start.toString('yyyy-MM-d'),to:end.toString('yyyy-MM-d')
                  },  
                   function(data){
                   get_page_data(data)
        }); 

    }
    );
	
});
    var chart1;
    $(document).ready(function() {
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: document.getElementById("page_title").value,
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
                    text: 'Rate'
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
    
    var chart_hour;
    $(document).ready(function() {
        chart_hour = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_hour',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: document.getElementById("page_title").value,
                x: -20 //center
            },
            subtitle: {
                text: 'hourly',
                x: -20
            },
            xAxis: {
                categories: JSON.parse(document.getElementById("during_hour").value.replace(/'/g, '"'))
            },
            yAxis: {
                title: {
                    text: 'Rate'
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
                data: JSON.parse(document.getElementById("hour_onebox").value)
            }, {
                name: 'Baidu',
                data: JSON.parse(document.getElementById("hour_baidu").value)
            },{
                name: 'Google',
                data: JSON.parse(document.getElementById("hour_google").value)
            },{
                name: 'QSS',
                data: JSON.parse(document.getElementById("hour_qss").value)
            },{
                name: 'Other',
                data: JSON.parse(document.getElementById("hour_other").value)
            }]
        });
    });


    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart_baidu_realtime;
        chart_baidu_realtime = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_baidu_realtime',
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
                text: 'Baidu '+document.getElementById("page_title").value+' Realtime'
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
        
           
        var chart_google_realtime;
        chart_google_realtime = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_google_realtime',
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
                text: 'Google '+document.getElementById("page_title").value+' Realtime'
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
   
        var chart_onebox_realtime;
        chart_onebox_realtime = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_onebox_realtime',
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
                text: 'Onebox '+document.getElementById("page_title").value+' Realtime'
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
   
        var chart_qss_realtime;
        chart_qss_realtime = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_qss_realtime',
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
                text: 'QSS '+document.getElementById("page_title").value+' Realtime'
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
        var chart_other_realtime;
        chart_other_realtime = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_other_realtime',
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
                text: 'Other '+document.getElementById("page_title").value+' Realtime'
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
    
