<template>
  <div class="pdf-viewer">
    <div class="viewer-toolbar">
      <div class="toolbar-left">
        <n-button-group size="small">
          <n-button @click="previousPage" :disabled="currentPage <= 1">
            <template #icon>
              <n-icon><ChevronBackOutline /></n-icon>
            </template>
          </n-button>
          <n-button disabled class="page-info">
            {{ currentPage }} / {{ totalPages || '-' }}
          </n-button>
          <n-button @click="nextPage" :disabled="currentPage >= totalPages">
            <template #icon>
              <n-icon><ChevronForwardOutline /></n-icon>
            </template>
          </n-button>
        </n-button-group>
      </div>

      <div class="toolbar-center">
        <n-input
          v-model:value="searchQuery"
          placeholder="搜索..."
          size="small"
          clearable
          @keyup.enter="handleSearch"
          style="width: 200px"
        >
          <template #prefix>
            <n-icon><SearchOutline /></n-icon>
          </template>
        </n-input>
      </div>

      <div class="toolbar-right">
        <n-button-group size="small">
          <n-button @click="zoomOut" :disabled="scale <= 0.5">
            <template #icon>
              <n-icon><RemoveOutline /></n-icon>
            </template>
          </n-button>
          <n-button disabled class="zoom-info">
            {{ Math.round(scale * 100) }}%
          </n-button>
          <n-button @click="zoomIn" :disabled="scale >= 3">
            <template #icon>
              <n-icon><AddOutline /></n-icon>
            </template>
          </n-button>
        </n-button-group>

        <n-divider vertical />

        <n-button-group size="small">
          <n-button @click="rotate -= 90">
            <template #icon>
              <n-icon><RotateLeftOutline /></n-icon>
            </template>
          </n-button>
          <n-button @click="rotate += 90">
            <template #icon>
              <n-icon><RotateRightOutline /></n-icon>
            </template>
          </n-button>
        </n-button-group>

        <n-divider vertical />

        <n-button size="small" @click="downloadPdf">
          <template #icon>
            <n-icon><DownloadOutline /></n-icon>
          </n-button>
        </n-button>
      </div>
    </div>

    <div class="viewer-container" ref="containerRef">
      <div v-if="loading" class="loading-state">
        <n-spin size="large" />
        <p>正在加载 PDF...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <n-icon :size="48" color="#ff4d4f">
          <AlertCircleOutline />
        </n-icon>
        <p>{{ error }}</p>
        <n-button @click="retryLoad">重新加载</n-button>
      </div>

      <div v-else class="pdf-canvas-wrapper" :style="canvasWrapperStyle">
        <canvas ref="canvasRef"></canvas>
      </div>
    </div>

    <div class="viewer-footer" v-if="!loading && !error">
      <div class="page-slider">
        <span class="slider-label">页面</span>
        <n-slider
          v-model:value="currentPage"
          :min="1"
          :max="totalPages || 1"
          :step="1"
          @update:value="goToPage"
        />
      </div>

      <div class="page-thumbnails" v-if="showThumbnails">
        <div
          v-for="page in Math.min(totalPages, 5)"
          :key="page"
          class="thumbnail"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
        >
          {{ page }}
        </div>
        <span v-if="totalPages > 5">...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import {
  NButton,
  NButtonGroup,
  NIcon,
  NInput,
  NSlider,
  NDivider,
  NSpin,
  NAlert
} from 'naive-ui'
import {
  ChevronBackOutline,
  ChevronForwardOutline,
  SearchOutline,
  RemoveOutline,
  AddOutline,
  RotateLeftOutline,
  RotateRightOutline,
  DownloadOutline,
  AlertCircleOutline
} from '@vicons/ionicons5'

const props = withDefaults(defineProps<{
  url: string
  page?: number
  scale?: number
  showThumbnails?: boolean
}>(), {
  page: 1,
  scale: 1,
  showThumbnails: true
})

const emit = defineEmits<{
  'page-change': [page: number]
  load: [info: { totalPages: number }]
  error: [message: string]
}>()

const containerRef = ref<HTMLDivElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)

const currentPage = ref(props.page)
const totalPages = ref(0)
const scale = ref(props.scale)
const rotate = ref(0)
const searchQuery = ref('')
const loading = ref(false)
const error = ref('')

let pdfDoc: any = null
let renderTask: any = null

