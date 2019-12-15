//echarts4.0 文档地址
//https://www.echartsjs.com/zh/option.html#series-graph.lineStyle.color
if (!window.console) {
    //兼容
    window.console = {
        error: function () {

        },
        log: function () {

        },
        table: function () {

        }
    }
}
window.ec = echarts;
initApp();
var keyCahce = {};

function getData(key) {
    return new Promise(function (resolve, reject) {
        axios.get('https://api.ownthink.com/kg/knowledge?entity=' + key).then(res => {

            if (res.data.message != 'success' || res.data.data.hasOwnProperty("avp") == false) {
                reject(res.data);
                app.noData = true;
            } else {
                app.noData = false;
                //移除关键词本身
                let temps = [];
                res.data.data.avp.forEach(item => {
                    let label = item[1];
                    if (label != key && !keyCahce[label]) {
                        temps.push(item);
                        // keyCahce[label] = "";
                    }
                });
                res.data.data.avp = temps;
                resolve(res.data.data);

            }

        }).catch(err => {
            console.error(err);
            alert('接口挂了，请联系管理员！');
        })
    });
}

function initApp() {
    //初始化vue
    window.app = new Vue({
        el: '#app',
        data: {
            input: '',
            noData: false
        },
        created: function () {

            var word = getQueryVariable('word')
            if (word) {
                word = decodeURI(word);
                this.search(word)
            } else {
                word = '';
            }

            this.input = word;

            this.$nextTick(function () {
                this.search(this.input);
            });

        },
        methods: {
            enter: function () {
                // this.search();
                if (this.input != '') {
                    window.location.href = '/knowledge.html?word=' + this.input;
                }
            },
            search: function () {
                if (this.input == "") {
                    return;
                }
                global_index = 1;
                keyCahce = {};
                getData(this.input).then(res => {

                    handlerData(res).then(data => {
                        data.nodes.unshift({
                            id: 0,
                            category: 0,
                            name: res.entity,
                            symbolSize: 10,
                            itemStyle: {
                                color: 'blue'
                            }
                        });
                        initEc(data);
                    })

                });

            }
        }
    })
}

function initEc(data) {

    var myChart = ec.init(document.getElementById('main'), 'macarons');
    window.myChart = myChart;
    var option = {
        tooltip: {
            show: false
        },
        series: [{
            itemStyle: {
                normal: {
                    label: {
                        position: 'top',
                        show: true,
                        textStyle: {
                            color: '#FFF'
                        }
                    },
                    nodeStyle: {
                        brushType: 'both',
                        borderColor: 'rgba(255,215,0,0.4)',
                        borderWidth: 1
                    },
                    linkStyle: {
                        color: 'source',
                        curveness: 0,
                        type: "solid"
                    }
                },

            },
            force: {
                initLayout: 'force',//初始布局
                edgeLength: 5,
                repulsion: 20,
                gravity: 0.2,
                layoutAnimation: false
            },
            edgeLabel: {
                show: true,
                formatter: function (param) {
                    return param.data.lineLabel
                }
            },
            //形状
            // symbol:'arrow',
            name: 'Les Miserables',
            type: 'graph',
            layout: 'force',//取值none,circular,force
            roam: true,//可以拖动
            draggable: true,
            useWorker: true,
            minRadius: 15,
            maxRadius: 25,
            // gravity: 0.1,
            // scaling: 3.1,
            zoom: 5,
            nodes: data.nodes,
            links: data.links
        }]
    };
    myChart.setOption(option);

    function openOrFold(param) {

        var option = myChart.getOption();
        var nodes = option.series[0].nodes;
        var links = option.series[0].links;

        var data = param.data;
        //如果节点点击过了，就不能再次点击了
        if (!data.flag) {
            for (var i = 0; i < nodes.length; i++) {
                if (data.id == nodes[i].id) {
                    option.series[0].nodes[i].flag = true;
                }
            }
        } else {
            console.log('节点被加载过了。')
            return;
        }

        // myChart.setOption(option);

        //从网络取下一个节点，然后追加到nodes中
        getData(data.name).then(res => {
            //追加节点到nodes
            handlerData(res, data.id).then(dd => {

                //遍历，如果nodes存在了，就不追加
                nodes = nodes.concat(dd.nodes);
                links = links.concat(dd.links);
                option.series[0].nodes = nodes;
                option.series[0].links = links;

                // console.log(option.series[0].nodes)
                myChart.clear();
                myChart.setOption(option);
            });
        });

    }

    myChart.on('click', openOrFold);
    myChart.on('dblclick', openOrFold);
}

var global_index = 1;

function handlerData(res, targetId) {
    if (!targetId) {
        targetId = 0;
    }

    return new Promise(resolve => {
        let links = [];
        let nodes = [];

        res.avp.forEach((item, index) => {
            let id = global_index++;
            nodes.push({
                id: id,
                name: item[1],
                value: item[1],
                symbolSize: 5,
                itemStyle: {
                    color: randomRgbColor()
                }
            });
            links.push({
                source: id,
                target: targetId,
                lineLabel: item[0]
            });
        });
        resolve({
            nodes: nodes,
            links: links
        });
    });
}

function randomRgbColor() { //随机生成RGB颜色
    var r = Math.floor(Math.random() * 256); //随机生成256以内r值
    var g = Math.floor(Math.random() * 256); //随机生成256以内g值
    var b = Math.floor(Math.random() * 256); //随机生成256以内b值
    return `rgb(${r},${g},${b})`; //返回rgb(r,g,b)格式颜色
}

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return (false);
}
