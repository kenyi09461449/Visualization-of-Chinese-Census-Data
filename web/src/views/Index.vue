<script setup>
import * as echarts from "echarts";
import china from "../map/china.json";
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import {onMounted, ref, watch} from "vue";
import {getChartData} from "@/api/chart"
import {userStar, userUnStar, userStarList} from "../api/user.js";
import {ElMessage} from "element-plus";

const router = useRouter();
const store = useStore();

const activeIndex = ref('')
const handleSelect = (key, keyPath) => {
    activeIndex.value = key
};

const starList = ref([]);

const handleLogout = () => {
    window.localStorage.clear()
    window.sessionStorage.clear()
    router.push('/login')
}

const handleHome = () => {
    router.push('/index')
}

const handleMyCollection = () => {
    router.push('/collection')
}

const nameMap = {
    '北京市': 'Beijing',
    '天津市': 'Tianjin',
    '河北省': 'Hebei',
    '山西省': 'Shānxī',
    '内蒙古自治区': 'Neimeng',
    '辽宁省': 'Liaoning',
    '吉林省': 'Jilin',
    '黑龙江省': 'Heilongjiang',
    '上海市': 'Shanghai',
    '江苏省': 'Jiangsu',
    '浙江省': 'Zhejiang',
    '安徽省': 'Anhui',
    '福建省': 'Fujian',
    '江西省': 'Jiangxi',
    '山东省': 'Shandong',
    '河南省': 'Henan',
    '湖北省': 'Hubei',
    '湖南省': 'Hunan',
    '广东省': 'Guangdong',
    '广西壮族自治区': 'Guangxi',
    '海南省': 'Hainan',
    '重庆市': 'Chongqing',
    '四川省': 'Sichuan',
    '贵州省': 'Guizhou',
    '云南省': 'Yunnan',
    '西藏自治区': 'Xizang',
    '陕西省': 'Shǎnxī',
    '甘肃省': 'Gansu',
    '青海省': 'Qinghai',
    '宁夏回族自治区': 'Ningxia',
    '新疆维吾尔自治区': 'Xinjiang',
    '台湾省': 'Taiwan',
    '香港特别行政区': 'HongKong',
    '澳门特别行政区': 'Macau',
    '南海诸岛': 'Nanhai',
}

// 2004-2023 year
const years = Array.from({length: 2023 - 2004 + 1}, (_, index) => 2004 + index);

const init = () => {
    // user if login
    if (!window.sessionStorage.getItem('user')) {
        router.push('/login')
        console.log("no login")
    }
}

const Chart1 = async () => {
    echarts.registerMap('china', china)
    const chartData = await getChartData('/chart1', {year: 2022});
    var chartDom = document.getElementById('chart1');
    var myChart = echarts.init(chartDom);
    var option = {
        title: {
            text: 'Population distribution by province and city in China in 2022',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}<br/>{c}/million people'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        visualMap: {
            type: 'continuous',
            left: 'right',
            top: 'bottom',
            min: 0,
            max: 110,
        },
        series: [
            {
                name: 'Province People',
                type: 'map',
                map: 'china',
                label: {
                    show: true
                },
                nameMap: nameMap,
                data: chartData.data.map(item => {
                    return {
                        name: nameMap[item.name],
                        value: item.value / 100
                    }
                })
            }
        ]
    }
    myChart.clear();
    option && myChart.setOption(option);

    window.addEventListener('resize', () => {
        myChart.resize();
    })
}

const Chart2 = async () => {
    var chartDom = document.getElementById('chart2');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart2', {});
    // console.log(chartData)
    option = {
        title: {
            text: '2004-2023 Demographic change (male to female ratio)',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/'
        },
        tooltip: {
            trigger: 'axis',
            formatter: '{b}<br/>{c}/million people',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        legend: {
            data: ['Total', 'Man', 'Woman'],
            align: 'right',
            right: '5%'
        },

        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: years
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: 'Man',
                type: 'line',
                stack: 'Total',
                label: {
                    show: true
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.man / 100)
            },
            {
                name: 'Woman',
                type: 'line',
                stack: 'Total',
                label: {
                    show: true
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.woman / 100)
            },
            {
                name: 'Total',
                type: 'line',
                stack: 'Total',
                label: {
                    show: true
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.total / 100)
            },
        ]
    };

    option && myChart.setOption(option);

    window.addEventListener('resize', () => {
        myChart.resize();
    })
}

