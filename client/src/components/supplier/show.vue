<template>
  <div id="layout">
    <div class="tools-div">
      <div class="m-4">
        <el-select v-model="searchData.pname" filterable clearable placeholder="项目名字" style="width: 200px" @change="get_all_data">
          <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
      <div class="m-4">
        <el-select v-model="searchData.supplier" filterable clearable placeholder="标注方" style="width: 100px" @change="get_all_data">
          <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
      <div class="block">
        <el-date-picker v-model="send_datarear" type="daterange" range-separator="-" start-placeholder="送标开始日期" end-placeholder="送标结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" style="width: 250px;" @change="get_all_data" />
      </div>
      <div class="block">
        <el-date-picker v-model="pay_datarear" type="daterange" range-separator="-" start-placeholder="交付开始日期" end-placeholder="交付结束日期" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" style="width: 250px;" @change="get_all_data" />
      </div>
      <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
      <el-button type="primary" :icon="Share" @click="export_table_data">导出</el-button>
    </div>
    <!-- add data dialog -->
    <el-dialog v-model="addmodel" title="添加数据" width="30%" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 550px;">
      <el-form label-position="left" label-width="100px" :model="addData" style="max-width: 560px;" require-asterisk-position="left">
        <el-form-item label="研发名字" required label-width="120">
          <el-select v-model="addData.user" filterable size="default" class="updataform" :disabled="rootdisable">
            <el-option v-for="item in UserList" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名字" required label-width="120">
          <el-select v-model="addData.pname" filterable size="default" class="updataform">
            <el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="送标批次" required label-width="120">
          <el-input v-model="addData.send_data_batch" />
        </el-form-item>
        <el-form-item label="送标时间" required label-width="120">
          <el-date-picker class="updataform" v-model="addData.send_data_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="送标样本数量" required label-width="120">
          <el-input v-model="addData.pnums" type="number" min="1" />
        </el-form-item>
        <el-form-item label="数据来源" required label-width="120">
          <el-select v-model="addData.data_source" filterable size="default" class="updataform">
            <el-option v-for="item in addmodel_source_list" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="场景分布" required label-width="120">
          <el-input v-model="addData.scene" />
        </el-form-item>
        <el-form-item label="送标原因" required label-width="120">
          <el-input v-model="addData.send_reason" />
        </el-form-item>
        <el-form-item label="关键帧抽取方式" required label-width="120">
          <el-input v-model="addData.key_frame_extracted_methods" />
        </el-form-item>
        <el-form-item label="是否首次标注" required label-width="120">
          <el-select v-model="addData.ann_field_flag" filterable size="default" class="updataform">
            <el-option v-for="item in addmodel_is_first_anno" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>

        <el-form-item label="标注方" required label-width="120">
          <el-select v-model="addData.wb_name" filterable size="default" class="updataform">
            <el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-button type="primary" class="updataform" @click="adddata">添加</el-button>
      </el-form>
    </el-dialog>
    <!-- update data dialog -->
    <el-dialog v-model="upd_anno_money_model" title="金额添加/修改" width="30%" center :close-on-click-modal="false" :close-on-press-escape="false" :draggable="true" style="width: 550px;">
      <el-form label-position="left" label-width="100px" :model="addData" style="max-width: 560px;" require-asterisk-position="left">
        <el-form-item label="虚拟ID" label-width="100">
          <el-input v-model="upd_money_data.id" disabled />
        </el-form-item>
        <el-form-item label="结算方式" required label-width="100">
          <el-select v-model="upd_money_data.settlement_method" clearable filterable size="default" class="updataform">
            <el-option v-for="item in JSFSList" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="交付准确率" label-width="100">
          <el-input v-model="upd_money_data.recovery_precision" type="number" min="1" @keydown="handleInput"/>
        </el-form-item>
        <el-form-item label="标注数量" required label-width="100">
          <el-input v-model="upd_money_data.knums" type="number" min="1" @keydown="handleInput" />
        </el-form-item>
        <el-form-item label="单价" required label-width="100">
          <el-input v-model="upd_money_data.unit_price" type="number" min="0.1" @keydown="handleInput" />
        </el-form-item>
        <el-button type="primary" class="updataform" @click="upd_money_btn" v-if="is_edit_model">修改</el-button>
        <el-button type="primary" class="updataform" @click="upd_money_btn" v-if="is_edit_model == false">添加</el-button>
      </el-form>
    </el-dialog>
    <el-dialog v-model="updmodel" title="修改数据" style="min-width: 600px; margin-top: 60px;" center :close-on-click-modal="false" :close-on-press-escape="false" >
      <table class="updtable1">
        <tr>
          <th>ID</th>
          <th>研发名字</th>
          <th>项目名字</th>
          <th>送标批次</th>
        </tr>
        <tr>
          <td><el-input type="text" v-model="updTableData.id" disabled /></td>
          <td><el-select v-model="updTableData.user" filterable size="default" class="updataform" :disabled="rootdisable"><el-option v-for="item in UserList" :key="item" :label="item" :value="item" /></el-select></td>
          <td><el-select v-model="updTableData.pname" filterable size="default" class="updataform" :disabled="rootdisable"><el-option v-for="item in ProjectList" :key="item" :label="item" :value="item" /></el-select></td>
          <td><el-input type="text" v-model="updTableData.send_data_batch" :disabled="rootdisable" /></td>
        </tr>
        <tr>
          <th>送标时间</th>
          <th>送标样本数量</th>
          <th>数据来源</th>
          <th>场景分布</th>
        </tr>
        <tr>
          <td><el-date-picker class="updataform" v-model="updTableData.send_data_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" :disabled="rootdisable" /></td>
          <td><el-input type="number" v-model="updTableData.pnums" :disabled="rootdisable" /></td>
          <td><el-select v-model="updTableData.data_source" filterable size="default" class="updataform" :disabled="rootdisable"><el-option v-for="item in addmodel_source_list" :key="item" :label="item" :value="item" /></el-select></td>
          <td><el-input type="text" v-model="updTableData.scene" :disabled="rootdisable" /></td>
        </tr>
        <tr>
          <th>送标原因</th>
          <th>关键帧抽取方式</th>
          <th>外包名字</th>
          <th>是否首次标注</th>
        </tr>
        <tr>
          <td><el-input type="text" v-model="updTableData.send_reason" :disabled="rootdisable" /></td>
          <td><el-input type="text" v-model="updTableData.key_frame_extracted_methods" :disabled="rootdisable" /></td>
          <td><el-select v-model="updTableData.wb_name" filterable size="default" class="updataform" :disabled="rootdisable"><el-option v-for="item in SupplierList" :key="item" :label="item" :value="item" /></el-select></td>
          <td><el-select v-model="updTableData.ann_field_flag" filterable size="default" class="updataform" :disabled="rootdisable"><el-option v-for="item in addmodel_is_first_anno" :key="item" :label="item" :value="item" /></el-select></td>
        </tr>
        <tr>
          <th>AnnotationTaskId</th>
          <th>开始验收时间</th>
          <th>结束验收时间</th>
          <th>收到标注结果时间</th>
        </tr>
        <tr>
          <td><el-input type="number" v-model="updTableData.anno_task_id" disabled /></td>
          <td><el-date-picker class="updataform" v-model="updTableData.begin_check_data_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" /></td>
          <td><el-date-picker class="updataform" v-model="updTableData.last_check_data_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" /></td>
          <td><el-date-picker class="updataform" v-model="updTableData.get_data_time" type="date" :size="size" value-format="YYYY-MM-DD" format="YYYY-MM-DD" :clearable="false" style="width: 100%;" /></td>
        </tr>
      </table>
      <div class="upd-dialog-tab-div">
        <el-table :data="updTableData.ann_meta_data" highlight-current-row style="width: 100%; height: 300px;" table-layout="fixed" @cell-click="handleCellClick">
          <el-table-column prop="settlement_method" label="结算方式" />
          <el-table-column prop="recovery_precision" label="交付准确率" />
          <el-table-column prop="knums" label="标注数" />
          <el-table-column prop="unit_price" label="单价" />
          <el-table-column fixed="right" width="60">
            <el-button link type="warning" size="small">编辑</el-button>
          </el-table-column>
          <el-table-column fixed="right" width="60">
            <template #default="scope">
              <el-button link type="danger" size="small" @click.prevent="deleteRow(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button class="mt-4" type="success" plain style="width: 100%" @click="onAddItem">新增</el-button>
        <el-button type="info" plain style="width: 50%; margin-top:5px; float:left; margin-left:-12px;" @click="updmodelcalbtn">取消</el-button>
        <el-button type="primary" plain style="width: 50%; margin-top:5px; float:left;" @click="updmodeleditbtn">修改</el-button>
      </div>
    </el-dialog>
    <!-- show -->
    <el-table :data="tableData" :default-sort="{ prop: 'send_data_time', order: 'descending' }" border highlight-current-row style="width: 100%;" height="800" table-layout="fixed">
      <el-table-column prop="id" label="ID" fixed="left" />
      <el-table-column prop="user" label="研发" width="90" fixed="left" />
      <el-table-column prop="pname" label="项目名字" width="210" fixed="left" />
      <el-table-column prop="send_data_batch" label="送标批次" width="150" fixed="left" />
      <el-table-column prop="send_data_time" label="送标时间" sortable width="120" fixed="left" />
      <el-table-column prop="pnums" label="送标样本数量" width="120" fixed="left" />
      <el-table-column prop="data_source" label="数据来源" width="120" />
      <el-table-column prop="scene" label="场景分布" width="120" />
      <el-table-column prop="send_reason" label="送标原因" width="180" />
      <el-table-column prop="ann_field_flag" label="是否首次标注" width="120" />
      <el-table-column prop="key_frame_extracted_methods" label="关键帧抽取方式" width="140" />
      <el-table-column prop="begin_check_data_time" label="开始验收时间" width="140" />
      <el-table-column prop="last_check_data_time" label="结束验收时间" width="140" />
      <el-table-column prop="get_data_time" label="标注结果返回时间" sortable width="170" />
      <el-table-column prop="ann_meta_data" label="准确率&框数&结算方式&单价" width="220" />
      <el-table-column prop="anno_task_id" label="AnnotationTaskId" width="160" />
      <el-table-column prop="total_money" label="总价" fixed="right" />
      <el-table-column prop="wb_name" label="供应商" width="80" fixed="right">
        <template #default="scope">
          <el-tag>{{ scope.row.wb_name }}</el-tag>
        </template>
      </el-table-column>
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
    <div class="demo-pagination-block">
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[20, 50, 100]"
        :small="small" :disabled="disabled" :background="background" layout="total, sizes, prev, pager, next, jumper"
        :total="count" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import * as XLSX from "xlsx";
