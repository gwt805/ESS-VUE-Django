import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";
import router from "@/routes/index";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import disableDevtool from'disable-devtool';

// https://github.com/theajack/disable-devtool/blob/master/README.cn.md
disableDevtool({url: "https://www.baidu.com/",  timeOutUrl: "https://www.baidu.com/"});

const app = createApp(App);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(ElementPlus, { locale: zhCn });
app.use(router);
app.mount("#app");
