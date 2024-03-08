<template>
    <div id="layout">
        <!-- search -->
        <div class="tools-div">
            <div class="m-4">
                <el-input v-model="searchData.task_id" type="number" min="0" placeholder="任务ID" clearable @change="get_all_data" />
            </div>
            <div class="m-4">
                <el-select v-model="searchData.uname" filterable clearable placeholder="请选择用户名" @change="get_all_data" style="width: 150px">
                    <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.pname" filterable clearable placeholder="请选择项目名字" @change="get_all_data" style="width: 200px">
                    <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.supplier" filterable clearable placeholder="请选择标注方" @change="get_all_data" style="width: 150px">
                    <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="m-4">
                <el-select v-model="searchData.task_kind" filterable clearable placeholder="请选择任务类型" @change="get_all_data" style="width: 150px">
                    <el-option v-for="item in AnnoTaskKindList" :key="item" :label="item" :value="item" />
                </el-select>
            </div>
            <div class="block">
                <el-date-picker v-model="datarear" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" @change="get_all_data" style="width: 250px;" />
            </div>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
            <el-button type="primary" :icon="Share" @click="export_table_data">导出</el-button>
        </div>
        <!-- add data dialog -->
        <el-dialog v-model="addmodel" title="添加数据" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 500px;">
            <el-form label-position="left" label-width="110px" :model="addData" require-asterisk-position="left" style="max-width: 560px;">
                <el-form-item label="用户名" required>
                    <el-select v-model="addData.tsuname" filterable size="default" class="updataform" :disabled="rootdisable">
                        <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="项目名字" required>
                    <el-select v-model="addData.tspname" filterable size="default" class="updataform">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="标注方" required>
                    <el-select v-model="addData.tswaibao" filterable size="default" class="updataform">
                        <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="任务ID">
                    <el-input v-model="addData.tstask_id" type="number" />
                </el-form-item>
                <el-form-item label="日期" required>
                    <el-date-picker class="updataform" v-model="addData.tsdtime" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" />
                </el-form-item>
                <el-form-item label="任务类型" required>
                    <el-select v-model="addData.tskind" filterable size="default" class="updataform">
                        <el-option v-for="item in AnnoTaskKindList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="图片/视频数量" required>
                    <el-input v-model="addData.tspnums" type="number" min="1" placeholder="图片/点云/视频数量" />
                </el-form-item>
                <el-form-item label="框数/时长">
                    <el-input v-model="addData.tsknums" placeholder="999/00:00:00" />
                </el-form-item>
                <el-form-item label="工时" required>
                    <el-input v-model="addData.tsptimes" type="number" min="0.1" step="0.1" />
                </el-form-item>
                <el-button type="primary" class="updataform" @click="adddata">添加</el-button>
            </el-form>
        </el-dialog>
        <!-- update dialog -->
        <el-dialog v-model="updatemodel" title="修改数据" width="30%" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 500px;">
            <el-form label-position="left" label-width="110px" :model="updateData" require-asterisk-position="left" style="max-width: 560px;">
                <el-form-item label="ID" required>
                    <el-input v-model="updateData.id" disabled />
                </el-form-item>
                <el-form-item label="用户名" required>
                    <el-select v-model="updateData.tsuname" filterable size="default" class="updataform" :disabled="rootdisable">
                        <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="项目名字" required>
                    <el-select v-model="updateData.tspname" filterable size="default" class="updataform">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="标注方" required>
                    <el-select v-model="updateData.tswaibao" filterable size="default" class="updataform">
                        <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="任务ID">
                    <el-input v-model="updateData.tstask_id" type="number" />
                </el-form-item>
                <el-form-item label="日期" required>
                    <el-date-picker v-model="updateData.tsdtime" type="date" :size="size" :clearable="false" value-format="YYYY-MM-DD" format="YYYY-MM-DD" style="width: 100%;" />
                </el-form-item>
                <el-form-item label="任务类型" required>
                    <el-select v-model="updateData.tskind" filterable size="default" class="updataform">
                        <el-option v-for="item in AnnoTaskKindList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="图片/视频数量" required>
                    <el-input v-model="updateData.tspnums" type="number" min="1" placeholder="图片/点云/视频数量" />
                </el-form-item>
                <el-form-item label="框数/时长">
                    <el-input v-model="updateData.tsknums" placeholder="999/00:00:00" />
                </el-form-item>
                <el-form-item label="工时" required>
                    <el-input v-model="updateData.tsptimes" type="number" min="0.1" step="0.1" />
                </el-form-item>
                <el-button type="primary" class="updataform" @click="changedata">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'tsdtime', order: 'descending' }" key="id" border highlight-current-row style="width: 100%;" height="800">
            <el-table-column prop="id" label="ID" />
            <el-table-column prop="tsuname" label="用户名" width="110" />
            <el-table-column prop="tspname" label="项目名字" width="210" />
            <el-table-column prop="tswaibao" label="标注方" width="80">
                <template #default="scope">
                    <el-tag>{{ scope.row.tswaibao }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="tstask_id" label="任务ID" width="120" />
            <el-table-column prop="tsdtime" label="日期" width="120" />
            <el-table-column prop="tskind" label="	任务类型" width="120" />
            <el-table-column prop="tspnums" label="	图片/点云/视频数量" width="150" />
            <el-table-column prop="tsknums" label="	框数/属性/时长" width="180" />
            <el-table-column prop="tsptimes" label="工时" width="140" />
            <el-table-column width="180px" fixed="right" align="center" v-if="!roothiden">
                <template #header>
                    <el-button type="primary" class="updataform" @click="addmodelck">添加</el-button>
                </template>
                <template #default="scope">
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" v-if="!rootdisable">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!-- pagination -->
        <div>
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[20, 50, 100]"
                :small="small" :disabled="disabled" :background="background"
                layout="total, sizes, prev, pager, next, jumper" :total="count" @size-change="handleSizeChange"
                @current-change="handleCurrentChange" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import * as XLSX from "xlsx";
import { ElMessageBox } from 'element-plus';
import { Share, Refresh } from '@element-plus/icons-vue';
import { user_list, project_list, supplier_list, anno_task_kind_list } from "@/api/public";
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { search_annoteam_data, add_anno_task_data, get_anno_task_data_one, get_all_anno_team_data, update_anno_task_data, delete_anno_task_data } from "@/api/annoteam";

document.title = "标注团队任务记录"

const UserList = ref([]);
const SupplierList = ref([]);
const ProjectList = ref([]);
const AnnoTaskKindList = ref([]);

const tableData = ref([]);
const count = ref(0);
const currentPage = ref(1);
const pageSize = ref(20);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);