import { ElMessageBox } from 'element-plus';
import { Share, Refresh } from '@element-plus/icons-vue';
import { user_list, project_list, supplier_list } from "@/api/public";
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { get_supplier_data, get_all_supplier_task_data, get_supplier_task_data_one, add_supplier_task_data, update_supplier_task_data, delete_supplier_task_data, get_supplier_data_jsfs } from "@/api/supplier";

document.title = "送标记录展示"

const tableData = ref([1]);
const count = ref(0);
const currentPage = ref(1);
const pageSize = ref(20);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);
const size = ref<'default' | 'large' | 'small'>('default');

const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);
const username:any = ref(window.localStorage.getItem("zhuname"));
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);
const intval:any = ref(null);

const UserList = ref([]);
const SupplierList = ref([]);
const ProjectList = ref([]);
const JSFSList = ref([]);

const now_date = new Date();
const now_month = now_date.getMonth() + 1 < 10 ? "0" + (now_date.getMonth() + 1) : now_date.getMonth() + 1;
const now_day = now_date.getDate() < 10 ? "0" + now_date.getDate() : now_date.getDate();
const now_now_date = now_date.getFullYear() + "-" + now_month + "-" + now_day;

const send_datarear = ref([now_date.getFullYear() + "-01-01", now_now_date]);
const pay_datarear = ref(null);
const searchData = ref({ "pname": "", "supplier": "", "send_begin_time": "", "send_last_time": "", "pay_begin_time": "", "pay_last_time": "" });