const Chart3 = async () => {
    var chartDom = document.getElementById('chart3');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart2', {});

    option = {
        title: {
            text: '2004-2023 Population change (urban-rural ratio)',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/'
        },
        tooltip: {
            trigger: 'axis',
            formatter: '{b}<br/>{c}/million people',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        legend: {
            right: '5%'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: years
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: 'Total',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.total / 100)
            },
            {
                name: 'City',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.city / 100)
            },
            {
                name: 'Village',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: chartData.data.map(item => item.village / 100)
            }
        ]
    };

    option && myChart.setOption(option);
}

const Chart4 = async () => {
    var chartDom = document.getElementById('chart4');
    var myChart = echarts.init(chartDom);
    let option;

    const chartData = await getChartData('/chart4', {});

    option = {
        title: {
            text: 'Age distribution of population (2023)',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} million people ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Age',
                type: 'pie',
                radius: '50%',
                data: [
                    {value: chartData.data['age_0_14'] / 100, name: '0-15 years old'},
                    {value: chartData.data['age_15_64'] / 100, name: '15-64 years old'},
                    {value: chartData.data['age_65_up'] / 100, name: '65 and above years old'}
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    option && myChart.setOption(option);
}

const Chart5 = async () => {
    var chartDom = document.getElementById('chart5');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart5', {});

    const data = chartData.data;

    option = {
        title: {
            text: 'Population and GDP of each province (2022)',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: (row) => {
                console.log(row.data)
                let data = row.data;
                return `${nameMap[data[3]]}:<br/>Population：${data[1] / 100}(million)<br/>gdp：${(data[0] / 100).toFixed(2)}(million)`
            }
        },
        backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [
            {
                offset: 0,
                color: '#f7f8fa'
            },
            {
                offset: 1,
                color: '#cdd0d5'
            }
        ]),
        legend: {
            right: '10%',
            top: '3%',
            data: ['2022']
        },
        grid: {
            left: '8%',
            top: '10%'
        },
        xAxis: {
            label: "people",
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        },
        yAxis: {
            label: "gdp",
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            scale: true
        },
        series: [
            {
                name: '2022',
                data: data,
                type: 'scatter',
                symbolSize: function (data) {
                    return data[2] * 2;
                },
                emphasis: {
                    focus: 'series',
                    label: {
                        show: true,
                        formatter: function (param) {
                            return nameMap[param.data[3]];
                        },
                        position: 'top'
                    }
                },
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(120, 36, 50, 0.5)',
                    shadowOffsetY: 5,
                    color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
                        {
                            offset: 0,
                            color: 'rgb(251, 118, 123)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(204, 46, 72)'
                        }
                    ])
                }
            }
        ]
    };

    option && myChart.setOption(option);

}

const Chart6 = async () => {
    var chartDom = document.getElementById('chart6');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart6', {});

    const data = chartData.data;

    var series = [];
    for (var i = 0; i < data.length; i++) {

        series.push({
            type: 'radar',
            symbol: 'none',
            lineStyle: {
                width: 1
            },
            emphasis: {
                areaStyle: {
                    color: 'rgba(0,250,0,0.3)'
                }
            },
            data: [
                {
                    name: data[i].year + '',
                    value: data[i].value.split(",").map(item => item / 100),
                    province: data[i].name.split(",").map(item => nameMap[item]),
                }
            ]
        });
    }

    option = {
        title: {
            text: 'Top5 Population Urban Changes',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            top: 10,
            left: 10
        },
        tooltip: {
            trigger: 'item',
            formatter: (data) => {
                let str = ''
                data.data.province.forEach((item, index) => {
                    str += `${item}：${data.value[index]}/million people<br>`
                })
                return `${data.name}<br>${str}`
            }
        },
        legend: {
            type: 'scroll',
            bottom: 10,
            data: data.map(item => item.year + '')
        },
        visualMap: {
            top: 'middle',
            right: 10,
            color: ['red', 'yellow'],
            calculable: true
        },
        radar: {
            indicator: [
                {name: 'Sichuan', max: 130},
                {name: 'Shandong', max: 130},
                {name: 'Guangdong', max: 130},
                {name: 'Jiangsu', max: 130},
                {name: 'Henan', max: 130}
            ],
            splitNumber: 10
        },
        series: series
    };

    option && myChart.setOption(option);

}

