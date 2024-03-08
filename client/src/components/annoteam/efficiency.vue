<template>
    <div id="layout">
        <!-- search -->
        <div class="tools-div">
            <div class="block">
                <el-date-picker v-model="begin_datarear" type="daterange" range-separator="-" start-placeholder="本周开始日期" end-placeholder="本周结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" />
            </div>
            <div class="block">
                <el-date-picker v-model="last_datarear" type="daterange" range-separator="-" start-placeholder="上周开始日期" end-placeholder="上周结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" />
            </div>
            <el-button class="search-btn" type="primary" :icon="Search" @click="search">搜索</el-button>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
        </div>
        <div class="effciency-data">
            <el-table :data="team_eff" key="id" border style="width: 100%">
                <el-table-column label="团队效率" align="center">
                    <el-table-column prop="kinds" label="任务类型" sortable />
                    <el-table-column prop="pname" label="项目名字" sortable />
                    <el-table-column prop="pnums" label="样本数量" />
                    <el-table-column prop="knums" label="标注数量" />
                    <el-table-column prop="neff" label="本周效率(帧|标注|时长/h)" />
                    <el-table-column prop="leff" label="上周效率(帧|标注|时长/h)" />
                </el-table-column>
            </el-table>
            <!-- <h3>个人效率</h3> -->
            <el-table :data="item" v-for="item in person_eff" border style="width: 100%">
                <el-table-column label="个人效率" align="center">
                    <el-table-column prop="name" label="用户名" />
                    <el-table-column prop="kinds" label="任务类型" sortable />
                    <el-table-column prop="pname" label="项目名字" sortable />
                    <el-table-column prop="pnums" label="样本数量" />
                    <el-table-column prop="knums" label="标注数量" />
                    <el-table-column prop="neff" label="本周效率(帧|标注|时长/h)" />
                    <el-table-column prop="leff" label="上周效率(帧|标注|时长/h)" />
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Search, Refresh } from "@element-plus/icons-vue";
import { get_anno_team_efficiency } from "@/api/annoteam";
import { public_elmsg_warning, public_elmsg_success } from "@/utils/elmsg/index";

const begin_datarear = ref("")
const last_datarear = ref("")
const team_eff = ref([]);
const user_list = ref([]);
const person_eff = ref([]);

const size = ref<'default' | 'large' | 'small'>('default');

const search = () => {
    if (begin_datarear.value == null || begin_datarear.value == "") { public_elmsg_warning("请选择开始日期 !"); }
    else {
        get_anno_team_efficiency(begin_datarear.value[0], begin_datarear.value[1], last_datarear.value[0], last_datarear.value[1]).then((res: any) => {
            if (res.code == 0) {
                public_elmsg_success(res.data);
                team_eff.value = res.eff_team;
                user_list.value = res.user_list;
                person_eff.value = res.eff_person;
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err: any) => { console.log(err) })
    }
};

const reset = () => {
    begin_datarear.value = "";
    last_datarear.value = "";
    team_eff.value = [];
    user_list.value = [];
    person_eff.value = [];
}

</script>

<style scoped>
.tools-div {
    display: flex;
}

.search-btn {
    margin-left: 15px;
}

.effciency-data {
    width: 100%;
    height: 96%;
    position: absolute;
    overflow: auto;
}
</style>