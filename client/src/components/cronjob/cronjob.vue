<template>
    <div id="layout">
        <el-dialog v-model="addmodel" title="添加数据" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 400px;">
            <el-form label-position="top" :model="addData" require-asterisk-position="left">
                <el-text class="mx-1" type="warning addmodelp">都不填 默认为每周一 零点</el-text>
                <el-form-item label="每周的第几天执行( 0 ~ 6 即 周一 ~ 周日)" required>
                    <el-input v-model="addData.weekday" type="number" min="0" max="6" />
                </el-form-item>
                <el-form-item label="开始执行时间(小时: 0 ~ 23)" required>
                    <el-input v-model="addData.hour" type="number" min="0" max="23" />
                </el-form-item>
                <el-form-item label="开始执行时间(分钟: 0 ~ 59)" required>
                    <el-input v-model="addData.minute" type="number" min="0" max="59" />
                </el-form-item>
                <el-form-item label="开始执行时间(秒: 0 ~ 59)" required>
                    <el-input v-model="addData.second" type="number" min="0" max="59" />
                </el-form-item>
                <el-button type="primary" class="addmodelbtn" @click="addmodelck">添加</el-button>
            </el-form>
        </el-dialog>
        <el-table :data="cronData" border highlight-current-row style="width: 100%" height="250" table-layout="fixed">
            <el-table-column prop="id" label="ID" />
            <el-table-column prop="time" label="下次执行时间" />
            <el-table-column width="180px" fixed="right" align="center">
                <template #header>
                    <el-button type="primary" class="addmodelbtn" @click="addmodeldk" v-if="!rootdisable">添加</el-button>
                </template>
                <template #default="scope">
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" v-if="!rootdisable">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-table :data="cronLogData" border highlight-current-row style="width: 100%" height="550" table-layout="fixed">
            <el-table-column prop="id" label="ID" />
            <el-table-column prop="job_id" label="job_id" />
            <el-table-column prop="status" label="status" />
            <el-table-column prop="run_time" label="run_time" />
            <el-table-column prop="duration" label="duration" />
            <el-table-column prop="finished" label="finished" />
            <el-table-column prop="exception" label="exception" />
            <el-table-column prop="traceback" label="traceback" />
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessageBox } from "element-plus";
import { add_cronjob, get_cronjob, get_cronjob_log, del_cronjob } from "@/api/cronjob";
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";

const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);

const cronData = ref([]);
const cronLogData = ref([]);

const addmodel = ref(false);
const addData = ref({ "weekday": 0, "hour": 0, "minute": 0, "second": 0 })

const get_all_data = () => {
    get_cronjob().then((res: any) => {
        cronData.value = res.data;
    }).catch((err) => { console.log(err) });
    get_cronjob_log().then((res: any) => {
        cronLogData.value = res.data;
    }).catch((err) => { console.log(err) });
};
get_all_data();

const addmodeldk = () => { addmodel.value = true; };
const addmodelck = () => {
    if (addData.value.weekday < 0 || addData.value.weekday > 6) { public_elmsg_warning("每周的第几天执行 参数填写错误 !"); }
    else if (addData.value.hour < 0 || addData.value.hour > 23) { public_elmsg_warning("开始执行时间(小时) 参数填写错误 !"); }
    else if (addData.value.minute < 0 || addData.value.minute > 59) { public_elmsg_warning("开始执行时间(分钟) 参数填写错误 !"); }
    else if (addData.value.second < 0 || addData.value.second > 59) { public_elmsg_warning("开始执行时间(秒) 参数填写错误 !"); }
    else {
        add_cronjob(addData.value.weekday, addData.value.hour, addData.value.minute, addData.value.second).then((res: any) => {
            if (res.code == 0) {
                addmodel.value = false;
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err) => { console.log(err); });
    }
};
// delete
const handleDelete = (index: any, row: any) => {
    console.log(index)
    ElMessageBox.confirm(
        `你确定要删除 ID 为 ${row.id} 的数据吗?`,
        'DELETE',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(() => {
            del_cronjob(row.id).then((res: any) => {
                if (res.code == 0) {
                    public_elmsg_success(res.data);
                    get_all_data();
                }
                else { public_elmsg_warning(res.data); }
            }).catch((err) => { console.log(err) });

        })
        .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消删除`); })
}

</script>

<style scoped>
.addmodelp {
    display: block;
    text-align: center;
    margin-top: -20px;
}

.addmodelbtn {
    width: 100%;
}
</style>