<template>
    <el-menu :default-active="menu_default_active" :default-openeds="openedMenus" class="el-menu-vertical-demo" :collapse="false" :router="true">
        <el-sub-menu index="1">
            <template #title><el-icon><HomeFilled /></el-icon><span>内部数据</span></template>
            <el-menu-item-group index="/index">
                <template #title><span>GS</span></template>
                <el-menu-item index="/index/anno-team-data" class="gs2"><el-icon><HelpFilled /></el-icon>所有数据</el-menu-item>
                <el-menu-item index="/index/anno-team-data/report" class="gs2"><el-icon><Histogram /></el-icon>图表展示</el-menu-item>
                <el-menu-item index="/index/anno-team-data/efficiency" class="gs2"><el-icon><ChromeFilled /></el-icon>团队效率</el-menu-item>
                <el-menu-item index="/index/anno-team-data/performance" class="gs2"><el-icon><Avatar /></el-icon>个人绩效</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-sub-menu index="2">
            <template #title><el-icon><Share /></el-icon><span>外部数据</span></template>
            <el-menu-item-group index="/index">
                <template #title><span>供应商</span></template>
                <el-menu-item index="/index/supplier-data"><el-icon><HelpFilled /></el-icon>所有数据</el-menu-item>
                <el-sub-menu index="2-2">
                    <template #title><span><el-icon><List /></el-icon>预算详情</span></template>
                    <el-menu-item index="/index/supplier-data/report"><el-icon><Histogram /></el-icon>图表展示</el-menu-item>
                    <el-menu-item index="/index/supplier-data/bugdet"><el-icon><Grid /></el-icon>表格展示</el-menu-item>
                </el-sub-menu>
                <el-menu-item index="/index/supplier-data/cronjob" v-if="!rootdisable"><el-icon><Timer /></el-icon>定时任务</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-sub-menu index="3" v-if="!rootdisable">
            <template #title><el-icon><Menu /></el-icon><span>后台管理</span></template>
            <el-menu-item-group index="/index">
                <template #title><span>管理员</span></template>
                <el-menu-item index="/index/dashboard-admin/user"><el-icon><UserFilled /></el-icon>用户管理</el-menu-item>
                <el-menu-item index="/index/dashboard-admin/project"><el-icon><Memo /></el-icon>项目管理</el-menu-item>
                <el-menu-item index="/index/dashboard-admin/supplier"><el-icon><Briefcase /></el-icon>供应商管理</el-menu-item>
                <el-menu-item index="/index/dashboard-admin/taskkind"><el-icon><Grape /></el-icon>任务类型管理</el-menu-item>
                <el-menu-item index="/index/dashboard-admin/ybudget"><el-icon><Money /></el-icon>项目预算管理</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-sub-menu index="4" v-if="!rootdisable">
            <template #title><el-icon><OfficeBuilding /></el-icon><span>对应关系管理</span></template>
            <el-menu-item-group index="/index">
                <template #title><span>Snorlax vs ESS</span></template>
                <el-menu-item index="/index/dashboard-admin/snorlax_vs_ess_proname"><el-icon><Guide /></el-icon>项目名对应关系</el-menu-item>
                <el-menu-item index="/index/dashboard-admin/snorlax_vs_ess_vender"><el-icon><School /></el-icon>供应商名对应关系</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item index="/index/updateinfo"><el-icon><View /></el-icon><span>更新记录</span></el-menu-item>
    </el-menu>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const intval:any = ref(null);
const openedMenus = ref(["1"]);
const menu_default_active = ref(router.currentRoute.value.fullPath);
const rootdisable = ref(window.localStorage.getItem("level") == "1" ? false : true);

onMounted(()=>{
    intval.value = setInterval(()=> {
        rootdisable.value = window.localStorage.getItem("level") == "1" ? false : true;
    }, 1000);
});

onUnmounted(() => {
    clearInterval(intval.value);
});
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    position: fixed;
    overflow: auto;
}

.el-menu-vertical-demo {
    width: 60px;
    height: 93.6%;
    user-select: none;
    position: fixed;
    overflow: auto;
}

a {
    text-decoration: none;
}

.f1 {
    position: absolute;
    bottom: 0;
    color: rgb(7, 108, 223);
}

#ck {
    visibility: hidden;
}

label {
    position: absolute;
    width: 100%;
    font-size: 30px;
    text-align: center;
}
</style>