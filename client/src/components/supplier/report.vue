<template>
    <div id="layout">
        <div class="tools-div">
            <div class="m-4">
                <strong>&nbsp;&nbsp;是否按照数据发送日期查询&nbsp;&nbsp;</strong>
                <el-select v-model="searchData.select_time_method" filterable style="width: 100px" @change="draw_echarts">
                    <el-option v-for="item in is_send_time" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.supplier_name" filterable clearable placeholder="标注方" style="width: 100px" @change="draw_echarts">
                    <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="block">
                <el-date-picker v-model="datarear" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" @change="draw_echarts" />
            </div>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
        </div>
        <div id="charts">
            <div id="chart_pnums"></div>
            <div id="chart_knums" style="width: 49.9%; height: 50%; float: left;"></div>
            <div id="char_money" style="width: 100%; height: 50%; float: left; border-top: 1px dashed gray;"></div>
            <div :id="item" v-for="item in proname_div"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import * as echarts from "echarts";
import { supplier_list } from "@/api/public";
import { Refresh } from '@element-plus/icons-vue';
import { get_supplier_task_count } from "@/api/supplier";
import { public_elmsg_warning } from "@/utils/elmsg/index";

document.title = "供应商各项目数据统计";

const SupplierList = ref([]);

const now_date = new Date();
const now_month = now_date.getMonth() + 1 < 10 ? "0" + (now_date.getMonth() + 1) : now_date.getMonth() + 1;
const now_day = now_date.getDate() < 10 ? "0" + now_date.getDate() : now_date.getDate();
const now_now_date = now_date.getFullYear() + "-" + now_month + "-" + now_day;
const datarear = ref([now_date.getFullYear() + "-" + now_month +"-01", now_now_date]);

const is_send_time = ["是", "否"];
const searchData = ref({ "select_time_method": "是", "supplier_name": "", "start_time": "", "last_time": "" });

const proname_div = ref([]);
let pie_text = "";

const size = ref<'default' | 'large' | 'small'>('default');

supplier_list().then((res) => {
    SupplierList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

const reportEcharts = (pname: any, chart_pie: any, chart_line: any, money_total: any) => {
    // 饼图 start
    const chart_list = [echarts.init(document.getElementById("chart_pnums"), 'dark'), echarts.init(document.getElementById("chart_knums"), 'dark'), echarts.init(document.getElementById("char_money"), 'dark')]
    const chart_pie_info = ["总样本数", '总标注数', "已用金额"];
    let echarts_doms = chart_list;
    for (let pie = 0; pie < chart_pie.length; pie++) {
        if (pie == 2) {
            pie_text = datarear.value[0] + ' ~ ' + datarear.value[1] + ' 各项目' + chart_pie_info[pie] + '情况(总金额: ' + money_total + ' 元)';
        }
        else {
            pie_text = datarear.value[0] + ' ~ ' + datarear.value[1] + ' 各项目' + chart_pie_info[pie] + '情况';
        }
        const option = {
            title: {
                text: pie_text, // 一级标题
                // subtext: 'Fake Data', // 二级标题
                left: 'center' // 标题居中显示
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            toolbox: {
                show: true,
                feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false, lang: ['数据视图', '关闭', '刷新'] },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            series: [
                {
                    name: '项目名字 - 框数/金额 - 占比',
                    type: 'pie',
                    radius: '50%',
                    label: {
                        normal: {
                            show: true,
                            formatter: '{b}: {c}({d}%)'
                        },
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 15
                        }, labelLine: { show: true }
                    },
                    data: chart_pie[pie],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }
        chart_list[pie].setOption(option);
    }
    // 饼图end

    // 折线图 start
    for (let line = 0; line < chart_line.length; line++) {
        var chart_lines = echarts.init(document.getElementById(pname[line]), 'dark');
        echarts_doms.push(chart_lines);
        var option = {
            title: {
                text: pname[line] + ' 框数,金额 走势图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['标注数', '金额', '样本数']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '12%',
                containLabel: true
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100,
                    xAxisIndex: [0, 1]
                }
            ],
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    dataView: { readOnly: false, lang: ['数据视图', '关闭', '刷新'] },
                    magicType: { type: ['line', 'bar'] },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: chart_line[line][0]
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '标注数',
                    type: 'line',
                    smooth: true,
                    markPoint: {
                        data: [
                            {
                                type: 'max',
                                name: '最大值',
                            },
                            // {
                            //     type: 'min',
                            //     name: '最小值',
                            // }
                        ]
                    },
                    data: chart_line[line][1],
                    // lineStyle: {color: 'yellow'} // 可以设置折线的颜色
                },
                {
                    name: '金额',
                    type: 'line',
                    smooth: true,
                    markPoint: {
                        data: [
                            {
                                type: 'max',
                                name: '最大值',
                            },
                            // {
                            //     type: 'min',
                            //     name: '最小值',
                            // }
                        ]
                    },
                    data: chart_line[line][2]
                },
                {
                    name: '样本数',
                    type: 'line',
                    stack: 'Total',
                    smooth: true,
                    markPoint: {
                        data: [
                            {
                                type: 'max',
                                name: '最大值',
                            },
                            // {
                            //     type: 'min',
                            //     name: '最小值',
                            // }
                        ]
                    },
                    data: chart_line[line][3],
                    // lineStyle: {color: 'yellow'} // 可以设置折线的颜色
                }
            ]
        };
        chart_lines.setOption(option);
    }
    // 折线图 end

    window.onresize = function () {
        for (let pie = 0; pie < echarts_doms.length; pie++) {
            chart_list[pie].resize();
        }
    }
}

const draw_echarts = () => {
    searchData.value.start_time = datarear.value[0];
    searchData.value.last_time = datarear.value[1];
    get_supplier_task_count(searchData.value.select_time_method, searchData.value.supplier_name, searchData.value.start_time, searchData.value.last_time).then((res: any) => {
        if (res.code == -1) {public_elmsg_warning(res.msg);}
        proname_div.value = res.proname;
        const chart_pie = res.chart_pie;
        const chart_line = res.chart_line;
        const money_total = res.money_total;

        setTimeout(() => {
            reportEcharts(res.proname, chart_pie, chart_line, money_total)
        }, 1)

    }).catch((err) => { console.log(err) })
}

draw_echarts()

const reset = () => {
    datarear.value = [now_date.getFullYear() + "-01-01", now_now_date];
    searchData.value = { "select_time_method": "是", "supplier_name": "", "start_time": "", "last_time": "" };
    draw_echarts();
};
</script>

<style scoped>
.tools-div {
    display: flex;
    justify-content: center;
}

#charts {
    width: 100%;
    min-width: 1200px;
    height: 95%;
    position: absolute;
    overflow-y: auto;
    overflow-x: hidden;
    /* border: 1px dashed yellow; */
}

#charts div {
    width: 100%;
    height: 500px;
    float: left;
    border-bottom: 1px dashed white;
}

#charts div:last-child {
    border-bottom: none;
}

#charts #chart_pnums {
    width: calc(100%/2);
    height: 50%;
    float: left;
    border-right: 1px dashed gray;
}
#charts #chart_knums {
    width: calc(100%/2);
    height: 50%;
    float: left;
}
</style>