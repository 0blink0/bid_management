<template>
  <div class="knowledge-tabs">
    <n-tabs
      :value="activeTab"
      type="line"
      @update:value="handleTabChange"
    >
      <n-tab-pane name="regulations">
        <template #tab>
          <div class="tab-label">
            <n-icon><document-text-outline /></n-icon>
            <span>法规库</span>
          </div>
        </template>
      </n-tab-pane>

      <n-tab-pane name="rules">
        <template #tab>
          <div class="tab-label">
            <n-icon><shield-check-outline /></n-icon>
            <span>规则库</span>
          </div>
        </template>
      </n-tab-pane>

      <n-tab-pane name="sensitive-words">
        <template #tab>
          <div class="tab-label">
            <n-icon><warning-outline /></n-icon>
            <span>错敏词库</span>
          </div>
        </template>
      </n-tab-pane>

      <n-tab-pane name="templates">
        <template #tab>
          <div class="tab-label">
            <n-icon><copy-outline /></n-icon>
            <span>模板库</span>
          </div>
        </template>
      </n-tab-pane>

      <n-tab-pane name="cases">
        <template #tab>
          <div class="tab-label">
            <n-icon><folder-outline /></n-icon>
            <span>案例库</span>
          </div>
        </template>
      </n-tab-pane>

      <n-tab-pane name="activation">
        <template #tab>
          <div class="tab-label">
            <n-icon><play-circle-outline /></n-icon>
            <span>规则生效</span>
          </div>
        </template>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup lang="ts">
import { NTabs, NTabPane, NIcon } from 'naive-ui'
import {
  DocumentTextOutline,
  ShieldCheckOutline,
  WarningOutline,
  CopyOutline,
  FolderOutline,
  PlayCircleOutline
} from '@vicons/ionicons5'

export type KnowledgeTabName =
  | 'regulations'
  | 'rules'
  | 'sensitive-words'
  | 'templates'
  | 'cases'
  | 'activation'

const props = defineProps<{
  activeTab: KnowledgeTabName
}>()

const emit = defineEmits<{
  (e: 'tab-change', tab: KnowledgeTabName): void
}>()

const handleTabChange = (tab: KnowledgeTabName) => {
  emit('tab-change', tab)
}
</script>

<style scoped lang="scss">
.knowledge-tabs {
  background-color: #fff;
  border-radius: var(--radius-lg);
  padding: 0 16px;

  :deep(.n-tabs-nav) {
    padding: 0;
  }

  :deep(.n-tab-pane) {
    padding: 16px 0 0 0;
  }

  .tab-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;

    .n-icon {
      font-size: 18px;
    }
  }
}
</style>