const rootdisable:any = ref(window.localStorage.getItem("level") == "1" ? false : true);
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);
const username:any = ref(window.localStorage.getItem("zhuname"));
const intval:any = ref(null);

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
        roothiden.value = window.localStorage.getItem("level") == "3" ? true : false;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

const now_date = new Date();
const now_month = now_date.getMonth() + 1 < 10 ? "0" + (now_date.getMonth() + 1) : now_date.getMonth() + 1;
const now_day = now_date.getDate() < 10 ? "0" + now_date.getDate() : now_date.getDate();
const now_now_date = now_date.getFullYear() + "-" + now_month + "-" + now_day;
const datarear = ref([now_date.getFullYear() + "-01-01", now_now_date]);
const searchData = ref({ "uname": "", "pname": "", "begin_time": "", "last_time": "", "task_id": "", "task_kind": "", "supplier": "" });

const addmodel = ref(false);
const addData = ref({ "tsuname": "", "tspname": "", "tswaibao": "", "tstask_id": "", "tsdtime": now_now_date, "tskind": "", "tspnums": "", "tsknums": "", "tsptimes": "" });

const updatemodel = ref(false);
const updateData = ref({ "id": 0, "tsuname": "", "tspname": "", "tswaibao": "", "tstask_id": "", "tsdtime": "", "tskind": "", "tspnums": 0, "tsknums": "", "tsptimes": 0.0 });

const size = ref<'default' | 'large' | 'small'>('default');

