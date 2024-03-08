<template>
    <el-dialog v-model="essaboutmodel" title="ESS-INFO" center :before-close="dialog_before_close" style="width: 550px;">
        <p>ESS 是一款统计性的功能平台</p>
        <p>主要有记录个人平时的工作内容，工作量，工作效率，绩效等</p>
        <p>也可以统计给供应商发送的数据量，各供应商在每个项目上所用的费用等</p>
        <p><strong>Copyright © gwt 2023.08</strong></p>
    </el-dialog>
    <el-dialog v-model="changepwdmodel" title="修改密码" center :close-on-click-modal="false" :close-on-press-escape="false" :before-close="dialog_before_close" style="width: 450px;">
        <el-form label-position="left" label-width="70px" :model="pwddict">
            <el-form-item label="新密码">
                <el-input v-model="pwddict.pwd1" />
            </el-form-item>
            <el-form-item label="确认密码">
                <el-input v-model="pwddict.pwd2" />
            </el-form-item>
            <p class="perrmsg" v-if="pwdflag">{{ pwderrmsg }}</p>
            <el-button type="primary" class="btn-updpwd" @click="changepwd">修改</el-button>
        </el-form>
    </el-dialog>
    <el-dialog v-model="selfinfomodel" title="个人信息" center :close-on-click-modal="false" :close-on-press-escape="false" :before-close="selfinfo_dialog_before_close" style="width: 550px;">
        <el-form label-position="left" label-width="50px" :model="pwddict" style="max-width: 550px">
            <div class="avatar-div">
                <el-image class="tx" :src="info_avatar" :zoom-rate="1.2" :preview-src-list="info_avatar_url_list" :max-scale="7" :min-scale="0.2" :initial-index="4" fit="cover" draggable="false"/>
            </div>
            <el-form-item label="头像">
                <el-input v-model="info_avatar" :disabled="roothiden"/>
            </el-form-item>
            <el-form-item label="账号">
                <el-input v-model="info_username" disabled />
            </el-form-item>
            <el-form-item label="姓名">
                <el-input v-model="info_zhuname" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
                <el-input v-model="info_email" disabled />
            </el-form-item>
            <el-form-item label="部门">
                <el-input v-model="info_group" disabled />
            </el-form-item>
            <p class="perrmsg" v-if="pwdflag">{{ pwderrmsg }}</p>
            <el-button type="primary" class="btn-updpwd" @click="updselfinfo" :disabled="roothiden">修改</el-button>
        </el-form>
    </el-dialog>
    <el-menu class="el-menu-demo top" mode="horizontal" :ellipsis="false">
        <el-menu-item class="slc"><img src="/src/assets/imgs/favicon.ico" alt="ESS" srcset=""></el-menu-item>
        <div class="flex-grow" />
        <el-switch class="theme" v-model="value1" :active-action-icon="Moon" inline-prompt :inactive-action-icon="Sunny" active-text="黑" inactive-text="白" @change="themeswitch" />
        <el-menu-item index="1" class="slc" @click="help">Help</el-menu-item>
        <el-sub-menu index="2" class="slc">
            <template #title><el-avatar class="avatar" size="small" :src="info_avatar" />{{ zhuname }}</template>
            <el-menu-item class="slc" @click="aboutck">关于我</el-menu-item>
            <el-menu-item class="slc" @click="selfinfo">个人信息</el-menu-item>
            <el-menu-item class="slc" @click="changepwdck" v-if="!roothiden">修改密码</el-menu-item>
            <el-menu-item class="slc" @click="loginout">退出登录</el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from "vue";
import { Sunny, Moon } from '@element-plus/icons-vue';
import { updatepwd, updateuserimg, get_user_info } from "@/api/auth";
import { public_elmsg_warning } from "@/utils/elmsg/index";


const value1 = ref(true);
const essaboutmodel = ref(false);
const changepwdmodel = ref(false);
const selfinfomodel = ref(false);
const zhuname = ref(window.localStorage.getItem("zhuname"));
const roothiden:any = ref(window.localStorage.getItem("level") == "3" ? true : false);
const info_username: any = ref(window.localStorage.getItem("username"));
const info_zhuname = ref(window.localStorage.getItem("zhuname"));
const info_email = ref(window.localStorage.getItem("email"));
const info_group = ref(window.localStorage.getItem("group"));
const info_avatar: any = ref(window.localStorage.getItem("imgurl") == "null" ? "https://img1.baidu.com/it/u=1285375996,3783960243&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500" : window.localStorage.getItem("imgurl"));
const info_avatar_url_list:any = ref([info_avatar.value]);
const intval:any = ref(null);

