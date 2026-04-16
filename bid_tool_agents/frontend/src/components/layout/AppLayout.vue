<template>
  <div class="app-layout">
    <AppTopbar />
    <div class="app-body">
      <AppSidebar />
      <main class="main-wrapper">
        <div class="main-content">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppTopbar from './AppTopbar.vue'
import AppSidebar from './AppSidebar.vue'
</script>

<style scoped lang="scss">
.app-layout {
  width: 100%;
  min-height: 100vh;
}

.app-body {
  display: flex;
}

.main-wrapper {
  flex: 1;
  margin-left: var(--sidebar-width);
  margin-top: var(--topbar-height);
  min-height: calc(100vh - var(--topbar-height));
  background-color: var(--gray-100);
}

.main-content {
  padding: 24px;
  max-width: 1200px;
}
</style>
