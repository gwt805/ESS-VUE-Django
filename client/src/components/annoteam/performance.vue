<template>
    <div id="layout">
        <!-- search -->
        <div class="tools-div">
            <div class="m-4">
                <el-select v-model="searchData.uname" filterable clearable placeholder="请选择用户名" style="width: 200px">
                    <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="block">
                <el-date-picker v-model="datarear" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" />
            </div>
            <el-button class="search-btn" type="primary" :icon="Search" @click="search">搜索</el-button>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
            <el-button type="primary" :icon="Share" @click="export_table_data">导出</el-button>
        </div>

        <!-- show -->
        <el-table :data="tableData" style="width: 100%" height="835">
            <el-table-column type="index" :index="indexMethod" />
            <el-table-column prop="tspname" label="项目名字" sortable />
            <el-table-column prop="tskind" label="任务类型" sortable />
            <el-table-column prop="tspnum" label="图片/点云/视频数量" />
            <el-table-column prop="tsknum" label="框数/属性/时长" />
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import * as XLSX from "xlsx";
import { user_list } from "@/api/public";
import { get_anno_team_person_performance } from "@/api/annoteam";
import { Search, Share, Refresh } from '@element-plus/icons-vue';
import { public_elmsg_warning, public_elmsg_success } from "@/utils/elmsg/index";

document.title = "个人绩效";

const UserList = ref([]);
const tableData = ref([]);
const searchData = ref({ "uname": "" });
const datarear = ref("");
const indexMethod = (index: number) => { return index + 1 };
const size = ref<'default' | 'large' | 'small'>('default');

user_list().then((res) => {
    UserList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
});

// export table data
const export_table_data = () => {
    const data = XLSX.utils.json_to_sheet(tableData.value)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, data, 'selfjs')
    XLSX.writeFile(wb, 'selfjs.xlsx')
}

// search
const search = () => {
    if (searchData.value.uname == "") { public_elmsg_warning("请选择用户名 !"); }
    else if ( datarear.value == "" || datarear.value == null) { public_elmsg_warning("请选择时间 !"); }
    else {
        const begin_date = datarear.value[0];
        const last_time = datarear.value[1];
        get_anno_team_person_performance(begin_date, last_time, searchData.value.uname).then((res: any) => {
            if (res.code == 0) {
                public_elmsg_success(res.msg);
                tableData.value = res.data;
            }
            else { public_elmsg_warning(res.msg); }
        }).catch((err: any) => {
            console.log(err);
        })
    }
}

// reset
const reset = () => {
    searchData.value = { "uname": "" };
    datarear.value = "";
    tableData.value = [];
}

</script>

<style scoped>
.tools-div {
    display: flex;
}

.search-btn {
    margin-left: 15px;
}
</style>