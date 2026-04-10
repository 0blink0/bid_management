<template>
  <div class="file-uploader">
    <n-upload
      ref="uploadRef"
      :multiple="multiple"
      :max="maxFiles"
      :accept="accept"
      :custom-request="handleCustomRequest"
      :show-file-list="false"
      @before-upload="handleBeforeUpload"
    >
      <div class="upload-zone" :class="{ dragover: isDragover }">
        <div class="upload-icon">
          <n-icon :size="48" color="#999">
            <CloudUploadOutline />
          </n-icon>
        </div>
        <div class="upload-text">
          <span v-if="isDragover">释放文件开始上传</span>
          <span v-else>拖拽文件到此处，或 <em>点击选择文件</em></span>
        </div>
        <div class="upload-hint">
          支持 {{ acceptedTypes }}，单个文件不超过 {{ formatSize(maxSize) }}
        </div>
      </div>
    </n-upload>

    <!-- 上传队列 -->
    <div v-if="fileList.length > 0" class="file-list">
      <div
        v-for="file in fileList"
        :key="file.id"
        class="file-item"
        :class="`status-${file.status}`"
      >
        <div class="file-icon">
          <n-icon size="24" :color="getFileColor(file.type)">
            <component :is="getFileIcon(file.type)" />
          </n-icon>
        </div>
        <div class="file-info">
          <div class="file-name">{{ file.name }}</div>
          <div class="file-meta">
            <span>{{ formatSize(file.size) }}</span>
            <span v-if="file.status === 'parsing'">解析中...</span>
            <span v-else-if="file.status === 'completed'">识别率 {{ file.accuracy }}%</span>
            <span v-else-if="file.status === 'error'">{{ file.error }}</span>
          </div>
          <n-progress
            v-if="file.status === 'uploading' || file.status === 'parsing'"
            type="line"
            :percentage="file.progress"
            :indicator-placement="'inside'"
            :status="file.status === 'error' ? 'exception' : 'active'"
          />
        </div>
        <div class="file-actions">
          <n-button
            v-if="file.status === 'completed'"
            size="small"
            quaternary
            @click="handlePreview(file)"
          >
            预览
          </n-button>
          <n-button
            v-if="file.status !== 'uploading' && file.status !== 'parsing'"
            size="small"
            quaternary
            type="error"
            @click="handleRemove(file)"
          >
            删除
          </n-button>
        </div>
      </div>
    </div>

    <!-- 预览弹窗 -->
    <n-modal v-model:show="showPreview" preset="card" :title="previewFile?.name" style="width: 80%">
      <div class="preview-content" v-html="previewContent"></div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  CloudUploadOutline,
  DocumentOutline,
  ImageOutline,
  FilmOutline
} from '@vicons/ionicons5'
import type { UploadFile, UploadInst } from 'naive-ui'
import type { UploadedFile } from '@/types/file'

const props = withDefaults(defineProps<{
  multiple?: boolean
  maxFiles?: number
  accept?: string
  maxSize?: number
  types?: string[]
}>(), {
  multiple: true,
  maxFiles: 10,
  accept: '.pdf,.doc,.docx,.jpg,.png',
  maxSize: 500 * 1024 * 1024, // 500MB
  types: () => ['pdf', 'doc', 'docx', 'jpg', 'png', 'zip']
})

const emit = defineEmits<{
  success: [files: UploadedFile[]]
  error: [error: any]
}>()

const uploadRef = ref<UploadInst | null>(null)
const isDragover = ref(false)
const fileList = ref<UploadedFile[]>([])
const showPreview = ref(false)
const previewFile = ref<UploadedFile | null>(null)
const previewContent = ref('')

const acceptedTypes = computed(() => {
  return props.types.map(t => `.${t}`).join(', ')
})

const handleBeforeUpload = (options: any) => {
  const file = options.file
  const ext = file.name.split('.').pop()?.toLowerCase()

  if (!props.types.includes(ext)) {
    window.$message.error(`不支持的文件类型: .${ext}`)
    return false
  }

  if (file.size > props.maxSize) {
    window.$message.error(`文件超过大小限制: ${formatSize(props.maxSize)}`)
    return false
  }

  // 添加到队列
  const uploadedFile: UploadedFile = {
    id: file.id,
    name: file.name,
    size: file.size,
    type: ext || 'unknown',
    status: 'uploading',
    progress: 0
  }
  fileList.value.push(uploadedFile)

  return true
}

const handleCustomRequest = async (options: any) => {
  const { file, onProgress, onFinish, onError } = options
  const uploadedFile = fileList.value.find(f => f.id === file.id)

  try {
    // 模拟上传进度
    const formData = new FormData()
    formData.append('file', file)

    // 实际上传
    const response = await fetch('/api/v1/files/upload', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('Upload failed')

    const result = await response.json()

    // 更新状态为解析中
    if (uploadedFile) {
      uploadedFile.status = 'parsing'
      uploadedFile.fileId = result.file_id
      uploadedFile.progress = 50

      // 模拟解析进度
      const interval = setInterval(() => {
        if (uploadedFile.progress < 95) {
          uploadedFile.progress += 10
        }
      }, 500)

      // 模拟解析完成
      setTimeout(() => {
        clearInterval(interval)
        uploadedFile.status = 'completed'
        uploadedFile.progress = 100
        uploadedFile.accuracy = 96
        onFinish()
      }, 3000)
    }

    emit('success', fileList.value.filter(f => f.status === 'completed'))
  } catch (error) {
    if (uploadedFile) {
      uploadedFile.status = 'error'
      uploadedFile.error = '上传失败'
    }
    onError(error)
    emit('error', error)
  }
}

const handleRemove = (file: UploadedFile) => {
  fileList.value = fileList.value.filter(f => f.id !== file.id)
  fetch(`/api/v1/files/${file.fileId}`, { method: 'DELETE' })
}

const handlePreview = async (file: UploadedFile) => {
  previewFile.value = file
  showPreview.value = true
  // 实际应该调用API获取预览内容
  previewContent.value = '<p>文档预览内容...</p>'
}

const formatSize = (bytes: number) => {
  if (bytes < 1024) return bytes + 'B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
  return (bytes / (1024 * 1024)).toFixed(1) + 'MB'
}

const getFileIcon = (type: string) => {
  if (['jpg', 'png', 'gif'].includes(type)) return ImageOutline
  if (['mp4', 'avi', 'mov'].includes(type)) return FilmOutline
  return DocumentOutline
}

const getFileColor = (type: string) => {
  if (['jpg', 'png', 'gif'].includes(type)) return '#1890ff'
  if (['pdf'].includes(type)) return '#ff4d4f'
  return '#52c41a'
}
</script>

<style scoped lang="scss">
.file-uploader {
  width: 100%;
}

.upload-zone {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;

  &:hover, &.dragover {
    border-color: #1890ff;
    background: #f0f7ff;
  }

  .upload-icon {
    margin-bottom: 16px;
  }

  .upload-text {
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;

    em {
      color: #1890ff;
      font-style: normal;
    }
  }

  .upload-hint {
    font-size: 12px;
    color: #999;
  }
}

.file-list {
  margin-top: 16px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #fafafa;
  border-radius: 4px;
  margin-bottom: 8px;

  &.status-error {
    background: #fff2f0;
  }
}

.file-info {
  flex: 1;
  min-width: 0;

  .file-name {
    font-weight: 500;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .file-meta {
    font-size: 12px;
    color: #999;
    display: flex;
    gap: 8px;
  }
}

.preview-content {
  max-height: 600px;
  overflow-y: auto;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 4px;
}
</style>