const addmodel = ref(false);
const addmodel_source_list = ["人工采集", "回流数据"];
const addmodel_is_first_anno = ["首次标注", "返修标注"];
const addData = ref({ "user": "", "pname": "", "send_data_batch": "", "send_data_time": "", "pnums": 0, "data_source": "", "scene": "", "send_reason": "", "ann_field_flag": "", "key_frame_extracted_methods": "", "wb_name": "" });

const updmodel = ref(false);
const upd_anno_money_model = ref(false);
const is_edit_model = ref(true);
const updTableData = ref({ "id": "", "user": "", "pname": "", "send_data_batch": "", "send_data_time": "", "pnums": 0, "data_source": "", "scene": "", "send_reason": "", "ann_field_flag": "", "key_frame_extracted_methods": "", "wb_name": "", "anno_task_id": "", "begin_check_data_time": "", "last_check_data_time": "", "get_data_time": "", "ann_meta_data": [{ "settlement_method": "", "recovery_precision": "", "knums": "", "unit_price": "" }] });
const upd_money_data = ref({ "id": 0, "settlement_method": "", "recovery_precision": "", "knums": "", "unit_price": "" });

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
        roothiden.value = window.localStorage.getItem("level") == "3" ? true : false;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

user_list().then((res) => {
    UserList.value = JSON.parse(res.data);
}).catch((err) => {
    console.log(err);
})
project_list().then((res) => {
  ProjectList.value = JSON.parse(res.data);
}).catch((err) => { console.log(err); })

