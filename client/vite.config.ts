import path from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { webUpdateNotice } from "@plugin-web-update-notification/vite";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/",
  plugins: [
    vue(),
    webUpdateNotice({
      versionType: "build_timestamp",
      logVersion: true,
      locale: "zh_CN",
      notificationProps: {
        title: '📢 系统更新',
        description: '系统更新啦, 请刷新页面',
        buttonText: '刷新',
        dismissButtonText: '忽略'
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    open: false,
  },
});