const Chart7 = async () => {
    const chartDom = document.getElementById('chart7');
    const myChart = echarts.init(chartDom);

    const chartData = await getChartData('/chart7', {})

    const formatUtil = echarts.format;

    function getLevelOption() {
        return [
            {
                itemStyle: {
                    borderWidth: 0,
                    gapWidth: 5
                }
            },
            {
                itemStyle: {
                    gapWidth: 1
                }
            },
            {
                colorSaturation: [0.35, 0.5],
                itemStyle: {
                    gapWidth: 1,
                    borderColorSaturation: 0.6
                }
            }
        ];
    }

    const option = {
        title: {
            text: 'A rectangular tree of population distribution by province in 2022',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: function (info) {

            }
        },
        series: [
            {
                name: 'China',
                type: 'treemap',
                visibleMin: 300,
                label: {
                    show: true,
                    formatter: '{b}'
                },
                itemStyle: {
                    borderColor: '#fff'
                },
                levels: getLevelOption(),
                data: chartData.data.map(item => {
                    return {
                        name: nameMap[item.province],
                        value: item.total
                    }
                })
            }
        ]
    };

    option && myChart.setOption(option);

}

const Chart8 = async () => {
    var chartDom = document.getElementById('chart8');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart7', {});

    const data = chartData.data;

    var sunburstData = {
        name: 'China',
        children: []
    };

    data.forEach(item => {
        sunburstData.children.push({
            name: nameMap[item.province],
            value: item.total / 100
        });
    });

    option = {
        title: {
            text: 'Permanent population statistics by provinces and cities in 2022',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        tooltip: {
            trigger: 'item',
            formatter: (data) => {
                return `${data.data.name}：${data.data.value} million people`
            }
            // triggerOn: 'mousemove'
        },
        visualMap: {
            min: Math.min(...data.map(item => item.total / 100)),
            max: Math.max(...data.map(item => item.total / 100)),
            calculable: true,
            inRange: {
                color: ['#8bc654', 'rgba(236,28,28,0.73)']
            },
            orient: 'vertical',
            left: 'right',
            top: 'center'
        },
        series: {
            type: 'sunburst',
            data: [sunburstData],
            radius: [0, '90%'],
            label: {
                rotate: 'radial'
            },
            levels: [{}, {
                r0: '15%',
                r: '35%',
                label: {
                    rotate: 0
                }
            }, {
                r0: '45%',
                r: '65%',
                label: {
                    align: 'right'
                }
            }, {
                r0: '75%',
                r: '85%',
                label: {
                    position: 'outside',
                    padding: 3,
                    silent: false
                },
                itemStyle: {
                    borderWidth: 3
                }
            }]
        }
    };

    option && myChart.setOption(option);
}

const Chart9 = async () => {

    var chartDom = document.getElementById('chart9');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart4', {});

    option = {
        title: {
            text: 'Age distribution of population (2023)',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        gird: {
            top: '25%'
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} million people ({d}%)'
        },
        legend: {
            bottom: 20,
        },
        series: [
            {
                name: 'Age',
                type: 'funnel',
                left: '10%',
                top: 60,
                bottom: 60,
                width: '80%',
                min: 0,
                max: 100,
                minSize: '0%',
                maxSize: '100%',
                sort: 'descending',
                gap: 2,
                label: {
                    show: true,
                    position: 'inside'
                },
                labelLine: {
                    length: 10,
                    lineStyle: {
                        width: 1,
                        type: 'solid'
                    }
                },
                itemStyle: {
                    borderColor: '#fff',
                    borderWidth: 1
                },
                emphasis: {
                    label: {
                        fontSize: 20
                    }
                },
                data: [
                    {value: chartData.data['age_0_14'] / 100, name: '0-15 years old'},
                    {value: chartData.data['age_15_64'] / 100, name: '15-64 years old'},
                    {value: chartData.data['age_65_up'] / 100, name: '65 and above years old'}
                ]
            }
        ]
    };

    option && myChart.setOption(option);

}

const Chart10 = async () => {
    var chartDom = document.getElementById('chart10');
    var myChart = echarts.init(chartDom);
    var option;

    // let _rawData = [["Population", "GDP", "Life", "Country", "Year"], [815, 34.05, 351014, "Australia", 1800], [1314, 39, 645526, "Canada", 1800]]
    const chartData = await getChartData('/chart10', {});

    let _rawData = [
        ["Population", "GDP", "Life", "Province", "Year"]
    ]

    echarts.util.each(chartData.data, function (item) {
        _rawData.push([item.total / 100, 0, 0, nameMap[item.province], item.year]);
    })

    const provinces = Object.values(nameMap);

    const datasetWithFilters = [];
    const seriesList = [];

    echarts.util.each(provinces, function (province) {
        var datasetId = 'dataset_' + province;
        datasetWithFilters.push({
            id: datasetId,
            fromDatasetId: 'dataset_raw',
            transform: {
                type: 'filter',
                config: {
                    and: [
                        {dimension: 'Province', '=': province}
                    ]
                }
            }
        });
        seriesList.push({
            type: 'line',
            datasetId: datasetId,
            showSymbol: false,
            name: province,
            endLabel: {
                show: true,
                formatter: function (params) {
                    return params.value[3] + ': ' + params.value[0];
                }
            },
            labelLayout: {
                moveOverlap: 'shiftY'
            },
            emphasis: {
                focus: 'series'
            },
            encode: {
                x: 'Year',
                y: 'Income',
                label: ['Country', 'Income'],
                itemName: 'Year',
                tooltip: ['Income']
            }
        });
    });

    option = {
        animationDuration: 10000,
        dataset: [
            {
                id: 'dataset_raw',
                source: _rawData
            },
            ...datasetWithFilters
        ],
        title: {
            text: 'The population growth trend of each province in the past 20 years',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        // legend: {
        //     type: 'scroll',
        //     bottom: 10,
        //     data: provinces
        // },
        tooltip: {
            // order: 'valueDesc',
            trigger: 'item',
            formatter: function (params) {
                // console.log(params)
                let value = params.data;
                return value[3] + ': ' + value[0] + ' million people';
            }
        },
        xAxis: {
            type: 'category',
            nameLocation: 'middle'
        },
        yAxis: {
            name: 'Population (million people)'
        },
        grid: {
            right: 140
        },
        series: seriesList
    };

    option && myChart.setOption(option);
}

const Chart11 = async () => {
    var chartDom = document.getElementById('chart11');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart2', {});
    var row = chartData.data[0];
    var data = [row.total / 100, row.man / 100, row.woman / 100, row.city / 100, row.village / 100];

    option = {
        title: [
            {
                text: 'Changes of urban and rural population structure and gender ratio in recent 20 years',
                subtext: 'Data from https://data.stats.gov.cn/',
                sublink: 'https://data.stats.gov.cn/',
                left: 'center',
            },
            {
                text: "2004",
                textAlign: 'center',
                left: '80%',
                top: '60%',
                textStyle: {
                    fontSize: 100
                }
            }
        ],
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        legend: {
            bottom: 20,
            data: ['Population']
        },
        xAxis: {
            max: 'dataMax'
        },
        yAxis: {
            type: 'category',
            data: ['Total', 'Man', 'Woman', 'City', 'Village'],
            inverse: true,
            animationDuration: 300,
            animationDurationUpdate: 300,
            max: 2 // only the largest 2 bars will be displayed
        },
        series: [
            {
                realtimeSort: true,
                name: 'Population',
                type: 'bar',
                data: data,
                label: {
                    show: true,
                    position: 'right',
                    valueAnimation: true
                }
            }
        ],
        animationDuration: 0,
        animationDurationUpdate: 1500,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear'
    };

    myChart.setOption(option);

    function run(index) {
        var row = chartData.data[index];
        var data = [row.total / 100, row.man / 100, row.woman / 100, row.city / 100, row.village / 100];
        myChart.setOption({
            title: [
                {
                    text: 'Changes of urban and rural population structure and gender ratio in recent 20 years',
                    subtext: 'Data from https://data.stats.gov.cn/',
                    sublink: 'https://data.stats.gov.cn/',
                    left: 'center',
                },
                {
                    text: row.year,
                    textAlign: 'center',
                    left: '80%',
                    top: '60%',
                    textStyle: {
                        fontSize: 100
                    }
                }
            ],
            series: [
                {
                    type: 'bar',
                    data
                }
            ]
        });
    }

    var index = 1;
    var timer = setInterval(function () {
        run(index);
        index += 1;
        if (index > 18) {
            clearInterval(timer);
        }
    }, 3000);
}

const Chart12 = async () => {
    var chartDom = document.getElementById('chart12');
    var myChart = echarts.init(chartDom);
    var option;

    const chartData = await getChartData('/chart12', {});
    const data = chartData.data;

    option = {
        title: {
            text: 'Population growth rate in recent 10 years',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            bottom: 20
        },
        grid: {
            left: '3%',
            right: '4%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'value'
            }
        ],
        yAxis: [
            {
                type: 'category',
                axisTick: {
                    show: false
                },
                data: data.map(item => item.year)
            }
        ],
        series: [
            {
                name: 'Birth',
                type: 'bar',
                label: {
                    show: true,
                    position: 'inside'
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.map(item => item.birth)
            },
            {
                name: 'Death',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.map(item => item.death)
            },
            {
                name: 'Rise',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true,
                    position: 'left'
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.map(item => item.up)
            }
        ]
    };

    option && myChart.setOption(option);

}

const Chart13 = async () => {
    var chartDom = document.getElementById('chart13');
    var myChart = echarts.init(chartDom);
    var option;

    var itemStyle = {
        opacity: 0.8
    };

    // Schema:
    var schema = [
        {name: 'Population', index: 0, text: 'Population', unit: ' millions people'},
        {name: 'Gdp', index: 1, text: 'Gdp', unit: ' millions RMB'},
        {name: 'Province', index: 2, text: 'Province', unit: ''},
        {name: 'Year', index: 3, text: 'Year', unit: ''}
    ];

    const chartData = await getChartData('/chart13', {});
    let records = chartData.data;
    for (let i = 0; i < records.length; i++) {
        for (let c = 0; c < records[i].length; c++) {
            const city = records[i][c][2];
            if (nameMap.hasOwnProperty(city)) {
                records[i][c][2] = nameMap[city];
            }
        }
    }

    var data = {
        "provinces": Object.values(nameMap),
        "timeline": [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        "series": records
    };

    console.log(data);

    option = {
        baseOption: {
            timeline: {
                axisType: 'category',
                orient: 'vertical',
                autoPlay: true,
                inverse: true,
                playInterval: 1000,
                left: null,
                right: 0,
                top: 20,
                bottom: 20,
                width: 55,
                height: null,
                symbol: 'none',
                checkpointStyle: {
                    borderWidth: 2
                },
                controlStyle: {
                    showNextBtn: false,
                    showPrevBtn: false
                },
                data: []
            },
            title: [
                {
                    text: data.timeline[0],
                    textAlign: 'center',
                    left: '63%',
                    top: '55%',
                    textStyle: {
                        fontSize: 100
                    }
                },
                {
                    text: 'Evolution of the relationship between population and GDP in each province',
                    left: 'center',
                    top: 10,
                    textStyle: {
                        fontWeight: 'normal',
                        fontSize: 20
                    }
                }
            ],
            toolbox: {
                left: -30,
                top: 0,
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: "none"
                    },
                    dataView: {
                        readOnly: false
                    },
                    magicType: {
                        type: ["line", "bar"]
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            tooltip: {
                padding: 5,
                borderWidth: 1,
                formatter: function (obj) {
                    var value = obj.value;
                    console.log(value)
                    // prettier-ignore
                    return schema[3].text + '：' + value[3] + '<br>'
                        + schema[0].text + '：' + value[0].toFixed(2) + schema[0].unit + '<br>'
                        + schema[1].text + '：' + value[1].toFixed(2) + schema[1].unit + '<br>'
                        + schema[2].text + '：' + value[2] + '<br>';
                }
            },
            grid: {
                top: 100,
                containLabel: true,
                left: 30,
                right: '110'
            },
            xAxis: {
                type: 'log',
                name: 'Population',
                // max: 100000,
                // min: 300,
                nameGap: 25,
                nameLocation: 'middle',
                nameTextStyle: {
                    fontSize: 18
                },
                splitLine: {
                    show: false
                },
                axisLabel: {
                    formatter: '{value}'
                }
            },
            yAxis: {
                type: 'value',
                name: 'Gdp',
                // max: 100,
                nameTextStyle: {
                    fontSize: 18
                },
                splitLine: {
                    show: false
                },
                axisLabel: {
                    formatter: '{value}'
                }
            },

            series: [
                {
                    type: 'scatter',
                    itemStyle: itemStyle,
                    data: data.series[0]
                }
            ],
            animationDurationUpdate: 1000,
            animationEasingUpdate: 'quinticInOut'
        },
        options: []
    };

    for (var n = 0; n < data.timeline.length; n++) {
        option.baseOption.timeline.data.push(data.timeline[n]);
        option.options.push({
            title: {
                show: true,
                text: data.timeline[n] + ''
            },
            series: {
                name: data.timeline[n],
                type: 'scatter',
                itemStyle: itemStyle,
                data: data.series[n],
                symbolSize: function (val) {
                    return val[1] * 0.25;
                }
            }
        });
    }

    option && myChart.setOption(option);
}

const Chart14 = async () => {
    var chartDom = document.getElementById('chart14');
    var myChart = echarts.init(chartDom);
    var option;

    // let _rawData = [["Population", "GDP", "Life", "Country", "Year"], [815, 34.05, 351014, "Australia", 1800], [1314, 39, 645526, "Canada", 1800]]
    const chartData = await getChartData('/chart14', {});

    let _rawData = [
        ["Population", "Age", "Year"]
    ]

    echarts.util.each(chartData.data, function (item) {
        _rawData.push([item.total / 100, 'Total', item.year]);
        _rawData.push([item.age_0_14 / 100, 'Age_0_14', item.year]);
        _rawData.push([item.age_15_64 / 100, 'Age_15_64', item.year]);
        _rawData.push([item.age_65_up / 100, 'Age_65_up', item.year]);
    })

    const ages = ['Age_0_14', 'Age_15_64', 'Age_65_up', 'Total'];

    const datasetWithFilters = [];
    const seriesList = [];

    echarts.util.each(ages, function (age) {
        var datasetId = 'dataset_' + age;
        datasetWithFilters.push({
            id: datasetId,
            fromDatasetId: 'dataset_raw',
            transform: {
                type: 'filter',
                config: {
                    and: [
                        {dimension: 'Age', '=': age}
                    ]
                }
            }
        });
        seriesList.push({
            type: 'line',
            datasetId: datasetId,
            showSymbol: false,
            name: age,
            endLabel: {
                show: true,
                formatter: function (params) {
                    return params.value[1] + ': ' + params.value[0] + ' millions people';
                }
            },
            labelLayout: {
                moveOverlap: 'shiftY'
            },
            emphasis: {
                focus: 'series'
            },
            encode: {
                x: 'Year',
                y: 'Income',
                label: ['Country', 'Income'],
                itemName: 'Year',
                tooltip: ['Income']
            }
        });
    });

    option = {
        animationDuration: 10000,
        dataset: [
            {
                id: 'dataset_raw',
                source: _rawData
            },
            ...datasetWithFilters
        ],
        title: {
            text: 'Line chart of population growth by age group',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/',
            left: 'center',
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            }
        },
        // legend: {
        //     type: 'scroll',
        //     bottom: 10,
        //     data: provinces
        // },
        tooltip: {
            // order: 'valueDesc',
            trigger: 'item',
            formatter: function (params) {
                // console.log(params)
                let value = params.data;
                return value[1] + ': ' + value[0] + ' million people';
            }
        },
        xAxis: {
            type: 'category',
            nameLocation: 'middle'
        },
        yAxis: {
            name: 'Population (million people)'
        },
        grid: {
            right: 140
        },
        series: seriesList
    };

    option && myChart.setOption(option);
}

const Chart15 = async () => {
    var chartDom = document.getElementById('chart15');
    var myChart = echarts.init(chartDom);
    var option;

    echarts.registerMap('china', china)

    const chartData = await getChartData('/chart1', {year: 2022});

    const data = chartData.data.map(item => {
        return {
            name: nameMap[item.name],
            value: item.value / 100
        }
    });

    data.sort(function (a, b) {
        return a.value - b.value;
    });

    const mapOption = {
        title: {
            text: 'Population distribution by province and city in China in 2022',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/'
        },
        visualMap: {
            left: 'right',
            min: 0,
            max: 120,
            text: ['High', 'Low'],
            calculable: true
        },
        series: [
            {
                id: 'population',
                type: 'map',
                roam: true,
                map: 'china',
                animationDurationUpdate: 1000,
                universalTransition: true,
                nameMap: nameMap,
                data: data
            }
        ]
    };
    const barOption = {
        title: {
            text: 'Population distribution by province and city in China in 2022',
            subtext: 'Data from https://data.stats.gov.cn/',
            sublink: 'https://data.stats.gov.cn/'
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            axisLabel: {
                rotate: 30
            },
            data: data.map(function (item) {
                return item.name;
            })
        },
        animationDurationUpdate: 1000,
        series: {
            type: 'bar',
            id: 'population',
            data: data.map(function (item) {
                return item.value;
            }),
            universalTransition: true
        }
    };
    let currentOption = mapOption;
    myChart.setOption(mapOption);
    setInterval(function () {
        currentOption = currentOption === mapOption ? barOption : mapOption;
        myChart.setOption(currentOption, true);
    }, 3000);

    // option && myChart.setOption(option);
}

const getUserStarList = async () => {
    const res = await userStarList({"user_id": store.state.user.id});
    if (res.code === 200) {
        console.log(res.data.map(item => item.chart_name))
        starList.value = res.data.map(item => item.chart_name);
    }
}

onMounted(() => {
        init()
        getUserStarList()
        Chart1()
        // Chart2()
        // Chart3()
        // Chart4()
        // Chart5()
        // Chart6()
        // Chart7()
        // Chart8()
        // Chart9()
        // Chart10()
        // Chart11()
        // Chart12()
        // Chart13()
        // Chart14()
        // Chart15()
    },
)

// menus
const menus = ref([
    {
        name: 'chart1',
        title: 'Population distribution by province and city in China in 2022',
    },
    {
        name: 'chart2',
        title: '2004-2023 Demographic change (male to female ratio)',
    },
    {
        name: 'chart3',
        title: '2004-2023 Population change (urban-rural ratio)',
    },
    {
        name: 'chart4',
        title: 'Age distribution of population (2023)',
    },
    {
        name: 'chart5',
        title: 'Population and GDP of each province (2022)',
    },
    {
        name: 'chart6',
        title: 'Top5 Population Urban Changes',
    },
    {
        name: 'chart7',
        title: 'A rectangular tree of population distribution by province in 2022',
    },
    {
        name: 'chart8',
        title: 'Rising Sun Map of 2022 population analysis by province',
    },
    {
        name: 'chart9',
        title: 'Age distribution of population (2023)',
    },
    {
        name: 'chart10',
        title: 'The population growth trend of each province in the past 20 years',
    },
    {
        name: 'chart11',
        title: 'Changes of urban and rural population structure and gender ratio in recent 20 years',
    },
    {
        name: 'chart12',
        title: 'Population growth rate in recent 10 years',
    },
    {
        name: 'chart13',
        title: 'Evolution of the relationship between population and GDP in each province',
    },
    {
        name: 'chart14',
        title: 'Line chart of population growth by age group',
    },
    {
        name: 'chart15',
        title: 'Population distribution Map of China by province and city in 2022 & bar chart'
    }
]);

const cur_menu = ref('chart1');

const handleClickMenu = (name) => {
    cur_menu.value = name;
}

const handleClickStar = async (cur_tab) => {
    let state = starList.value.includes(cur_tab);
    if (state) {
        // remove star
        let res = await userUnStar({
            "user_id": store.state.user.id,
            "chart_name": cur_tab
        })
        if (res.code === 200) {
            ElMessage.success('Unstar success')
            await getUserStarList();
        } else {
            ElMessage.error(res.msg);
        }
    } else {
        // add star
        let res = await userStar({
            "user_id": store.state.user.id,
            "chart_name": cur_tab
        })
        if (res.code === 200) {
            ElMessage.success('Star success')
            await getUserStarList();
        } else {
            ElMessage.error(res.msg);
        }
    }
}

watch(cur_menu, (newValue, oldValue) => {
    console.log(newValue, oldValue);
    switch (newValue) {
        case 'chart1':
            setTimeout(() => {
                Chart1()
            }, 500)
            break;
        case 'chart2':
            setTimeout(() => {
                Chart2()
            }, 500)
            break;
        case 'chart3':
            setTimeout(() => {
                Chart3()
            }, 500)
            break;
        case 'chart4':
            setTimeout(() => {
                Chart4()
            }, 500)
            break;
        case 'chart5':
            setTimeout(() => {
                Chart5()
            }, 500)
            break;
        case 'chart6':
            setTimeout(() => {
                Chart6()
            }, 500)
            break;
        case 'chart7':
            setTimeout(() => {
                Chart7()
            }, 500)
            break;
        case 'chart8':
            setTimeout(() => {
                Chart8()
            }, 500)
            break;
        case 'chart9':
            setTimeout(() => {
                Chart9()
            }, 500)
            break;
        case 'chart10':
            setTimeout(() => {
                Chart10()
            }, 500)
            break;
        case 'chart11':
            setTimeout(() => {
                Chart11()
            }, 500)
            break;
        case 'chart12':
            setTimeout(() => {
                Chart12()
            }, 500)
            break;
        case 'chart13':
            setTimeout(() => {
                Chart13()
            }, 500)
            break;
        case 'chart14':
            setTimeout(() => {
                Chart14()
            }, 500)
            break;
        case 'chart15':
            setTimeout(() => {
                Chart15()
            }, 500)
            break;
    }
})
</script>

<template>
    <el-container>
        <el-header>
            <el-menu
                class="el-menu-demo"
                mode="horizontal"
                :ellipsis="false"

                @select="handleSelect"
            >
                <el-menu-item index="0" @click="handleHome">
                    <img
                        style="width: 200px;height: 50px;"
                        src="/logo.png"
                        alt="Logo"
                    />
                </el-menu-item>
                <div class="flex-grow"/>
                <el-sub-menu index="2">
                    <template #title>Welcome, {{ store.state.user.username }}</template>
                    <el-menu-item index="2-1" @click="handleMyCollection">My collection</el-menu-item>
                    <el-menu-item index="2-1" @click="handleLogout">Logout</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-header>

        <el-container>
            <el-aside width="400px">
                <el-menu
                    class="el-menu-vertical-demo"
                    default-active="chart1"
                >
                    <el-menu-item v-for="menu in menus" :index="menu.name" @click="handleClickMenu(menu.name)">
                        <el-tooltip class="box-item" effect="dark" :content="menu.title" placement="top-start">
                            <div>
                                <i class="el-icon-s-home"/>
                                <span>{{ menu.title }}</span>
                            </div>
                        </el-tooltip>
                    </el-menu-item>
                </el-menu>
            </el-aside>

            <el-main class="el-main-fix">
                <div class="chart-tab" v-if="'chart1' === cur_menu">
                    <div id="chart1" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart2' === cur_menu">
                    <div id="chart2" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart3' === cur_menu">
                    <div id="chart3" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart4' === cur_menu">
                    <div id="chart4" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart5' === cur_menu">
                    <div id="chart5" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart6' === cur_menu">
                    <div id="chart6" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart7' === cur_menu">
                    <div id="chart7" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart8' === cur_menu">
                    <div id="chart8" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart9' === cur_menu">
                    <div id="chart9" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart10' === cur_menu">
                    <div id="chart10" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart11' === cur_menu">
                    <div id="chart11" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart12' === cur_menu">
                    <div id="chart12" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart13' === cur_menu">
                    <div id="chart13" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart14' === cur_menu">
                    <div id="chart14" class="chart">

                    </div>
                </div>

                <div class="chart-tab" v-if="'chart15' === cur_menu">
                    <div id="chart15" class="chart">

                    </div>
                </div>

                <footer class="footer">
                    <el-icon size="32" color="red" @click="handleClickStar(cur_menu)">
                        <StarFilled v-if="starList.includes(cur_menu)"/>
                        <Star v-else/>
                    </el-icon>

                    <div class="footer-desc" v-if="starList.includes(cur_menu)">
                        Unfavorite
                    </div>
                    <div v-else>
                        Favorite
                    </div>
                </footer>
            </el-main>

        </el-container>
    </el-container>
</template>

<style scoped>
.flex-grow {
    flex-grow: 1;
}

.el-main {
    margin: 20px;
    width: 60% !important;
    padding: unset !important;
}

.el-header {
    padding: 0;
}

.chart-tab {
    background-color: white;
    width: 100%;
    margin: 30px auto;
    padding: 50px;
}

.chart {
    width: 100%;
    height: 60vh;
}

.footer {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.footer-desc {

}

.custom-menu-item {
    word-break: break-all;
    word-wrap: break-word;
    white-space: normal;
}

.el-menu-item {
    max-width: 400px;
    height: 80px;
    line-height: unset;
}

.el-menu-item * {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>