// show
user_list().then((res) => {
    UserList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

project_list().then((res) => {
    ProjectList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

supplier_list().then((res) => {
    SupplierList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

anno_task_kind_list().then((res) => {
    AnnoTaskKindList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})

const get_all_data = () => {
    if (datarear.value != null) {
        searchData.value.begin_time = datarear.value[0];
        searchData.value.last_time = datarear.value[1];
    }
    else {
        searchData.value.begin_time = "";
        searchData.value.last_time = "";
    }

    search_annoteam_data(searchData.value, currentPage.value, pageSize.value).then((res: any) => {
        tableData.value = res.data;
        count.value = res.count;
    }).catch((err) => {
        console.log(err);
    })
}

get_all_data();

// size and current change
const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_all_data();
}
const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_all_data();
}

// export table data
const export_table_data = () => {
    get_all_anno_team_data(searchData.value).then((res: any) => {
        const data = XLSX.utils.json_to_sheet(res.sources)//此处tableData.value为表格的数据
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, data, 'annoteam')//test-data为自定义的sheet表名
        XLSX.writeFile(wb, 'annoteam.xlsx')//test.xlsx为自定义的文件名
    }).catch((err) => { console.log(err) });
}

// reset
const reset = () => {
    searchData.value = { "uname": "", "pname": "", "begin_time": "", "last_time": "", "task_id": "", "task_kind": "", "supplier": "" };
    datarear.value = [now_date.getFullYear() + "-01-01", now_now_date];
    get_all_data();
}

// add
const addmodelck = () => {
    addData.value = { "tsuname": username.value, "tspname": "", "tswaibao": "", "tstask_id": "", "tsdtime": now_now_date, "tskind": "", "tspnums": "", "tsknums": "", "tsptimes": "" };
    addmodel.value = true;
}

const adddata = () => {
    if (addData.value.tspname == "") { public_elmsg_warning("请填写项目名字 !"); }
    else if (addData.value.tswaibao == "") { public_elmsg_warning("请填写标注方 !"); }
    else if (addData.value.tsptimes == "") { public_elmsg_warning("请填写工时 !"); }
    else if (addData.value.tsptimes <= "0") { public_elmsg_warning("工时不能小于0 !"); }
    else if (addData.value.tskind == "") { public_elmsg_warning("请填写任务类型 !"); }
    else if (addData.value.tsdtime == null) { public_elmsg_warning("请选择日期 !"); }
    else if (addData.value.tspnums == "") { public_elmsg_warning("请填写标注数量 !"); }
    else if (addData.value.tspnums <= "0") { public_elmsg_warning("标注数量不能小于0 !"); }
    else {
        add_anno_task_data(username.value, addData.value.tsuname, addData.value.tspname, addData.value.tswaibao, addData.value.tstask_id, addData.value.tsdtime, addData.value.tskind, addData.value.tspnums, addData.value.tsknums, addData.value.tsptimes).then((res: any) => {
            if (res.code == 0) {
                addmodel.value = false;
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err) => { console.log(err) })
    }
}

// edit
const handleEdit = (index: any, row: any) => {
    console.log(index)
    if (row.tsuname != username.value && rootdisable.value) {public_elmsg_warning("您只能修改自己的数据喔 !");}
    else {
        ElMessageBox.confirm(`你确定要修改 ID 为 ${row.id} 的数据吗?`,'UPDATE',{confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning'}).then(() => {
            get_anno_task_data_one(row.id).then((res: any) => {
                updateData.value = res.data[0];
            }).catch((err) => { console.log(err) });
            updatemodel.value = true;
        })
        .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
    }
}

const changedata = () => {
    if (updateData.value.tsdtime == null) { public_elmsg_warning("请选择日期 !"); }
    else if (updateData.value.tspnums <= 0) { public_elmsg_warning("图片数量不能小于0 !"); }
    else if (updateData.value.tsptimes <= 0) { public_elmsg_warning("工时不能小于0 !"); }
    else {
        update_anno_task_data(username.value, updateData.value.id, updateData.value.tsuname, updateData.value.tspname, updateData.value.tswaibao, updateData.value.tstask_id, updateData.value.tsdtime, updateData.value.tskind, updateData.value.tspnums, updateData.value.tsknums, updateData.value.tsptimes).then((res: any) => {
            if (res.code == -1) { public_elmsg_warning(res.data); }
            else {
                updatemodel.value = false;
                public_elmsg_success("修改成功 !");
                get_all_data();

            }
        }).catch((err) => { console.log(err) });
    }
};
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
        delete_anno_task_data(row.id, username.value).then((res: any) => {
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
.tools-div {
    display: flex;
}

.search-btn {
    margin-left: 15px;
}

.updataform {
    width: 100%;
}
</style>