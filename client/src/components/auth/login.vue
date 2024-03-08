<template>
  <div class="login-box" id="demo" v-loading="loading" element-loading-text="正在登录请稍后...">
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
        <input type="text" placeholder="用户名/邮箱" autocomplete="off" class="login_txtbx" id="user" v-model="user">
      </p>
      <p class="p user_icon" v-if="is_zhuname">
        <input type="text" placeholder="姓名" autocomplete="off" class="login_txtbx" id="zhuser" v-model="zhuname"
          @change="diff">
      </p>
      <p class="p pwd_icon">
        <input type="password" placeholder="密码" autocomplete="off" class="login_txtbx" id="pwd" v-model="pwd">
      </p>
      <div class="signup">
        <a class="gv" @click="loginfn(false)">登&nbsp;&nbsp;录</a>
        <a class="gv" @click="loginfn(true)">LDAP&nbsp;登录</a>
      </div>
    </div>
    <div class="canvaszz"> </div>
    <canvas id="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import '@/assets/js/login_canvas.js';
import { login } from '@/api/auth';
import router from "@/routes/index";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg/index";

document.title = "登录";

let user = "";
let pwd = "";
const zhuname = ref("");
const loginflag = ref(true);
const is_zhuname = ref(false);
const loading = ref(false);

const diff = () => {
    let reg = /[\u4e00-\u9fa5]+/g;
    let reg_name = reg.exec(zhuname.value.trim());

    if (user.trim() == "" || pwd.trim() == "") {
        if (is_zhuname.value == true) {
          public_elmsg_warning("不允许有空值喔 !");
          loginflag.value = false;
        }
        else {
          public_elmsg_warning("不允许有空值喔 !");
          loginflag.value = false;
        }
    }
    else if (is_zhuname.value == true && (reg_name == null || reg_name[0].length != zhuname.value.trim().length)) {
        public_elmsg_warning("姓名需要写自己中文名字喔 !");
        loginflag.value = false;
    }
    else {
        loginflag.value = true;
    }
};

const loginfn = (is_ldap_login:boolean) => {
  diff();
  if (loginflag.value) {
    loading.value = true;
    login(user.trim(), pwd.trim(), is_ldap_login, zhuname.value.trim()).then((res: any) => {
      loading.value = false;
      if (res.code == 0) {
        const username = res.username;
        const zhuname = res.zhuname;
        const email = res.email;
        const token = res.token;
        const level = res.level;
        const group = res.group;
        const imgurl = res.imgurl;
        window.localStorage.setItem("username", username);
        window.localStorage.setItem("zhuname", zhuname);
        window.localStorage.setItem("email", email);
        window.localStorage.setItem("token", token);
        window.localStorage.setItem("level", level);
        window.localStorage.setItem("group", group);
        window.localStorage.setItem("imgurl", imgurl);
        public_elmsg_success("登录成功 !");

        setTimeout(() => {
          if (router.currentRoute.value.query.redirect) {
            const redirect: any = router.currentRoute.value.query.redirect;
            window.location.href = redirect;
          }
          else {
            window.location.href = "/index";
          }
        }, 2000);
      }
      else {
        if (res?.is_zhuname == "true") {
          is_zhuname.value = true;
        }
        public_elmsg_warning(res.data);
      }
    })
      .catch((err) => {
        console.log(err);
      });
  }
};

// document.onkeydown = (e) => {
//   if (e.code == "Enter") {
//     loginfn();
//   }
// }

if (localStorage.getItem("username") != null && localStorage.getItem("zhuname") != null && localStorage.getItem("email") != null && localStorage.getItem("group") != null && localStorage.getItem("imgurl") != null && localStorage.getItem("token") != null && localStorage.getItem("level") != null) {
  window.location.href = "/index";
}
</script>

<style scoped>
@import url('@/assets/css/login.css');
</style>
