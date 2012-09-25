$(document).ready(function() {
    $("#main_form").fadeIn(800)
    $('#paidinfo').attr('class','active')
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_paidinfo',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '付费情况'
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
                    ['试用用户',   JSON.parse(document.getElementById("try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("crack").value)],
                ]
            }]
        });
    });
});