supplier_list().then((res) => {
  SupplierList.value = JSON.parse(res.data);
}).catch((err) => { console.log(err); })

get_supplier_data_jsfs().then((res: any) => {
  JSFSList.value = res.data
}).catch((err) => { console.log(err); })

const get_all_data = () => {
  if (send_datarear.value == null) {
    searchData.value.send_begin_time = "";
    searchData.value.send_last_time = "";
  }
  else {
    searchData.value.send_begin_time = send_datarear.value[0];
    searchData.value.send_last_time = send_datarear.value[1];
  }
  if (pay_datarear.value == null) {
    searchData.value.pay_begin_time = "";
    searchData.value.pay_last_time = "";
  }
  else {
    searchData.value.pay_begin_time = pay_datarear.value[0];
    searchData.value.pay_last_time = pay_datarear.value[1];
  }
  get_supplier_data(searchData.value.pname, searchData.value.supplier, searchData.value.send_begin_time, searchData.value.send_last_time, searchData.value.pay_begin_time, searchData.value.pay_last_time, currentPage.value, pageSize.value).then((res: any) => {
    tableData.value = res.data;
    count.value = res.count;
  });
}
get_all_data();

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
  addData.value = { "user": username.value, "pname": "", "send_data_batch": "", "send_data_time": now_now_date, "pnums": 0, "data_source": "", "scene": "", "send_reason": "", "ann_field_flag": "", "key_frame_extracted_methods": "", "wb_name": "" };
  addmodel.value = true;
}

