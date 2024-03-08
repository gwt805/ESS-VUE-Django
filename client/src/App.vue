<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey === true || event.metaKey === true) && (event.which === 61 || event.which === 107 || event.which === 173 || event.which === 109 || event.which === 187 || event.which === 189)) {
    event.preventDefault();
  }
}, false);

document.addEventListener('mousewheel', (e: any) => {
  if ((e.wheelDelta && e.ctrlKey) || e.detail) {
    e.preventDefault();
  }
}, {
  capture: false,
  passive: false
});
</script>