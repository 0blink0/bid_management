<template>
  <div class="file-card">
    <div class="file-icon" :style="{ backgroundColor: iconBgColor }">
      <n-icon :size="24" :color="iconColor">
        <DocumentTextOutline v-if="fileType === 'pdf'" />
        <ImageOutline v-else-if="isImage" />
        <DocumentOutline v-else />
      </n-icon>
    </div>
    <div class="file-info">
      <div class="file-name" :title="fileName">{{ fileName }}</div>
      <div class="file-meta">
        <span class="file-size">{{ formattedSize }}</span>
        <span v-if="fileCategory" class="file-category">{{ fileCategory }}</span>
      </div>
    </div>
    <div class="file-actions">
      <n-dropdown trigger="click" :options="typeOptions" @select="handleTypeChange">
        <n-tag :type="categoryType" size="small">
          {{ fileCategory || '选择类型' }}
          <template #icon>
            <n-icon><ChevronDown /></n-icon>
          </template>
        </n-tag>
      </n-dropdown>
      <n-button quaternary circle size="small" @click="handleRemove">
        <template #icon>
          <n-icon><CloseOutline /></n-icon>
        </template>
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NIcon, NTag, NButton, NDropdown } from 'naive-ui'
import { DocumentTextOutline, DocumentOutline, ImageOutline, CloseOutline, ChevronDown } from '@vicons/ionicons5'

const props = defineProps<{
  fileName: string
  fileSize: number
  fileType?: string
  fileCategory?: string
}>()

const emit = defineEmits<{
  (e: 'remove'): void
  (e: 'categoryChange', category: string): void
}>()

const isImage = computed(() => {
  const ext = props.fileName?.toLowerCase().split('.').pop()
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp'].includes(ext || '')
})

const iconBgColor = computed(() => {
  if (props.fileType === 'pdf') return 'rgba(255, 77, 79, 0.1)'
  if (isImage.value) return 'rgba(82, 196, 26, 0.1)'
  return 'rgba(30, 90, 168, 0.1)'
})

const iconColor = computed(() => {
  if (props.fileType === 'pdf') return '#ff4d4f'
  if (isImage.value) return '#52c41a'
  return '#1E5AA8'
})

const formattedSize = computed(() => {
  const size = props.fileSize
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / (1024 * 1024)).toFixed(1) + ' MB'
})

const categoryType = computed(() => {
  if (props.fileCategory === '招标文件') return 'info'
  if (props.fileCategory === '投标文件') return 'warning'
  return 'default'
})

const typeOptions = [
  { label: '招标文件', key: '招标文件' },
  { label: '投标文件', key: '投标文件' }
]

const handleRemove = () => {
  emit('remove')
}

const handleTypeChange = (key: string) => {
  emit('categoryChange', key)
}
</script>

<style scoped lang="scss">
.file-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  transition: border-color 0.2s;

  &:hover {
    border-color: var(--primary-color);
  }
}

.file-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.file-size {
  font-size: 12px;
  color: var(--gray-500);
}

.file-category {
  font-size: 12px;
  color: var(--gray-500);
}

.file-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
