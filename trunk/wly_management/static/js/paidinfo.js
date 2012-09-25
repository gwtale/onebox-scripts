$(document).ready(function() {
    $("#main_form").fadeIn(800)
    $('#paidinfo').attr('class','active')
    var chart1;
    $(document).ready(function() {
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_paidinfo_weibo',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '微博客户端付费情况'
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
                    ['试用用户',   JSON.parse(document.getElementById("w_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("w_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("w_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("w_crack").value)],
                ]
            }]
        });
    });


    var chart2;
    $(document).ready(function() {
        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_paidinfo_seo',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'SEO付费情况'
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
                    ['试用用户',   JSON.parse(document.getElementById("o_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("o_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("o_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("o_crack").value)],
                ]
            }]
        });
    });
    var chart3;
    $(document).ready(function() {
        chart3 = new Highcharts.Chart({
            chart: {
                renderTo: 'chart_paidinfo_sem',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'SEM付费情况'
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
                    ['试用用户',   JSON.parse(document.getElementById("m_try").value)],
                    ['停用用户',    JSON.parse(document.getElementById("m_stop").value)],
                    {
                        name: '正常用户',
                        y: JSON.parse(document.getElementById("m_normal").value),
                        sliced: true,
                        selected: true
                    },
                    ['非法用户',    JSON.parse(document.getElementById("m_crack").value)],
                ]
            }]
        });
    });



});

