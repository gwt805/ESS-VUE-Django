import axios from "axios";
import { ElMessage } from 'element-plus';
import router from "@/routes/index";

const http = axios.create({
  baseURL: "http://localhost:8088",
  headers: {
    USERNAME: window.localStorage.getItem("username"),
    AUTHORIZATION: window.localStorage.getItem("token"),
  },
});

http.interceptors.response.use(
  (res) => {
    if (res.data.code == -2) {
      window.localStorage.clear();
      window.location.href = `/login?redirect=${router.currentRoute.value.fullPath}`;
    } else {
      return res.data;
    }
  },
  (error) => {
    ElMessage({
      type: 'error',
      message: "请求错误 , 请检查网络/服务状态 !",
  })
    return Promise.reject(error);
  }
);

export default http;
