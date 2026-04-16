<template>
  <AppLayout>
    <div class="workspace-new-page">
      <PageHeader
        title="新建审查任务"
        subtitle="上传招标文件和投标文件，开启智能审查"
        back-link="/home"
      />

      <div class="workspace-content">
        <!-- Step 1: File Upload -->
        <div class="step-card">
          <div class="step-header step-header-blue">
            <div class="step-icon">
              <n-icon :size="24"><CloudUploadOutline /></n-icon>
            </div>
            <div class="step-info">
              <h3>第一步：上传文件</h3>
              <p>上传 PDF、图片等格式文件，支持拖拽上传，单个文件最大 500MB</p>
            </div>
          </div>

          <div
            class="upload-zone"
            :class="{ 'dragover': isDragover }"
            @dragover.prevent="isDragover = true"
            @dragleave="isDragover = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.png,.jpg,.jpeg"
              hidden
              @change="handleFileSelect"
            />
            <div class="upload-content">
              <n-icon :size="48" color="#8c8c8c"><CloudUploadOutline /></n-icon>
              <p class="upload-text">点击或拖拽文件到此区域上传</p>
              <p class="upload-hint">支持 PDF、PNG、JPG 格式</p>
            </div>
          </div>

          <div v-if="files.length > 0" class="file-list">
            <FileCard
              v-for="(file, index) in files"
              :key="index"
              :file-name="file.name"
              :file-size="file.size"
              :file-category="file.category"
              @remove="removeFile(index)"
              @category-change="(cat) => setFileCategory(index, cat)"
            />
          </div>
        </div>

        <!-- Step 2: AI Recognition -->
        <div class="step-card">
          <div class="step-header step-header-purple">
            <div class="step-icon">
              <n-icon :size="24"><BulbOutline /></n-icon>
            </div>
            <div class="step-info">
              <h3>第二步：AI 智能识别</h3>
              <p>上传文件后自动识别文件类型和内容</p>
            </div>
          </div>

          <div v-if="files.length > 0" class="recognition-result">
            <n-grid :cols="3" :x-gap="16" :y-gap="16">
              <n-gi>
                <div class="stat-item">
                  <span class="stat-value">{{ files.length }}</span>
                  <span class="stat-label">总数量</span>
                </div>
              </n-gi>
              <n-gi>
                <div class="stat-item">
                  <span class="stat-value">{{ biddingCount }}</span>
                  <span class="stat-label">招标文件</span>
                </div>
              </n-gi>
              <n-gi>
                <div class="stat-item">
                  <span class="stat-value">{{ tenderCount }}</span>
                  <span class="stat-label">投标文件</span>
                </div>
              </n-gi>
            </n-grid>
          </div>

          <div v-else class="empty-state">
            <n-icon :size="48" color="#d9d9d9"><BulbOutline /></n-icon>
            <p>上传文件后自动识别</p>
          </div>
        </div>

        <!-- Step 3: Review Configuration -->
        <div class="step-card">
          <div class="step-header step-header-orange">
            <div class="step-icon">
              <n-icon :size="24"><SettingsOutline /></n-icon>
            </div>
            <div class="step-info">
              <h3>第三步：审查配置</h3>
              <p>选择需要执行的审查项目</p>
            </div>
          </div>

          <div class="config-grid">
            <div
              v-for="item in reviewOptions"
              :key="item.key"
              class="config-item"
              :class="{ active: selectedReviews.includes(item.key) }"
              @click="toggleReview(item.key)"
            >
              <div class="config-checkbox">
                <div class="checkbox-inner"></div>
              </div>
              <div class="config-info">
                <span class="config-title">{{ item.title }}</span>
                <span class="config-desc">{{ item.desc }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <n-button @click="goHome">返回首页</n-button>
          <n-button
            type="primary"
            :disabled="files.length === 0"
            @click="startReview"
          >
            开始审查
          </n-button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { NIcon, NButton, NGrid, NGi } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import FileCard from '@/components/common/FileCard.vue'
import {
  CloudUploadOutline,
  BulbOutline,
  SettingsOutline
} from '@vicons/ionicons5'

const router = useRouter()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragover = ref(false)
const files = ref<Array<{
  name: string
  size: number
  category?: string
}>>([])

const reviewOptions = [
  { key: 'bidding', title: '招标文件检测', desc: '错敏词、合规性、条款完整性检查' },
  { key: 'collusion', title: '围串标检测', desc: '投标文件雷同性、关联关系分析' },
  { key: 'qualification', title: '资质核验', desc: '企业资质、证书有效期核验' },
  { key: 'comparison', title: '响应比对', desc: '招标文件与投标文件响应性比对' }
]

const selectedReviews = ref<string[]>(['bidding', 'collusion', 'qualification', 'comparison'])

const biddingCount = computed(() => files.value.filter(f => f.category === '招标文件').length)
const tenderCount = computed(() => files.value.filter(f => f.category === '投标文件').length)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files) {
    addFiles(Array.from(target.files))
  }
}

