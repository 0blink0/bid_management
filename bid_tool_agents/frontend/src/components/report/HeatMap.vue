<template>
  <div class="heatmap-container">
    <div class="heatmap-header">
      <h4>围串标热力图</h4>
      <div class="legend">
        <div class="legend-item">
          <span class="legend-color high"></span>
          <span class="legend-label">高关联 (&gt;{{ threshold }})</span>
        </div>
        <div class="legend-item">
          <span class="legend-color medium"></span>
          <span class="legend-label">中关联 ({{ mediumThreshold }}-{{ threshold }})</span>
        </div>
        <div class="legend-item">
          <span class="legend-color low"></span>
          <span class="legend-label">低关联 (&lt;{{ mediumThreshold }})</span>
        </div>
      </div>
    </div>

    <div class="heatmap-wrapper" ref="wrapperRef">
      <canvas
        ref="canvasRef"
        @mousemove="handleMouseMove"
        @mouseleave="handleMouseLeave"
        @click="handleClick"
      ></canvas>

      <div class="labels-row">
        <div
          v-for="(label, idx) in labels"
          :key="'col-' + idx"
          class="label"
          :style="{ width: cellSize + 'px' }"
        >
          {{ truncateLabel(label) }}
        </div>
      </div>

      <div class="labels-col">
        <div
          v-for="(label, idx) in labels"
          :key="'row-' + idx"
          class="label"
          :style="{ height: cellSize + 'px' }"
        >
          {{ truncateLabel(label) }}
        </div>
      </div>

      <div
        v-if="tooltip.show"
        class="tooltip"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
      >
        <div class="tooltip-header">
          {{ tooltip.label1 }} ↔ {{ tooltip.label2 }}
        </div>
        <div class="tooltip-content">
          <div class="tooltip-row">
            <span>关联强度:</span>
            <span class="value">{{ tooltip.value }}%</span>
          </div>
          <div class="tooltip-row">
            <span>风险等级:</span>
            <span :class="'risk-' + tooltip.riskLevel">{{ tooltip.riskText }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = withDefaults(defineProps<{
  data: number[][]
  labels: string[]
  threshold?: number
}>(), {
  threshold: 85
})

const emit = defineEmits<{
  cellClick: [row: number, col: number, value: number]
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const wrapperRef = ref<HTMLDivElement | null>(null)
const cellSize = ref(60)

const mediumThreshold = computed(() => props.threshold * 0.6)

const tooltip = ref({
  show: false,
  x: 0,
  y: 0,
  label1: '',
  label2: '',
  value: 0,
  riskLevel: 'low',
  riskText: '低风险'
})

const getColor = (value: number): string => {
  if (value >= props.threshold) return 'rgba(255, 77, 79, 0.8)'
  if (value >= mediumThreshold.value) return 'rgba(250, 173, 20, 0.6)'
  if (value > 0) return 'rgba(82, 196, 26, 0.4)'
  return 'rgba(229, 229, 229, 0.3)'
}

const getTextColor = (value: number): string => {
  if (value >= props.threshold) return '#ff4d4f'
  if (value >= mediumThreshold.value) return '#d46b08'
  if (value > 0) return '#389e0d'
  return '#999'
}

const truncateLabel = (label: string, maxLen = 8): string => {
  if (!label) return ''
  return label.length > maxLen ? label.slice(0, maxLen) + '...' : label
}

const drawHeatmap = () => {
  const canvas = canvasRef.value
  if (!canvas || !props.data.length) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const matrixSize = props.data.length
  canvas.width = cellSize.value * matrixSize
  canvas.height = cellSize.value * matrixSize

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  for (let i = 0; i < matrixSize; i++) {
    for (let j = 0; j < matrixSize; j++) {
      const value = props.data[i]?.[j] ?? 0
      const x = j * cellSize.value
      const y = i * cellSize.value

      ctx.fillStyle = getColor(value)
      ctx.fillRect(x, y, cellSize.value - 2, cellSize.value - 2)

      if (i !== j && value > 0) {
        ctx.fillStyle = getTextColor(value)
        ctx.font = '12px -apple-system, BlinkMacSystemFont, sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(
          `${value}%`,
          x + cellSize.value / 2,
          y + cellSize.value / 2
        )
      }
    }
  }
}

const handleMouseMove = (e: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas) return

  const rect = canvas.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  const col = Math.floor(x / cellSize.value)
  const row = Math.floor(y / cellSize.value)

  if (row >= 0 && row < props.labels.length && col >= 0 && col < props.labels.length) {
    const value = props.data[row]?.[col] ?? 0

    tooltip.value = {
      show: true,
      x: e.clientX - rect.left + 10,
      y: e.clientY - rect.top + 10,
      label1: props.labels[row] || '',
      label2: props.labels[col] || '',
      value,
      riskLevel: value >= props.threshold ? 'high' : value >= mediumThreshold.value ? 'medium' : 'low',
      riskText: value >= props.threshold ? '高风险' : value >= mediumThreshold.value ? '中风险' : '低风险'
    }
  } else {
    tooltip.value.show = false
  }
}

