<template>
  <div class="page-header">
    <div class="page-header-main">
      <div v-if="backLink" class="back-link" @click="handleBack">
        <n-icon><ChevronBack /></n-icon>
        <span>返回</span>
      </div>
      <div class="page-title-section">
        <h1 class="page-title">{{ title }}</h1>
        <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
      </div>
    </div>
    <div v-if="$slots.actions" class="page-header-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { NIcon } from 'naive-ui'
import { ChevronBack } from '@vicons/ionicons5'

defineProps<{
  title: string
  subtitle?: string
  backLink?: string
}>()

const router = useRouter()

const handleBack = () => {
  if (router.currentRoute.value.meta?.backPath) {
    router.push(router.currentRoute.value.meta.backPath as string)
  } else {
    router.back()
  }
}
</script>

<style scoped lang="scss">
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.page-header-main {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  color: var(--gray-600);
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background-color: var(--gray-100);
    color: var(--primary-color);
  }
}

.page-title-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--gray-800);
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  color: var(--gray-500);
}

.page-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
