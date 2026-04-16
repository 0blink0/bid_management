<template>
  <div class="upload-page">
    <n-card title="文件上传">
      <n-space vertical>
        <n-upload
          multiple
          :max="10"
          action="/api/v1/files/upload"
          :headers="authHeaders"
          @before-upload="beforeUpload"
        >
          <n-button>选择文件</n-button>
        </n-upload>

        <n-space>
          <n-tag type="info">支持 PDF</n-tag>
          <n-tag type="info">Word</n-tag>
          <n-tag type="info">图片</n-tag>
          <n-tag type="info">压缩包</n-tag>
        </n-space>

        <n-divider />

        <n-space vertical>
          <n-text strong>上传进度</n-text>
          <n-list v-if="uploadingFiles.length > 0">
            <n-list-item v-for="file in uploadingFiles" :key="file.name">
              <n-space justify="space-between">
                <n-text>{{ file.name }}</n-text>
                <n-progress
                  type="line"
                  :percentage="file.percentage"
                  :indicator-placement="'inside'"
                />
              </n-space>
            </n-list-item>
          </n-list>
          <n-empty v-else description="暂无上传任务" />
        </n-space>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

interface UploadingFile {
  name: string
  percentage: number
}

const userStore = useUserStore()

const authHeaders = computed(() => {
  if (!userStore.token) return {}
  return { Authorization: `Bearer ${userStore.token}` }
})

const uploadingFiles = ref<UploadingFile[]>([])

const beforeUpload = (options: any) => {
  uploadingFiles.value.push({
    name: options.file.name,
    percentage: 0
  })
  return true
}
</script>

<style scoped>
.upload-page {
  padding: 24px;
}
</style>