watch(info_avatar, (newval, oldval) => {
    console.log(oldval);
    info_avatar_url_list.value = [newval];
});
const pwddict = ref({ "pwd1": "", "pwd2": "" });
const pwdflag = ref(false);
const pwderrmsg = ref("两个密码不相等");

const add_main_body_div_layout_z_index = () => {
    const div_layout:any = document.getElementById("layout");
    div_layout.style.zIndex = "-1";
};

const themeswitch = (flag: boolean) => {
    if (flag) { document.getElementsByTagName("html")[0].classList.add("dark"); }
    else { document.getElementsByTagName("html")[0].classList.remove("dark"); }
};

const help = () => { public_elmsg_warning("请联系卫龙~"); }

const aboutck = () => {
    essaboutmodel.value = true;
    add_main_body_div_layout_z_index();
}

const selfinfo = () => {
    selfinfomodel.value = true;
    add_main_body_div_layout_z_index();
};

const updselfinfo = () => {
    const imgurl: any = info_avatar.value.trim();
    if (imgurl.length > 1024) { public_elmsg_warning("头像地址不能超过1024"); }
    else {
        updateuserimg(info_username.value, info_avatar.value).then((res: any) => {
            if (res.code == 0) {
                selfinfomodel.value = false;
                window.localStorage.setItem("imgurl", info_avatar.value);
            }
        }).catch((err) => { console.log(err) });
    }
};

const changepwdck = () => {
    changepwdmodel.value = true;
    add_main_body_div_layout_z_index();
}

const changepwd = () => {
    if (pwddict.value.pwd1 == "" || pwddict.value.pwd2 == "") {
        pwdflag.value = true;
        pwderrmsg.value = "不允许有空值!";
    }
    else if (pwddict.value.pwd1 != pwddict.value.pwd2) {
        pwdflag.value = true;
        pwderrmsg.value = "两个密码填写的不一致!";
    }
    else {
        pwdflag.value = false;
        changepwdmodel.value = false;
        const username: any = window.localStorage.getItem("username");
        updatepwd(username, pwddict.value.pwd1).then((res: any) => {
            if (res.code == 0) {
                window.location.href = "/";
                window.localStorage.clear();
            }
        }).catch((err: any) => {
            console.error(err);
        })
    }
}

const loginout = () => {
    window.localStorage.clear();
    window.location.href = "/";
};

const selfinfo_dialog_before_close = (done:any) => {
    const local_imgurl: any = window.localStorage.getItem("imgurl") == "null" ? "https://img1.baidu.com/it/u=1285375996,3783960243&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500" : window.localStorage.getItem("imgurl");
    info_avatar.value = local_imgurl;
    const div_layout:any = document.getElementById("layout");
    div_layout.style.zIndex = "0";
    done();
};

const dialog_before_close = (done:any) => {
    const div_layout:any = document.getElementById("layout");
    div_layout.style.zIndex = "0";
    done();
};

onMounted(()=>{
    intval.value = setInterval(()=> {
        get_user_info(info_username.value).then((res:any)=>{
            zhuname.value = res.zh_uname;
            info_zhuname.value = res.zh_uname;
            info_email.value = res.email;
            info_group.value = res.group;
            
            window.localStorage.setItem("zhuname", res.zh_uname);
            window.localStorage.setItem("email", res.email);
            window.localStorage.setItem("level", res.power);
            window.localStorage.setItem("group", res.group);
            window.localStorage.setItem("imgurl", res.img);

            roothiden.value = window.localStorage.getItem("level") == "3" ? true : false;
        }).catch((err)=>{console.error(err)});
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});

</script>

<style scoped>
.top {
    position: absolute;
    width: 100%;
    height: 60px;
    left: 0;
}
.theme {
    margin: auto;
}
.avatar {
    margin-right: 10px;
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

p {
    text-align: center;
    margin-left: 20px;
    line-height: 30px;
}

p:first-child {
    margin-top: -20px;
}

p:last-child {
    text-align: center;
    margin: 20px 0 -30px 0;
}

.flex-grow {
    flex-grow: 1;
}

img {
    margin-top: 5px;
    padding-bottom: 5px;
    -webkit-user-drag: none;
}

.slc img::before {
    background-color: transparent;
}

.slc {
    user-select: none !important;
}

.perrmsg {
    color: red;
    margin-bottom: 10px;
}

.btn-updpwd {
    width: 100%;
}
</style>