const handleMouseLeave = () => {
  tooltip.value.show = false
}

const handleClick = (e: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas) return

  const rect = canvas.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  const col = Math.floor(x / cellSize.value)
  const row = Math.floor(y / cellSize.value)

  if (row >= 0 && row < props.data.length && col >= 0 && col < props.data.length) {
    const value = props.data[row]?.[col] ?? 0
    if (row !== col) {
      emit('cellClick', row, col, value)
    }
  }
}

const updateCellSize = () => {
  const wrapper = wrapperRef.value
  if (!wrapper) return

  const containerWidth = wrapper.clientWidth - cellSize.value
  if (props.labels.length > 0 && containerWidth > 0) {
    const calculatedSize = Math.floor(containerWidth / props.labels.length)
    cellSize.value = Math.max(40, Math.min(80, calculatedSize))
  }
}

let resizeObserver: ResizeObserver | null = null

onMounted(() => {
  updateCellSize()
  drawHeatmap()

  if (wrapperRef.value) {
    resizeObserver = new ResizeObserver(() => {
      updateCellSize()
      drawHeatmap()
    })
    resizeObserver.observe(wrapperRef.value)
  }
})

onUnmounted(() => {
  resizeObserver?.disconnect()
})

watch(() => [props.data, props.labels, props.threshold], () => {
  updateCellSize()
  drawHeatmap()
}, { deep: true })
</script>

<style scoped lang="scss">
.heatmap-container {
  background: #fff;
  border-radius: $radius-lg;
  padding: $spacing-xl;
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;

  h4 {
    margin: 0;
    font-size: $font-size-base;
    font-weight: $font-weight-semibold;
    color: $gray-800;
  }
}

.legend {
  display: flex;
  gap: $spacing-lg;

  .legend-item {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    font-size: $font-size-xs;
    color: $gray-600;
  }

  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: $radius-sm;

    &.high {
      background: rgba(255, 77, 79, 0.8);
    }

    &.medium {
      background: rgba(250, 173, 20, 0.6);
    }

    &.low {
      background: rgba(82, 196, 26, 0.4);
    }
  }
}

.heatmap-wrapper {
  position: relative;
  display: flex;
  padding-left: 80px;
  padding-top: 40px;
  overflow-x: auto;
}

canvas {
  cursor: pointer;
}

.labels-row {
  position: absolute;
  top: 0;
  left: 80px;
  display: flex;
  height: 40px;
}

.labels-col {
  position: absolute;
  left: 0;
  top: 40px;
  display: flex;
  flex-direction: column;
}

.label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $font-size-xs;
  color: $gray-600;
  padding: $spacing-xs;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tooltip {
  position: absolute;
  background: #fff;
  border: 1px solid $gray-300;
  border-radius: $radius-lg;
  padding: $spacing-md;
  box-shadow: $shadow-lg;
  z-index: $z-tooltip;
  pointer-events: none;
  min-width: 180px;
}

.tooltip-header {
  font-weight: $font-weight-semibold;
  color: $gray-800;
  margin-bottom: $spacing-sm;
  padding-bottom: $spacing-sm;
  border-bottom: 1px solid $gray-200;
}

.tooltip-content {
  .tooltip-row {
    display: flex;
    justify-content: space-between;
    font-size: $font-size-sm;
    color: $gray-600;
    margin-top: $spacing-xs;

    .value {
      font-weight: $font-weight-semibold;
      color: $gray-800;
    }

    .risk-high {
      color: $danger-color;
      font-weight: $font-weight-medium;
    }

    .risk-medium {
      color: $warning-color;
      font-weight: $font-weight-medium;
    }

    .risk-low {
      color: $success-color;
      font-weight: $font-weight-medium;
    }
  }
}
</style>