const handleDrop = (e: DragEvent) => {
  isDragover.value = false
  if (e.dataTransfer?.files) {
    addFiles(Array.from(e.dataTransfer.files))
  }
}

const addFiles = (newFiles: File[]) => {
  newFiles.forEach(file => {
    const isBidding = file.name.includes('招标')
    files.value.push({
      name: file.name,
      size: file.size,
      category: isBidding ? '招标文件' : '投标文件'
    })
  })
}

const removeFile = (index: number) => {
  files.value.splice(index, 1)
}

const setFileCategory = (index: number, category: string) => {
  files.value[index].category = category
}

const toggleReview = (key: string) => {
  const index = selectedReviews.value.indexOf(key)
  if (index > -1) {
    selectedReviews.value.splice(index, 1)
  } else {
    selectedReviews.value.push(key)
  }
}

const goHome = () => {
  router.push('/home')
}

const startReview = () => {
  sessionStorage.setItem('reviewConfig', JSON.stringify({
    files: files.value,
    reviews: selectedReviews.value
  }))
  router.push('/workspace/progress')
}
</script>

<style scoped lang="scss">
.workspace-new-page {
  max-width: 720px;
  margin: 0 auto;
}

.workspace-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.step-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.step-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  color: #fff;
}

.step-header-blue {
  background: linear-gradient(135deg, #1E5AA8, #2C7BE5);
}

.step-header-purple {
  background: linear-gradient(135deg, #722ed1, #8b5cf6);
}

.step-header-orange {
  background: linear-gradient(135deg, #d97706, #f59e0b);
}

.step-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-info {
  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }

  p {
    margin: 4px 0 0;
    font-size: 13px;
    opacity: 0.9;
  }
}

.upload-zone {
  margin: 24px;
  padding: 48px;
  border: 2px dashed var(--gray-300);
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover,
  &.dragover {
    border-color: var(--primary-color);
    background-color: var(--primary-bg);
  }
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.upload-text {
  margin: 0;
  font-size: 14px;
  color: var(--gray-700);
}

.upload-hint {
  margin: 0;
  font-size: 12px;
  color: var(--gray-500);
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 24px 24px;
}

.recognition-result {
  padding: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--gray-800);
}

.stat-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 4px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 48px;
  color: var(--gray-500);

  p {
    margin: 0;
    font-size: 14px;
  }
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 24px;
}

.config-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--primary-color);
  }

  &.active {
    border-color: var(--primary-color);
    background-color: var(--primary-bg);

    .config-checkbox .checkbox-inner {
      background-color: var(--primary-color);
      border-color: var(--primary-color);
    }
  }
}

.config-checkbox {
  flex-shrink: 0;
}

.checkbox-inner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--gray-400);
  border-radius: 50%;
  transition: all 0.2s;
}

.config-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.config-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
}

.config-desc {
  font-size: 12px;
  color: var(--gray-500);
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
