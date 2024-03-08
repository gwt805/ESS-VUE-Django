<template>
    <div id="layout">
        <div class="tools-div">
            <div class="m-4">
                <el-select v-model="searchData.uname" filterable clearable placeholder="用户名" style="width: 150px" @change="draw_echarts">
                    <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.kind" filterable placeholder="任务类型" style="width: 100px" @change="draw_echarts">
                    <el-option v-for="item in ['审核', '标注']" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.supplier" filterable clearable placeholder="标注方" style="width: 100px" @change="draw_echarts">
                    <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="block">
                <el-date-picker v-model="datarear" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" @change="draw_echarts" />
            </div>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
        </div>
        <div id="charts">
            <div id="bar_chart_check" ref="bar_chart_check" v-if="searchData.kind=='审核'"></div>
            <div id="bar_chart_anno" ref="bar_chart_anno" v-if="searchData.kind=='标注'"></div>
            <div :ref="'验收' + itemc" :id="'验收' + itemc" v-for="itemc in check_data_pname_list_div" v-if="searchData.kind=='审核'"></div>
            <div :ref="'标注' + itema" :id="'标注' + itema" v-for="itema in anno_data_pname_list_div" v-if="searchData.kind=='标注'"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import * as echarts from "echarts";
import { Refresh } from '@element-plus/icons-vue';
import { user_list, supplier_list } from "@/api/public";
import { get_anno_team_task_count } from "@/api/annoteam";
import { public_elmsg_warning } from "@/utils/elmsg";

const UserList = ref([]);
const SupplierList = ref([]);

const check_data_pname_list_div = ref([]);
const anno_data_pname_list_div = ref([]);

const now_date = new Date();
const now_month = now_date.getMonth() + 1 < 10 ? "0" + (now_date.getMonth() + 1) : now_date.getMonth() + 1;
const now_day = now_date.getDate() < 10 ? "0" + now_date.getDate() : now_date.getDate();
const begin_date = now_date.getFullYear() + "-" + now_month +"-01";
const last_date = now_date.getFullYear() + "-" + now_month + "-" + now_day;

const datarear = ref([begin_date, last_date]);
const searchData = ref({ "uname": "", "kind": "审核", "supplier": "" });
const size = ref<'default' | 'large' | 'small'>('default');

user_list().then((res) => {
    UserList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
});

supplier_list().then((res) => {
    SupplierList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

const reportEcharts = (init_dom:any, check_data_pname_list: any, kind: string, line_chart_check_or_anno_list:any) => {
    // check bar chart
    const echarts_dom_list: any = [init_dom];
    if (kind === "审核"){
        // 验收折线图 start
        for (let line = 0; line < check_data_pname_list.length; line++) {
            var dom = document.getElementById("验收" + check_data_pname_list[line]);
            var chart_lines = echarts.init(dom, 'dark')
            echarts_dom_list.push(chart_lines);
            var option = {
                title: {
                    text: check_data_pname_list[line] + ' 验收样本数量走势图'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['样本数']
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
                    data: line_chart_check_or_anno_list[line][0]
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '样本数',
                        type: 'line',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: line_chart_check_or_anno_list[line][1],
                        // lineStyle: {color: 'yellow'} // 可以设置折线的颜色
                    }
                ]
            };
            chart_lines.setOption(option);
        }
        // 验收折线图 end
    }
    else {
        // 标注折线图 start
        for (let line = 0; line < check_data_pname_list.length; line++) {
            var dom = document.getElementById("标注" + check_data_pname_list[line]);
            var chart_lines = echarts.init(dom, 'dark')
            echarts_dom_list.push(chart_lines);
            var option = {
                title: {
                    text: check_data_pname_list[line] + ' 样本量&标注量走势图'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['样本数', '标注量']
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
                    data: line_chart_check_or_anno_list[line][0]
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '样本数',
                        type: 'line',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: line_chart_check_or_anno_list[line][1],
                        // lineStyle: {color: 'yellow'} // 可以设置折线的颜色
                    },
                    {
                        name: '标注量',
                        type: 'line',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: line_chart_check_or_anno_list[line][2],
                        // lineStyle: {color: 'yellow'} // 可以设置折线的颜色
                    }
                ]
            };
            chart_lines.setOption(option);
        }
        // 标注折线图 end
    }

    // echart resizes
    window.onresize = () => {
        for (let i = 0; i < echarts_dom_list.length; i++) {
            echarts_dom_list[i].resize();
        }
    }
}

const draw_echarts = () => {
    const begin_time = datarear.value[0];
    const last_time = datarear.value[1];
    get_anno_team_task_count(searchData.value.uname, searchData.value.kind, searchData.value.supplier, begin_time, last_time).then((res: any) => {
        if (res.code == -1) {public_elmsg_warning(res.msg);}
        if (res.kind == "审核") {
            check_data_pname_list_div.value = res.pname_list;
            const check_bar = echarts.init(document.getElementById("bar_chart_check"), 'dark');
            const check_bar_option = {
                title: {
                    text: datarear.value[0] + ' ~ ' + datarear.value[1] + ' 各项目验收情况'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['验收样本数量']
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
                    data: res.bar_chart_check_or_anno_list[0]
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '验收样本数量',
                        type: 'bar',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: res.bar_chart_check_or_anno_list[1],
                    }
                ]
            };
            check_bar.setOption(check_bar_option);
            setTimeout(() => {
                reportEcharts(check_bar,res.pname_list, res.kind, res.line_chart_check_or_anno_list)
            }, 1)
        }
        else {
            anno_data_pname_list_div.value = res.pname_list;
            // anno bar chart 
            const anno_bar = echarts.init(document.getElementById("bar_chart_anno"), 'dark');
            const anno_bar_option = {
                title: {
                    text: datarear.value[0] + ' ~ ' + datarear.value[1] + ' 各项目标注情况'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['样本量', '标注量']
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
                    data: res.bar_chart_check_or_anno_list[0]
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '样本量',
                        type: 'bar',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: res.bar_chart_check_or_anno_list[1],
                    },
                    {
                        name: '标注量',
                        type: 'bar',
                        smooth: true,
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    name: '最大值',
                                },
                            ]
                        },
                        data: res.bar_chart_check_or_anno_list[2],
                    }
                ]
            };
            anno_bar.setOption(anno_bar_option);
            // 柱状图 end
            setTimeout(() => {
                reportEcharts(anno_bar,res.pname_list, res.kind, res.line_chart_check_or_anno_list)
            }, 1)
        }
    }).catch((err: any) => {
        console.log(err);
    })
};
draw_echarts();

const reset = () => {
    datarear.value = [begin_date, last_date];
    searchData.value = { "uname": "", "kind": "审核", "supplier": "" };
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

#bar_chart_check,
#bar_chart_anno {
    width: 100%;
    height: 500px;
}
</style>