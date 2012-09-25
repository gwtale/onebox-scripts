var chart;
$(document).ready(function() {
    $("#main_form").fadeIn(800)
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
         $.getJSON("/clientinfo/get_setup_amounts",  
                  {from:start.toString('yyyy-MM-d'),to:end.toString('yyyy-MM-d')
                  },  
                   function(data){
                   get_setup_amounts(data)
                    
        }); 

    }
    );
        $('#setup_amounts').attr('class','active')
        $(".hero-unit").fadeIn(800)
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_setup_amounts',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: '客户端安装量',
                x: -20 //center
            },
            subtitle: {
                text: 'Source: oneboxtech.com',
                x: -20
            },
            xAxis: {
                categories: JSON.parse(document.getElementById("during").value.replace(/'/g, '"')) 
            },
            yAxis: {
                title: {
                    text: '安装数量(个)'
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
                        this.x +': '+ this.y +'个用户';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -20,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: '微博营销',
                data: JSON.parse(document.getElementById("weibo").value) 
            }, {
                name: 'SEO',
                data: JSON.parse(document.getElementById("seo").value) 
            }, {
                name: 'SEM',
                data: JSON.parse(document.getElementById("sem").value) 
            }]
        });
    });
function get_setup_amounts(data){
$(".hero-unit").fadeIn(800)
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_setup_amounts',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: '客户端安装量',
                x: -20 //center
            },
            subtitle: {
                text: 'Source: oneboxtech.com',
                x: -20
            },
            xAxis: {
                categories: data.result.during 
            },
            yAxis: {
                title: {
                    text: '安装数量(个)'
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
                        this.x +': '+ this.y +'个用户';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -20,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: '微博营销',
                data: data.result.weibo
            }, {
                name: 'SEO',
                data: data.result.seo
            }, {
                name: 'SEM',
                data: data.result.sem
            }]
        });


}