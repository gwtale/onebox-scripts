$(document).ready(function() {
    $("#main_form").fadeIn(800)
    $('#online_users').attr('class','active')
    
     $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart1;
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_online_users',
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function() { 
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        var y=Math.random();
                        setInterval(function() {
                        $.getJSON("/userinfo/get_online_users", {},  
                        function(data){
                               y=data.result
                        });
                            var x = (new Date()).getTime(); // current time
                                
                            series.addPoint([x, y], true, true);
                        }, 5000);
                    }
                }
            },
            title: {
                text: '用户实时在线情况(所有客户端)'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: '在线用户数'
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
                        Highcharts.numberFormat(this.y, 0);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: '实时在线人数',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
    
                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.floor(Math.random() * 100 + 10)
                        });
                    }//旧数据
                    return data;
                })()
            }]
        });
    });

});

    
    var chart;
 $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_online_users_share_weibo',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '当前(非实时)微博客户端在线用户所在比例'
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'User Info Share',
                data: [
                    ['试用用户',   JSON.parse(document.getElementById("weibo_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("weibo_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("weibo_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("weibo_crack").value)],
                ]
            }]
        });
    });

   var chart1;
 $(document).ready(function() {
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_online_users_share_seo',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '当前(非实时)SEO客户端在线用户所在比例'
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'User Info Share',
                data: [
                    ['试用用户',   JSON.parse(document.getElementById("seo_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("seo_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("seo_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("seo_crack").value)],
                ]
            }]
        });
    });
    
       var chart2;
 $(document).ready(function() {
        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_online_users_share_sem',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '当前(非实时)SEM客户端在线用户所在比例'
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'User Info Share',
                data: [
                    ['试用用户',   JSON.parse(document.getElementById("sem_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("sem_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("sem_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("sem_crack").value)],
                ]
            }]
        });
    });