const canvasWrapperStyle = computed(() => ({
  transform: `rotate(${rotate.value}deg) scale(${scale.value})`,
  transformOrigin: 'center center'
}))

const loadPdf = async () => {
  if (!props.url) {
    error.value = 'PDF URL is required'
    return
  }

  loading.value = true
  error.value = ''

  try {
    if (typeof window !== 'undefined' && 'pdfjsDist' in window) {
      const pdfjsLib = (window as any).pdfjsLib

      const loadingTask = pdfjsLib.getDocument(props.url)
      pdfDoc = await loadingTask.promise

      totalPages.value = pdfDoc.numPages
      emit('load', { totalPages: pdfDoc.numPages })

      await renderPage(currentPage.value)
    } else {
      throw new Error('PDF.js library not loaded. Please include pdfjs-dist in your dependencies.')
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to load PDF'
    emit('error', error.value)
  } finally {
    loading.value = false
  }
}

const renderPage = async (pageNum: number) => {
  if (!pdfDoc || !canvasRef.value) return

  if (renderTask) {
    renderTask.cancel()
  }

  try {
    const page = await pdfDoc.getPage(pageNum)
    const canvas = canvasRef.value
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const viewport = page.getViewport({ scale: scale.value })
    canvas.height = viewport.height
    canvas.width = viewport.width

    renderTask = page.render({
      canvasContext: ctx,
      viewport: viewport
    })

    await renderTask.promise
  } catch (e: any) {
    if (e.name !== 'RenderingCancelledException') {
      console.error('Error rendering page:', e)
    }
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page: number) => {
  currentPage.value = Math.max(1, Math.min(page, totalPages.value))
}

const zoomIn = () => {
  scale.value = Math.min(3, scale.value + 0.25)
}

const zoomOut = () => {
  scale.value = Math.max(0.5, scale.value - 0.25)
}

const handleSearch = () => {
  console.log('Search for:', searchQuery.value)
}

const downloadPdf = () => {
  if (props.url) {
    const link = document.createElement('a')
    link.href = props.url
    link.download = props.url.split('/').pop() || 'document.pdf'
    link.click()
  }
}

const retryLoad = () => {
  loadPdf()
}

watch(currentPage, (newPage) => {
  emit('page-change', newPage)
  renderPage(newPage)
})

watch(scale, () => {
  renderPage(currentPage.value)
})

watch(() => props.url, () => {
  loadPdf()
})

watch(() => props.page, (newPage) => {
  currentPage.value = newPage
})

onMounted(() => {
  loadPdf()
})

onUnmounted(() => {
  if (renderTask) {
    renderTask.cancel()
  }
})
</script>

<style scoped lang="scss">
.pdf-viewer {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: $radius-lg;
  overflow: hidden;
  height: 100%;
}

.viewer-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  background: $gray-100;
  border-bottom: 1px solid $gray-200;
  flex-wrap: wrap;
  gap: $spacing-md;
}

.toolbar-left,
.toolbar-center,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.page-info,
.zoom-info {
  min-width: 70px;
  text-align: center;
  font-size: $font-size-sm;
}

.viewer-container {
  flex: 1;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: $spacing-xl;
  background: $gray-200;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-3xl;
  color: $gray-500;

  p {
    margin: $spacing-md 0;
    font-size: $font-size-sm;
  }
}

.error-state {
  color: $danger-color;
}

.pdf-canvas-wrapper {
  transition: transform $transition-base;
}

canvas {
  box-shadow: $shadow-lg;
  background: #fff;
}

.viewer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  background: $gray-100;
  border-top: 1px solid $gray-200;
}

.page-slider {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  flex: 1;
  max-width: 300px;

  .slider-label {
    font-size: $font-size-sm;
    color: $gray-600;
  }
}

.page-thumbnails {
  display: flex;
  align-items: center;
  gap: $spacing-xs;

  .thumbnail {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    border: 1px solid $gray-300;
    border-radius: $radius-sm;
    font-size: $font-size-xs;
    cursor: pointer;
    transition: all $transition-fast;

    &:hover {
      border-color: $primary-color;
      color: $primary-color;
    }

    &.active {
      background: $primary-color;
      border-color: $primary-color;
      color: #fff;
    }
  }

  span {
    color: $gray-500;
    font-size: $font-size-xs;
  }
}
</style>
