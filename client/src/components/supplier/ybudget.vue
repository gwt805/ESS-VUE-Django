<template>
    <div id="layout">
        <div class="tools-div">
            <div class="m-4">
                <el-input v-model="search_year" type="number" @change="get_all_data"><template #append>年</template></el-input>
            </div>
            <h3>{{ search_year }} 年项目预算管理</h3>
        </div>
        <!-- add data dialog -->
        <el-dialog v-model="addmodel" title="添加数据" width="20%" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 400px;">
            <el-form label-position="top" label-width="100px" :model="addData" require-asterisk-position="left">
                <el-form-item label="年份" required>
                    <el-input v-model="addData.year" type="number" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="主预算项目名" required>
                    <el-select v-model="addData.mpname" filterable class="addmodelform" :disabled="rootdisable">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="使用如上项目预算的项目" required>
                    <el-select v-model="addData.pnamel" multiple filterable default-first-option :reserve-keyword="false" placeholder="选择使用如上项目预算的项目" class="addmodelform" :disabled="rootdisable">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item"/>
                    </el-select>
                </el-form-item>
                <el-button type="primary" class="addmodelform" @click="addmodelck" :disabled="rootdisable">添加</el-button>
            </el-form>
        </el-dialog>
        <!-- update data dialog -->
        <el-dialog v-model="updmodel" title="修改数据" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 500px;">
            <el-form label-position="top" label-width="100px" :model="addData" require-asterisk-position="left">
                <el-form-item label="ID" required>
                    <el-input type="text" v-model="updData.id" disabled />
                </el-form-item>
                <el-form-item label="年份" required>
                    <el-input type="number" v-model="updData.year" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="主预算项目名" required>
                    <el-select v-model="updData.mpname" filterable size="default" class="addmodelform" :disabled="rootdisable">
                            <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                        </el-select>
                </el-form-item>
                <el-form-item label="使用如上项目预算的项目" required>
                    <el-select v-model="updData.pnamel" multiple filterable default-first-option :reserve-keyword="false" placeholder="选择使用如上项目预算的项目" class="addmodelform" :disabled="rootdisable">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item"/>
                    </el-select>
                </el-form-item>
                <el-button type="primary" class="upd-dialog-btn" @click="upd_upd_btn" :disabled="rootdisable">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'used_ratio', order: 'descending' }" border highlight-current-row style="width: 100%;" height="800" table-layout="fixed">
            <el-table-column prop="id" label="ID" width="100" fixed="left" />
            <el-table-column prop="year" label="年份" width="100" fixed="left" />
            <el-table-column prop="mpname" label="使用该项目的标注预算" width="210" fixed="left" />
            <el-table-column prop="pnamel" label="使用该项目预算的有哪些" fixed="left" />
            <el-table-column width="140px" fixed="right" align="center">
                <template #header>
                    <el-button type="primary" class="addmodelform" @click="modelck" :disabled="rootdisable">添加</el-button>
                </template>
                <template #default="scope">
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)" :disabled="rootdisable">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" :disabled="rootdisable">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="demo-pagination-block">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[20, 50, 100]"
                :small="small" :disabled="disabled" :background="background"
                layout="total, sizes, prev, pager, next, jumper" :total="count" @size-change="handleSizeChange"
                @current-change="handleCurrentChange" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { project_list } from "@/api/public";
import { ElMessageBox } from "element-plus";
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { admin_get_ybudget_data, admin_add_ybudget_data, admin_get_ybudget_data_one, admin_update_ybudget_data, admin_delete_ybudget_data } from "@/api/admin";

const now_year = new Date().getFullYear();
const search_year = ref(now_year);
const addmodel = ref(false);

const ProjectList = ref([]);
const tableData = ref([]);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);

const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);
const username:any = ref(window.localStorage.getItem("zhuname"));
const intval:any = ref(null);

const count = ref(0);
const currentPage = ref(1);
const pageSize = ref(20);

const updmodel = ref(false);
const updData = ref({ "id": 0, "year": now_year, "mpname": "", "pnamel": "" })

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

project_list().then((res) => {
    ProjectList.value = JSON.parse(res.data);
}).catch((err) => { console.log(err); })

const addData = ref({ "year": now_year, "mpname": "", "pnamel": "" })

const modelck = () => {
    addData.value = { "year": now_year, "mpname": "", "pnamel": "" };
    addmodel.value = true;
};

const get_all_data = () => {
    if (search_year.value <= 0) { public_elmsg_warning("请选择年份 !"); }
    else {
        admin_get_ybudget_data(search_year.value, currentPage.value, pageSize.value).then((res: any) => {
            tableData.value = res.data;
            count.value = res.count;
            if (res.code == -1) {public_elmsg_warning(res.msg);}
        }).catch((err:any) => { console.log(err); });
    }
};
get_all_data();

const addmodelck = () => {
    let flag = true;
    if (addData.value.year <= 0) {
        flag = false;
        public_elmsg_warning("请选择正确的年份 !");
    }
    else {
        flag = true;
    }
    if (addData.value.mpname == "") {
        flag = false;
        public_elmsg_warning("请填写主项目名称 !");
    }
    else {
        flag = true;
    }
    if (addData.value.pnamel == "") {
        flag = false;
        public_elmsg_warning("请填正确填写使用如上项目预算的项目 !");
    }
    else {
        flag = true;
    }

    if (flag) {
        admin_add_ybudget_data(username.value, addData.value.year, addData.value.mpname, addData.value.pnamel).then((res: any) => {
            if (res.code == 0) {
                addmodel.value = false;
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err) => { console.log(err); });
    }

};

const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_all_data();
}
const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_all_data();
}

const handleEdit = (index: any, row: any) => {
    console.log(index);
    ElMessageBox.confirm(
        `你确定要修改 ID 为 ${row.id} 的数据吗?`,
        'UPDATE',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
    .then(() => {
        admin_get_ybudget_data_one(row.id).then((res: any) => {
            if (res.code == 0) {
                updData.value = res.data;
                updmodel.value = true;
            }
        }).catch((err) => { console.log(err); });
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
};

const upd_upd_btn = () => {
    if (updData.value.pnamel == "") { public_elmsg_warning("请填写使用如上项目预算的项目 !"); }
    else {
        admin_update_ybudget_data(username.value, updData.value.id, updData.value.year, updData.value.mpname, updData.value.pnamel).then((res: any) => {
            if (res.code == 0) {
                updmodel.value = false;
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err) => { console.log(err); });
    }
};

const handleDelete = (index: any, row: any) => {
    console.log(index);
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
        admin_delete_ybudget_data(username.value, row.id).then((res: any) => {
            if (res.code == 0) {
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err) => { console.log(err) });
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消删除`); })
};

</script>

<style scoped>
.tools-div {
    display: flex;
}

h3 {
    margin: auto;
}

.addmodelform {
    display: block;
    width: 100%;
}

.upd-dialog-btn {
    display: inline-block;
    width: 100%;
    margin-top: 20px;
}
</style>