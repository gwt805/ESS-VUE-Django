<template>
    <div id="layout">
        <div class="tools-div">
            <div class="m-4">
                <el-input v-model="search_year" type="number" @change="get_all_data"><template #append>年</template></el-input>
            </div>
            <h3>{{ search_year }} 年标注预算使用情况</h3>
        </div>
        <!-- add data dialog -->
        <el-dialog v-model="addmodel" title="添加数据" width="20%" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 400px;">
            <el-form label-position="left" label-width="80px" :model="addData" require-asterisk-position="left">
                <el-form-item label="年份" required>
                    <el-input v-model="addData.year" type="number" />
                </el-form-item>
                <el-form-item label="项目名字" required>
                    <el-select v-model="addData.proname" filterable clearable class="addmodelform">
                        <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="标注预算" required>
                    <el-input v-model="addData.money" type="number" />
                </el-form-item>
                <el-button type="primary" class="addmodelform" @click="addmodelck">添加</el-button>
            </el-form>
        </el-dialog>
        <!-- update data dialog -->
        <el-dialog v-model="updmodel" title="修改数据" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 700px;">
            <table class="updtable">
                <tr>
                    <th>ID</th>
                    <th>项目名字</th>
                    <th>标注预算</th>
                </tr>
                <tr>
                    <td><el-input type="text" v-model="updData.id" disabled /></td>
                    <td>
                        <el-select v-model="updData.proname" filterable size="default" class="addmodelform" :disabled="rootdisable">
                            <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
                        </el-select>
                    </td>
                    <td><el-input type="number" v-model="updData.ann_budget" :disabled="root_update" /></td>
                </tr>
                <tr>
                    <th>已使用费用</th>
                    <th>使用百分比</th>
                    <th></th>
                </tr>
                <tr>
                    <td><el-input type="number" v-model="updData.used_money" disabled /></td>
                    <td><el-input type="number" v-model="updData.used_ratio" disabled /></td>
                    <td></td>
                </tr>
                <tr>
                    <th>达到1/3预算日期</th>
                    <th>1/3 汇报日期</th>
                    <th>1/3 汇报文档</th>
                </tr>
                <tr>
                    <td><el-date-picker v-model="updData.reaching_one_third_budget_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" disabled /></td>
                    <td><el-date-picker v-model="updData.one_third_report_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" /></td>
                    <td><el-input v-model="updData.one_third_report_file" /></td>
                </tr>
                <tr>
                    <th>达到2/3预算日期</th>
                    <th>2/3 汇报日期</th>
                    <th>2/3 汇报文档</th>
                </tr>
                <tr>
                    <td><el-date-picker v-model="updData.reaching_two_third_budget_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" disabled /></td>
                    <td><el-date-picker v-model="updData.two_third_report_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" /></td>
                    <td><el-input v-model="updData.two_third_report_file" /></td>
                </tr>
                <tr>
                    <th>达到 100%预算日期</th>
                    <th>100% 汇报日期</th>
                    <th>100% 汇报文档</th>
                </tr>
                <tr>
                    <td><el-date-picker v-model="updData.reaching_third_third_budget_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" disabled /></td>
                    <td><el-date-picker v-model="updData.third_third_report_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" /></td>
                    <td><el-input v-model="updData.third_third_report_file" /></td>
                </tr>
            </table>
            <el-button type="primary" class="upd-dialog-btn" @click="upd_upd_btn">修改</el-button>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'used_ratio', order: 'descending' }" border highlight-current-row style="width: 100%;" height="800" table-layout="fixed">
            <el-table-column prop="id" label="ID" fixed="left" />
            <el-table-column prop="pname" label="项目名字" width="210" fixed="left" />
            <el-table-column prop="ann_budget" label="标注预算(元)" width="120" fixed="left" />
            <el-table-column prop="used_money" label="已使用费用(元)" width="120" fixed="left" />
            <el-table-column prop="used_ratio" label="使用百分比(%)" sortable width="150" fixed="left" />
            <el-table-column prop="reaching_one_third_budget_time" label="达到1/3预算日期" width="130" fixed="left" />
            <el-table-column prop="one_third_report_time" label="1/3 汇报日期" width="110" />
            <el-table-column prop="one_third_report_file" label="1/3 汇报文档" width="110" />
            <el-table-column prop="reaching_two_third_budget_time" label="达到2/3预算日期" width="130" />
            <el-table-column prop="two_third_report_time" label="2/3 汇报日期" width="120" />
            <el-table-column prop="two_third_report_file" label="2/3 汇报文档" width="140" />
            <el-table-column prop="reaching_third_third_budget_time" label="达到 100%预算日期" width="150" />
            <el-table-column prop="third_third_report_time" label="100% 汇报日期" width="130" />
            <el-table-column prop="third_third_report_file" label="100% 汇报文档" width="130" />
            <el-table-column width="140px" fixed="right" align="center" v-if="!roothiden">
                <template #header>
                    <el-button type="primary" class="addmodelform" @click="modelck">添加</el-button>
                </template>
                <template #default="scope">
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" v-if="!rootdisable">删除</el-button>
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
import { add_budget_data, get_budget_all_data, get_budget_one_data, update_budget_data, delete_budget_data } from "@/api/supplier";

