<template>
    <el-container>
      <el-header><top /></el-header>
      <el-container>
        <el-aside width="200px" class="left"><left /></el-aside>
        <el-container>
          <el-main class="main"><router-view></router-view></el-main>
        </el-container>
      </el-container>
    </el-container>
</template>

<script setup lang="ts">
import top from './nvgmenu/top.vue';
import left from './nvgmenu/left.vue';
</script>

<style scoped>
.left {
  height: 100%;
  position: fixed;
  top: 60px;
  overflow: auto;
  z-index: -1;
}

.main {
  position: absolute;
  left: 200px;
  top: 60px;
}
</style>