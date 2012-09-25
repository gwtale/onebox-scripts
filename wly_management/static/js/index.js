 var chart2;
    $(document).ready(function() {
    sum_weibo=0;
    $.each(JSON.parse(document.getElementById("money_weibo").value),function() {sum_weibo += this;});
    sum_seo=0;
    $.each(JSON.parse(document.getElementById("money_seo").value),function() {sum_seo += this;});
    sum_sem=0;
    $.each(JSON.parse(document.getElementById("money_sem").value),function() {sum_sem += this;});
    
        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_overview_money'
            },
            title: {
                text: '收入总览(近5周)'
            },
            xAxis: {
                categories: ['WEEK1', 'WEEK2', 'WEEK3', 'WEEK4', 'WEEK5']
            },
            tooltip: {
                formatter: function() {
                    var s;
                    if (this.point.name) { // the pie chart
                        s = ''+
                            this.point.name +': '+ this.y +' 元';
                    } else {
                        s = ''+
                            this.x  +': '+ this.y;
                    }
                    return s;
                }
            },
            labels: {
                items: [{
                    html: '各客户端占总收入比例',
                    style: {
                        left: '40px',
                        top: '8px',
                        color: 'black'
                    }
                }]
            },
            series: [{
                type: 'column',
                name: '微博营销',
                data: JSON.parse(document.getElementById("money_weibo").value)
            }, {
                type: 'column',
                name: 'SEO',
                data: JSON.parse(document.getElementById("money_seo").value)
            }, {
                type: 'column',
                name: 'SEM',
                data: JSON.parse(document.getElementById("money_sem").value)
            }, {
                type: 'spline',
                name: '总收入',
                data: JSON.parse(document.getElementById("money_total").value)
            }, {
                type: 'pie',
                name: 'Total consumption',
                data: [{
                    name: '微博营销',
                    y:sum_weibo ,
                    color: '#4572A7' // Jane's color
                }, {
                    name: 'SEO',
                    y: sum_seo,
                    color: '#AA4643' // John's color
                }, {
                    name: 'SEM',
                    y: sum_sem,
                    color: '#89A54E' // Joe's color
                }],
                center: [100, 80],
                size: 100,
                showInLegend: false,
                dataLabels: {
                    enabled: false
                }
            }]
        });
    });

$(document).ready(function() {
    $("#main_form").fadeIn(800)
    $("#overview-top").attr('class','active')
    
     var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_overview_clients',
                type: 'bar'
            },
            title: {
                text: '三大客户端安装量'
            },
            subtitle: {
                text: 'Source: oneboxtech.com'
            },
            xAxis: {
                categories: ['微博营销', 'SEO', 'SEM'],
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: '装机量 (个)',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.series.name +': '+ this.y +' 个';
                }
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -100,
                y: 100,
                floating: true,
                borderWidth: 1,
                backgroundColor: '#FFFFFF',
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                name: '正式用户',
                data: [JSON.parse(document.getElementById("weibo_normal").value),JSON.parse(document.getElementById("seo_normal").value), JSON.parse(document.getElementById("sem_normal").value)]
            }, {
                name: '试用用户',
                data: [JSON.parse(document.getElementById("weibo_try").value),JSON.parse(document.getElementById("seo_try").value), JSON.parse(document.getElementById("sem_try").value)]
            }, {
                name: '停用用户',
                data: [JSON.parse(document.getElementById("weibo_stop").value),JSON.parse(document.getElementById("seo_stop").value), JSON.parse(document.getElementById("sem_stop").value)]
            }, {
                name: '非法用户',
                data: [JSON.parse(document.getElementById("weibo_crack").value),JSON.parse(document.getElementById("seo_crack").value), JSON.parse(document.getElementById("sem_crack").value)]
            }]
        });
    });

});