const adddata = () => {
  if (addData.value.user == "") { public_elmsg_warning("请填写研发名字"); }
  else if (addData.value.pname == "") { public_elmsg_warning("请选择项目名字"); }
  else if (addData.value.send_data_batch.trim() == "") { public_elmsg_warning("请填写送标批次"); }
  else if (addData.value.send_data_time == null) { public_elmsg_warning("请选择送标时间"); }
  else if (addData.value.pnums <= 0) { public_elmsg_warning("请填写送标数量"); }
  else if (addData.value.data_source == "") { public_elmsg_warning("请填写数据来源"); }
  else if (addData.value.scene.trim() == "") { public_elmsg_warning("请填写场景分布"); }
  else if (addData.value.send_reason.trim() == "") { public_elmsg_warning("请填写送标原因"); }
  else if (addData.value.ann_field_flag == "") { public_elmsg_warning("请选择是否是首次标注"); }
  else if (addData.value.key_frame_extracted_methods == "") { public_elmsg_warning("请填写关键帧提取方式"); }
  else if (addData.value.wb_name == "") { public_elmsg_warning("请选择供应商"); }
  else {
    add_supplier_task_data(username.value, addData.value.user, addData.value.pname, addData.value.send_data_batch, addData.value.send_data_time, addData.value.pnums, addData.value.data_source, addData.value.scene, addData.value.send_reason, addData.value.key_frame_extracted_methods, addData.value.ann_field_flag, addData.value.wb_name).then((res: any) => {
      if (res.code == 0) {
        addmodel.value = false;
        public_elmsg_success(res.data);
        get_all_data();
      }
      else { public_elmsg_warning(res.data); }
    }).catch((err: any) => { console.log(err) });
  }
};

// update
const handleEdit = (index: any, row: any) => {
  console.log(index);
  ElMessageBox.confirm(`你确定要修改 ID 为 ${row.id} 的数据吗?`,'UPDATE', {confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning'}).then(() => {
    updmodel.value = true;
    get_supplier_task_data_one(row.id).then((res: any) => {
      if (res.code == 0) {
        updTableData.value = res.data;
      }
    }).catch((err: any) => { console.log(err) });
  })
  .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
}

const deleteRow = (index: number) => {
  if (index != 0) {
    updTableData.value.ann_meta_data.splice(index, 1)
  }
  else { public_elmsg_warning("首行不允许删除"); }
}

const onAddItem = () => {
  upd_anno_money_model.value = true;
  is_edit_model.value = false;
  upd_money_data.value = { "id": 0, "settlement_method": "", "recovery_precision": "", "knums": "", "unit_price": "" }
}

const handleCellClick = (row: any, column: any, cell: any, event: any) => {
  console.log(column)
  console.log(cell)
  if (event.target.innerText === "编辑") {
    upd_anno_money_model.value = true;
    is_edit_model.value = true;
    upd_money_data.value = { "id": updTableData.value.ann_meta_data.indexOf(row), "settlement_method": row.settlement_method, "recovery_precision": row.recovery_precision, "knums": row.knums, "unit_price": row.unit_price }
  }
};

const handleInput = (e:any) =>{
  let key = e.key;
  if (key === 'e' || key === 'E' || key === '+' || key === '-') {
    e.returnValue = false;
    return false;
  }
  return true;
}
const upd_money_btn = () => {
  let flag = true;
  if (upd_money_data.value.recovery_precision != "") {
    if (upd_money_data.value.settlement_method == "" || upd_money_data.value.knums == "" || upd_money_data.value.unit_price == "") {
      public_elmsg_warning("带 * 号的需同时填写 !");
      flag = false;
    }
    else {
      if (upd_money_data.value.recovery_precision != null && (Number(upd_money_data.value.recovery_precision) <= 0 || Number(upd_money_data.value.recovery_precision) > 100)) {
        flag = false;
        public_elmsg_warning("交付准确率需要 >0 且 <= 100");
      }
      if (Number(upd_money_data.value.knums) < 0) {
        flag = false;
        public_elmsg_warning("请填写正确的标注数量");
      }
      if (Number(upd_money_data.value.unit_price) < 0) {
        flag = false;
        public_elmsg_warning("请填写正确的单价");
      }
    }
  }
  else {
    if (upd_money_data.value.settlement_method != "" && (upd_money_data.value.knums == "" || upd_money_data.value.unit_price == "")) {
      public_elmsg_warning("带 * 号的需同时填写 !");
      flag = false;
    }
    else if (upd_money_data.value.knums != "" && (upd_money_data.value.settlement_method == "" || upd_money_data.value.unit_price == "")) {
      public_elmsg_warning("带 * 号的需同时填写 !");
      flag = false;
    }
    else if (upd_money_data.value.unit_price != "" && (upd_money_data.value.knums == "" || upd_money_data.value.settlement_method == "")) {
      public_elmsg_warning("带 * 号的需同时填写 !");
      flag = false;
    }
    else {
      if (upd_money_data.value.knums != "" && upd_money_data.value.settlement_method != "" && upd_money_data.value.unit_price != "") {
        console.log(4)
        if (Number(upd_money_data.value.knums) < 0) {
          flag = false;
          public_elmsg_warning("请填写正确的标注数量");
          console.log(1)
        }
        if (Number(upd_money_data.value.unit_price) < 0) {
          flag = false;
          public_elmsg_warning("请填写正确的单价");
          console.log(3)
        }
      }
    }
  }

  if (flag) {
    if (is_edit_model.value) { // edit
      const source_money_data = updTableData.value.ann_meta_data;
      source_money_data[upd_money_data.value.id] = {
        "settlement_method": upd_money_data.value.settlement_method,
        "recovery_precision": upd_money_data.value.recovery_precision,
        "knums": upd_money_data.value.knums,
        "unit_price": upd_money_data.value.unit_price
      }
      updTableData.value.ann_meta_data = source_money_data;
      upd_anno_money_model.value = false;
    }
    else { // add
      updTableData.value.ann_meta_data.push({
        "settlement_method": upd_money_data.value.settlement_method,
        "recovery_precision": upd_money_data.value.recovery_precision,
        "knums": upd_money_data.value.knums,
        "unit_price": upd_money_data.value.unit_price
      });
    }
  }
};