const now_year = new Date().getFullYear();
const search_year = ref(now_year);
const addmodel = ref(false);

const ProjectList = ref([]);
const tableData = ref([]);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);
const size = ref<'default' | 'large' | 'small'>('default');

const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);
const username:any = ref(window.localStorage.getItem("zhuname"));
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);
const intval:any = ref(null);

const count = ref(0);
const currentPage = ref(1);
const pageSize = ref(20);

const updmodel = ref(false);
const root_update = ref(window.localStorage.getItem("level") == "1" ? false : true)
const updData = ref({ "id": 0, "proname": "", "ann_budget": 0, "used_money": 0, "used_ratio": 0, "reaching_one_third_budget_time": "", "one_third_report_time": "", "one_third_report_file": "", "reaching_two_third_budget_time": "", "two_third_report_time": "", "two_third_report_file": "", "reaching_third_third_budget_time": "", "third_third_report_time": "", "third_third_report_file": "" })

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
        roothiden.value = window.localStorage.getItem("level") == "3" ? true : false;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

project_list().then((res) => {
    ProjectList.value = JSON.parse(res.data);
}).catch((err) => { console.log(err); })

const addData = ref({ "year": now_year, "proname": "", "money": 0 })

const modelck = () => {
    addData.value = { "year": now_year, "proname": "", "money": 0 };
    addmodel.value = true;
};

const get_all_data = () => {
    if (search_year.value <= 0) { public_elmsg_warning("请选择年份 !"); }
    else {
        get_budget_all_data(search_year.value, currentPage.value, pageSize.value).then((res: any) => {
            tableData.value = res.data;
            count.value = res.count;
            if (res.code == -1) {public_elmsg_warning(res.msg);}
        }).catch((err) => { console.log(err); });
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
    if (addData.value.proname == "") {
        flag = false;
        public_elmsg_warning("请填写项目名称 !");
    }
    else {
        flag = true;
    }
    if (addData.value.money <= 0) {
        flag = false;
        public_elmsg_warning("请填写正确的标注预算 !");
    }
    else {
        flag = true;
    }

    if (flag) {
        add_budget_data(username.value, addData.value.year, addData.value.proname, addData.value.money).then((res: any) => {
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
        get_budget_one_data(row.id).then((res: any) => {
            if (res.code == 0) {
                updData.value = res.data;
                updmodel.value = true;
            }
        }).catch((err) => { console.log(err); });
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
};

const upd_upd_btn = () => {
    if (updData.value.ann_budget <= 0) { public_elmsg_warning("标注预算填写错误 !"); }
    else {
        update_budget_data(username.value, updData.value.id, updData.value.proname, updData.value.ann_budget, updData.value.one_third_report_time, updData.value.one_third_report_file, updData.value.two_third_report_time, updData.value.two_third_report_file, updData.value.third_third_report_time, updData.value.third_third_report_file).then((res: any) => {
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
        delete_budget_data(username.value, row.id).then((res: any) => {
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

.updtable {
    width: 100%;
    height: 300px;
    border-collapse: collapse;
}

.updtable tr {
    height: 40px;
}

.updtable tr:not(:last-child) {
    border-bottom: 1px solid #dddddd63;
}

.upd-dialog-btn {
    display: inline-block;
    width: 100%;
    margin-top: 20px;
}
</style>