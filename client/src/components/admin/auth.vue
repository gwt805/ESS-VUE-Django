<template>
    <div id="layout">
        <!-- search -->
        <div class="tools-div">
            <div class="m-4">
                <el-input v-model="searchData.emial" clearable @change="get_all_data"><template #append>@gs-robot.com</template></el-input>
            </div>
            <el-button type="primary" :icon="Refresh" @click="reset">重置</el-button>
        </div>
        <!-- update pwd -->
        <el-dialog v-model="updpwdmodel" title="修改密码" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 450px;">
            <el-form label-position="left" label-width="70px" :model="pwddict">
                <el-form-item label="用户名"><el-input v-model="pwddict.username" disabled /></el-form-item>
                <el-form-item label="新密码"><el-input v-model="pwddict.pwd1" :disabled="rootdisable" /></el-form-item>
                <el-form-item label="确认密码"><el-input v-model="pwddict.pwd2" :disabled="rootdisable" /></el-form-item>
                <el-button type="primary" class="btn-updpwd" @click="changepwd" :disabled="rootdisable">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- update info -->
        <el-dialog v-model="updmodel" title="修改用户信息" center :close-on-click-modal="false" :close-on-press-escape="false" style="width: 550px;">
            <el-form label-position="left" label-width="50px" :model="userinfo" style="max-width: 550px">
                <div class="avatar-div">
                    <el-image class="tx" :src="userinfo.img" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2" :initial-index="4" fit="cover" draggable="false"/>
                </div>
                <el-form-item label="账号">
                    <el-input v-model="userinfo.username" disabled />
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="userinfo.zh_uname" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="userinfo.email" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="头像">
                    <el-input v-model="userinfo.img" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="部门">
                    <el-input v-model="userinfo.group" :disabled="rootdisable" />
                </el-form-item>
                <el-form-item label="权限">
                    <el-input type="number" v-model="userinfo.power" :disabled="rootdisable" min="1" max="4" />
                </el-form-item>
                <el-button type="primary" class="btn-updpwd" @click="updsuerinfo" :disabled="rootdisable">修改</el-button>
            </el-form>
        </el-dialog>
        <!-- show -->
        <el-table :data="tableData" :default-sort="{ prop: 'tsdtime', order: 'descending' }" key="id" border highlight-current-row style="width: 100%;" height="800">
            <el-table-column prop="username" label="账号" width="150" />
            <el-table-column prop="zh_uname" label="姓名" width="120" />
            <el-table-column prop="email" label="邮箱" width="250" />
            <el-table-column prop="group" label="部门" width="100" />
            <el-table-column prop="img" label="头像" />
            <el-table-column prop="power" label="权限" width="80">
                <template #default="scope">
                    <el-tag type="success">{{ scope.row.power }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="180px" fixed="right" align="center" v-if="!roothiden">
                <template #default="scope">
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)" :disabled="rootdisable">编辑</el-button>
                    <el-button size="small" type="danger" @click="handlePwd(scope.$index, scope.row)" :disabled="rootdisable">改密</el-button>
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
import { ElMessageBox } from 'element-plus';
import { ref,onMounted, onUnmounted } from "vue";
import { Refresh } from '@element-plus/icons-vue';
import { public_elmsg_warning, public_elmsg_success, public_elmsg_info } from "@/utils/elmsg/index";
import { admin_get_user_info_list, admin_get_user_info, admin_update_user_info, admin_update_user_pwd } from "@/api/admin";

const count = ref(0);
const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);

const small = ref(false);
const background = ref(false);
const disabled = ref(false);

const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);
const username:any = ref(window.localStorage.getItem("zhuname"));
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);
const intval:any = ref(null);

const updmodel = ref(false);
const userinfo = ref({"username": "", "zh_uname": "", "email": "", "group": "", "img": "", "power": ""});

const updpwdmodel = ref(false);
const pwddict = ref({"username": "", "pwd1": "", "pwd2": ""});

const searchData = ref({"emial": ""})

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
    admin_get_user_info_list(currentPage.value, pageSize.value, `${searchData.value.emial}@gs-robot.com`).then((res:any) => {
            if (res.code == 0) {
                tableData.value = res.data;
                count.value = res.count;
            }
            else {
                public_elmsg_warning(res.data);
            }
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
// edit info
const handleEdit = (index: any, row: any) => {
    console.log(index);
    ElMessageBox.confirm(`你确定要修改 ID 为 ${row.username} 的数据吗?`,'UPDATE',{confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning'}).then(() => {
        admin_get_user_info(row.username).then((res: any) => {
            userinfo.value = res.data;
        }).catch((err) => { console.log(err) });
        updmodel.value = true;
    })
    .catch(() => { public_elmsg_info(`ID 为 ${row.id} 的数据 取消修改`); })
}

const updsuerinfo = () => {
    let reg = /[\u4e00-\u9fa5]+/g;
    let reg_name = reg.exec(userinfo.value.zh_uname.trim());
    let reg_email = /^[a-zA-Z0-9]+([-_.][A-Za-zd]+)*@gs-robot.com$/;
    let reg_email_res = reg_email.test(userinfo.value.email.trim());

    if (userinfo.value.zh_uname.trim() == "" || userinfo.value.email.trim() == "" || userinfo.value.power == "") { public_elmsg_warning("不允许有空值喔 !"); }
    else if (reg_name == null || reg_name[0].length != userinfo.value.zh_uname.trim().length) { public_elmsg_warning("姓名需要写自己中文名字喔 !"); }
    else if (reg_email_res == false) { public_elmsg_warning("请填写正确的公司邮箱 !"); }
    else if (userinfo.value.img != null && userinfo.value.img.length > 1024) { public_elmsg_warning("头像地址不能超过 1024 !"); }
    else if (Number(userinfo.value.power) < 1 || Number(userinfo.value.power) > 4) { public_elmsg_warning("权限范围错误( 1 ~ 4 ) !"); }
    else {
        admin_update_user_info(username.value, userinfo.value.username.trim(), userinfo.value.zh_uname.trim(), userinfo.value.email.trim(), userinfo.value.group, userinfo.value.img, userinfo.value.power).then((res:any)=>{
            if (res.code == 0) {
                public_elmsg_success(res.data);
                updmodel.value = false;
                get_all_data();
            }
            else { public_elmsg_warning(res.data); }
        }).catch((err)=>{console.log(err)});
    }
};
// edit pwd
const handlePwd = (index: any, row: any) => {
    console.log(index);
    pwddict.value.username = row.username;
    updpwdmodel.value = true;
};
const changepwd = () => {
    if (pwddict.value.pwd1.trim() == "" || pwddict.value.pwd2.trim() == "") { public_elmsg_warning("不允许有空值 !"); }
    else if (pwddict.value.pwd1.trim() != pwddict.value.pwd2.trim()) { public_elmsg_warning("两个密码填写的不一致 !"); }
    else {
        admin_update_user_pwd(username.value, pwddict.value.username, pwddict.value.pwd1).then((res: any) => {
            if (res.code == 0) {
                updpwdmodel.value = false;
                public_elmsg_success(res.data);
            }
        }).catch((err: any) => {
            console.error(err);
        })
    }
};

const reset = () => {
    searchData.value = {"emial": ""};
    get_all_data();
}
</script>

<style scoped>
.tools-div {
    display: flex;
}
.btn-updpwd {
    width: 100%;
}
.avatar-div {
    height: 100px;
    margin-bottom: 20px;
}

.avatar-div .tx {
    width: 100px;
    height: 100px;
    margin: auto;
    display: block;
    border-radius: 50%;
}
</style>