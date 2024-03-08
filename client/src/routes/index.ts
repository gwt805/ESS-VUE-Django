import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";
import login from "@/components/auth/login.vue";
// import regist from "@/components/auth/regist.vue";
import admin_auth from "@/components/admin/auth.vue";
import admin_project from "@/components/admin/project.vue";
import admin_supplier from "@/components/admin/supplier.vue";
import index from "@/components/index.vue";
import anno_team_show from "@/components/annoteam/show.vue";
import anno_team_report from "@/components/annoteam/report.vue";
import anno_team_performance from "@/components/annoteam/performance.vue";
import anno_team_efficiency from "@/components/annoteam/efficiency.vue";
import anno_team_task_kind from "@/components/annoteam/taskkind.vue";
import supplier_show from "@/components/supplier/show.vue";
import supplier_report from "@/components/supplier/report.vue";
import supplier_bugdet from "@/components/supplier/budget.vue";
import supplier_ybudget from "@/components/supplier/ybudget.vue";
import snorlax_vs_ess_proname from "@/components/snorlax_vs_ess/proname.vue";
import snorlax_vs_ess_vender from "@/components/snorlax_vs_ess/vender.vue";
import cronjob from "@/components/cronjob/cronjob.vue";
import empty from "@/components/empty/empty.vue";
import updateinfo from "@/components/updateinfo/updateinfo.vue";
import { public_elmsg_warning } from "@/utils/elmsg/index";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: login,
  },
  // {
  //   path: "/regist",
  //   name: "Regist",
  //   component: regist,
  // },
  {
    path: "/index",
    component: index,
    children: [
      {
        path: "",
        redirect: "/index/anno-team-data",
      },
      {
        path: "anno-team-data",
        children: [
          {
            path: "",
            name: "anno_team_show",
            component: anno_team_show,
          },
          {
            path: "report",
            name: "anno_team_report",
            component: anno_team_report,
          },
          {
            path: "efficiency",
            name: "anno_team_efficiency",
            component: anno_team_efficiency,
          },
          {
            path: "performance",
            name: "anno_team_performance",
            component: anno_team_performance,
          },
        ],
      },
      {
        path: "supplier-data",
        children: [
          {
            path: "",
            name: "supplier_show",
            component: supplier_show,
          },
          {
            path: "report",
            name: "supplier_report",
            component: supplier_report,
          },
          {
            path: "bugdet",
            name: "supplier_bugdet",
            component: supplier_bugdet,
          },
          {
            path: "cronjob",
            name: "cronjob",
            component: cronjob,
            meta: { roles: "1" }
          }
        ]
      },
      {
        path: "dashboard-admin",
        children: [
          {
            path: "",
            redirect: {name: "admin_auth"}
          },
          {
            path: "user",
            name: "admin_auth",
            component: admin_auth,
            meta: { roles: "1" }
          },
          {
            path: "project",
            name: "admin_project",
            component: admin_project,
            meta: { roles: "1" }
          },
          {
            path: "supplier",
            name: "admin_supplier",
            component: admin_supplier,
            meta: { roles: "1" }
          },
          {
            path: "taskkind",
            name: "admin_taskkind",
            component: anno_team_task_kind,
            meta: { roles: "1" }
          },
          {
            path: "ybudget",
            name: "supplier_ybudget",
            component: supplier_ybudget,
          },
          {
            path: "snorlax_vs_ess_proname",
            name: "snorlax_vs_ess_proname",
            component: snorlax_vs_ess_proname
          },
          {
            path: "snorlax_vs_ess_vender",
            name: "snorlax_vs_ess_vender",
            component: snorlax_vs_ess_vender
          }
        ]
      },
      {
        path: "updateinfo",
        name: "updateInfo",
        component: updateinfo,
      },
    ],
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: empty },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(from);
  const userRole = window.localStorage.getItem("level");
  if (to.meta.roles) {
    if (to.meta.roles == userRole) { next(); }
    else {
      public_elmsg_warning("您没有权限访问该页面 !");
      next({name: "anno_team_show"});
    }
  }
  else { next(); }
});

export default router;