const updmodeleditbtn = () => {
  update_supplier_task_data(
    username.value,
    updTableData.value.id,
    updTableData.value.user,
    updTableData.value.pname,
    updTableData.value.send_data_batch,
    updTableData.value.send_data_time,
    updTableData.value.pnums,
    updTableData.value.data_source,
    updTableData.value.scene,
    updTableData.value.send_reason,
    updTableData.value.ann_field_flag,
    updTableData.value.key_frame_extracted_methods,
    updTableData.value.begin_check_data_time,
    updTableData.value.last_check_data_time,
    updTableData.value.get_data_time,
    updTableData.value.ann_meta_data,
    updTableData.value.anno_task_id,
    updTableData.value.wb_name,
    username.value
    ).then((res: any) => {
      if (res.code == 0) {
        updmodel.value = false;
        public_elmsg_success(res.data);
        get_all_data();
      }
      else { public_elmsg_warning(res.data); }
    }).catch((err) => { console.log(err) })
};
// cancle
const updmodelcalbtn = () => {
  updmodel.value = false;
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
      delete_supplier_task_data(row.id, username.value).then((res: any) => {
        if (res.code == 0) {
          public_elmsg_success(res.data);
          get_all_data();
        }
        else {
          public_elmsg_warning(res.data);
        }
      }).catch((err) => { console.log(err) });

    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消删除`); })
}

const reset = () => {
  searchData.value = { "pname": "", "supplier": "", "send_begin_time": "", "send_last_time": "", "pay_begin_time": "", "pay_last_time": "" };
  send_datarear.value = [now_date.getFullYear() + "-01-01", now_now_date];
  pay_datarear.value = null;
  get_all_data();
}


const export_table_data = () => {
  get_all_supplier_task_data(searchData.value.pname, searchData.value.supplier, searchData.value.send_begin_time, searchData.value.send_last_time, searchData.value.pay_begin_time, searchData.value.pay_last_time).then((res: any) => {
    const data = XLSX.utils.json_to_sheet(res.source)//此处tableData.value为表格的数据
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, data, 'supplier')//test-data为自定义的sheet表名
    XLSX.writeFile(wb, 'supplier.xlsx')//test.xlsx为自定义的文件名
  }).catch((err) => { console.log(err) });
}
</script>

<style scoped>
.tools-div {
  display: flex;
}

.updataform {
  width: 100%;
}

.updtable1 {
  width: 100%;
  height: 300px;
  border-collapse: collapse;
}

.updtable1 tr:not(:last-child) {
  border-bottom: 1px solid #353434;
}

.upd-dialog-tab-div {
  width: 100%;
  height: 370px;
  overflow-y: auto;
  margin-top: 20px;
}
</style>