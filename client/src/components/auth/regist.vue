<template>
    <div class="login-box" id="demo">
        <div class="input-content">
            <div class="login_tit">
                <div>
                    <i class="tit-bg left"></i>
                    Everyday · 效率系统
                    <i class="tit-bg right"></i>
                </div>
                <p>ESS&nbsp;&nbsp;&nbsp;&nbsp;Everyday</p>
            </div>
            <p class="p user_icon">
                <input type="text" placeholder="账号" autocomplete="off" class="login_txtbx" id="user" v-model="username"
                    @change="diff">
            </p>
            <p class="p user_icon">
                <input type="text" placeholder="姓名" autocomplete="off" class="login_txtbx" id="zhuser" v-model="zhuname"
                    @change="diff">
            </p>
            <p class="p email_icon">
                <input type="email" placeholder="邮箱" autocomplete="off" class="login_txtbx" id="email" v-model="email"
                    @change="diff">
            </p>
            <p class="p pwd_icon">
                <input type="password" placeholder="密码" autocomplete="off" class="login_txtbx" id="pwd" v-model="password"
                    @change="diff">
            </p>
            <p class="p pwd_icon">
                <input type="password" placeholder="确认密码" autocomplete="off" class="login_txtbx" id="pwd2"
                    v-model="password1" @change="diff">
            </p>
            <div class="signup">
                <a class="gv" @click="userregist">注&nbsp;&nbsp;册</a>
                <a class="gv" href="/">返&nbsp;&nbsp;回</a>
            </div>
        </div>
        <div class="canvaszz"> </div>
        <canvas id="canvas"></canvas>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import '@/assets/js/login_canvas.js';
import { regist } from '@/api/auth';
import { public_elmsg_warning } from "@/utils/elmsg/index";

document.title = "注册";

const username = ref("");
const zhuname = ref("");
const email = ref("");
const password = ref("");
const password1 = ref("");
const registflag = ref(false);

const diff = () => {
    let reg = /[\u4e00-\u9fa5]+/g;
    let reg_name = reg.exec(zhuname.value.trim());
    let reg_email = /^[a-zA-Z0-9]+([-_.][A-Za-zd]+)*@gs-robot.com$/;
    let reg_email_res = reg_email.test(email.value.trim());

    if (username.value.trim() == "" || password.value.trim() == "" || zhuname.value.trim() == "" || email.value.trim() == "" || password1.value.trim() == "") {
        public_elmsg_warning("不允许有空值喔 !");
        registflag.value = false;
    }
    else if (reg_name == null || reg_name[0].length != zhuname.value.trim().length) {
        public_elmsg_warning("姓名需要写自己中文名字喔 !");
        registflag.value = false;
    }
    else if (reg_email_res == false) {
        public_elmsg_warning("请填写正确的公司邮箱 !");
        registflag.value = false;
    }
    else if (password.value.trim() != password1.value.trim()) {
        public_elmsg_warning("两次密码输入不一致喔 !");
        registflag.value = false;
    }
    else {
        registflag.value = true;
    }
};

const userregist = () => {
    if (registflag.value) {
        regist(username.value.trim(), zhuname.value.trim(), email.value.trim(), password.value.trim()).then((res: any) => {
            if (res.code == 0) {
                window.location.href = "/";
            }
            else{ public_elmsg_warning(res.data); }
        }).catch((err: any) => { console.log(err) })
    }
    else {
        diff();
    }
};
document.onkeydown = (e) => {
  if (e.code == "Enter") {
    userregist();
  }
}
</script>

<style scoped>
@import url('@/assets/css/login.css');
</style>