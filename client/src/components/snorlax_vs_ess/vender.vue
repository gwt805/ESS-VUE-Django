<template>
    <div id="layout">
        <!-- add data dialog -->
        <el-dialog v-model="addmodel" title="添加数据" width="20%" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 500px;">
            <el-form label-position="top" label-width="100px" :model="addData" require-asterisk-position="left">
                <el-form-item label="Snorlax 供应商名" required>
                    <el-input v-model="addData.slvender" autocomplete placeholder="请填写 Snorlax 供应商名" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="ESS 对应的供应商名" required>
                    <el-select v-model="addData.essvender" filterable class="addmodelform" :disabled="rootdisable">
                        <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
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
                <el-form-item label="Snorlax 供应商名" required>
                    <el-input v-model="updData.slvender" autocomplete placeholder="请填写 Snorlax 供应商名" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="ESS 供应商名" required>
                    <el-select v-model="updData.essvender" filterable size="default" class="addmodelform" :disabled="rootdisable">
                            <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
                        </el-select>
                </el-form-item>
                <el-button type="primary" class="upd-dialog-btn" @click="upd_upd_btn" :disabled="rootdisable">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'used_ratio', order: 'descending' }" border highlight-current-row style="width: 100%;" height="830" table-layout="fixed">
            <el-table-column prop="id" label="ID" width="100" fixed="left" />
            <el-table-column prop="slvender" label="Snorlax 供应商名" fixed="left" />
            <el-table-column prop="essvender" label="ESS 对应的供应商名" fixed="left" />
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
import { supplier_list } from "@/api/public";
import { ElMessageBox } from "element-plus";
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { admin_get_slessvd, admin_add_slessvd, admin_get_slessvd_one, admin_update_slessvd, admin_delete_slessvd } from "@/api/snorlax_vs_ess";

const addmodel = ref(false);

const SupplierList = ref([]);
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
const updData = ref({ "id": 0, "essvender": "", "slvender": "" })

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

supplier_list().then((res) => {
    SupplierList.value = JSON.parse(res.data);
}).catch((err) => { console.log(err); })

const addData = ref({ "essvender": "", "slvender": "" })

const modelck = () => {
    addData.value = { "essvender": "", "slvender": "" };
    addmodel.value = true;
};

const get_all_data = () => {
    admin_get_slessvd( currentPage.value, pageSize.value).then((res: any) => {
        tableData.value = res.data;
        count.value = res.count;
        if (res.code == -1) {public_elmsg_warning(res.msg);}
    }).catch((err:any) => { console.log(err); });
};
get_all_data();

const addmodelck = () => {
    if (addData.value.slvender.trim() == "") {public_elmsg_warning("请填 Snorlax 供应商项名 !");}
    else if (addData.value.essvender == "") {public_elmsg_warning("请填写 ESS 对应的项目名 !");}
    else {
        admin_add_slessvd(username.value,  addData.value.essvender, addData.value.slvender.trim()).then((res: any) => {
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
        admin_get_slessvd_one(row.id).then((res: any) => {
            if (res.code == 0) {
                updData.value = res.data;
                updmodel.value = true;
            }
        }).catch((err) => { console.log(err); });
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
};

const upd_upd_btn = () => {
    if (updData.value.slvender.trim() == "") { public_elmsg_warning("请填写 Snorlax 供应商名 !");}
    else if (updData.value.essvender == "") { public_elmsg_warning("请选择 ESS 对应的供应商名 !"); }
    else {
        admin_update_slessvd(username.value, updData.value.id, updData.value.essvender, updData.value.slvender.trim()).then((res: any) => {
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
        admin_delete_slessvd(username.value, row.id).then((res: any) => {
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