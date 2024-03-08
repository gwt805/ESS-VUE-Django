<template>
    <div id="layout">
        <!-- add -->
        <el-dialog v-model="addmodel" title="添加供应商名字" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 550px;">
            <el-form label-position="left" label-width="90px" :model="adddata" style="max-width: 550px">
                <el-form-item label="供应商名字">
                    <el-input v-model="adddata.name" :disabled="rootdisable" />
                </el-form-item>
                <el-button type="primary" class="btn" @click="addproject" :disabled="rootdisable">添加</el-button>
            </el-form>
        </el-dialog>
        <!-- update -->
        <el-dialog v-model="updmodel" title="修改供应商名字" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 550px;">
            <el-form label-position="left" label-width="90px" :model="upddata" style="max-width: 550px">
                <el-form-item label="ID">
                    <el-input v-model="upddata.id" disabled />
                </el-form-item>
                <el-form-item label="供应商名字">
                    <el-input v-model="upddata.name" :disabled="rootdisable" />
                </el-form-item>
                <el-button type="primary" class="btn" @click="updprojectinfo" :disabled="rootdisable">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'tsdtime', order: 'descending' }" key="id" border highlight-current-row style="width: 100%;" height="830">
            <el-table-column prop="id" label="ID" align="center" />
            <el-table-column prop="name" label="项目名字" />
            <el-table-column label="操作" width="180px" fixed="right" align="center" v-if="!roothiden">
                <template #header>
                    <el-button type="primary" class="btn" @click="addmodelck" :disabled="rootdisable">添加</el-button>
                </template>
                <template #default="scope">
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)" :disabled="rootdisable">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" :disabled="rootdisable">删除</el-button>
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
import { ElMessageBox } from 'element-plus';
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { admin_get_supplier_info_list, admin_add_supplier, admin_get_supplier_info, admin_update_supplier_info, admin_delete_psupplier } from "@/api/admin";

const count = ref(0);
const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);

const updmodel = ref(false);
const upddata = ref({"id": 0, "name": ""});

const addmodel = ref(false);
const adddata = ref({"name": ""});

const intval:any = ref(null);
const username:any = ref(window.localStorage.getItem("zhuname"));
const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
        roothiden.value = window.localStorage.getItem("level") == "3" ? true : false;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

const get_all_data = () => {
    admin_get_supplier_info_list(currentPage.value, pageSize.value).then((res:any) => {
            tableData.value = res.data;
            count.value = res.count;
            if (res.code == -1) { public_elmsg_warning(res.msg);};
    });
};
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

// add
const addmodelck = () => {
    addmodel.value = true;
    adddata.value = {"name": ""};
};
const addproject = () => {
    if (adddata.value.name.trim() == "") { public_elmsg_warning("项目名不能为空"); }
    else {
        admin_add_supplier(username.value, adddata.value.name).then((res:any) => {
            if (res.code == 0) {
                addmodel.value = false;
                public_elmsg_success(res.data);
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err)=>{console.log(err)});
    }
};

// edit info
const handleEdit = (index: any, row: any) => {
    console.log(index);
    ElMessageBox.confirm(`你确定要修改 ID 为 ${row.id} 的项目名字吗?`,'UPDATE',{confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning'}).then(() => {
        admin_get_supplier_info(row.id).then((res: any) => {
            upddata.value = {"id": row.id, "name": res.data};
            updmodel.value = true;
        }).catch((err) => { console.log(err) });
        updmodel.value = true;
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
}

const updprojectinfo = () => {
    if (upddata.value.name == "") { public_elmsg_warning("项目名字不能为空"); }
    else {
        admin_update_supplier_info(username.value, upddata.value.id, upddata.value.name.trim()).then((res:any) => {
            if (res.code == 0) {
                public_elmsg_success(res.data);
                get_all_data();
                updmodel.value = false;
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err)=>{ console.log(err) });
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
        admin_delete_psupplier(username.value, row.id).then((res: any) => {
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
.btn {
    width: 100%;
}
</style>