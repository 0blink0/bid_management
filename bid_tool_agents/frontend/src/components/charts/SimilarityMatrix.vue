<template>
  <div class="similarity-matrix">
    <div class="matrix-header">
      <h4>相似度矩阵</h4>
      <div class="legend">
        <span class="legend-item high">🔴 高风险 (&gt;85%)</span>
        <span class="legend-item medium">🟡 中风险 (50-85%)</span>
        <span class="legend-item low">🟢 低风险 (&lt;50%)</span>
      </div>
    </div>

    <div class="matrix-container">
      <table class="matrix-table">
        <thead>
          <tr>
            <th></th>
            <th v-for="doc in documents" :key="doc">{{ doc }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIdx) in matrix" :key="rowIdx">
            <td class="row-label">{{ documents[rowIdx] }}</td>
            <td
              v-for="(cell, colIdx) in row"
              :key="colIdx"
              class="matrix-cell"
              :class="getCellClass(cell)"
              @click="handleCellClick(rowIdx, colIdx, cell)"
            >
              <span v-if="rowIdx !== colIdx">{{ cell }}%</span>
              <span v-else class="diagonal">-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 详情弹窗 -->
    <n-modal v-model:show="showDetail" preset="card" title="相似详情" style="width: 600px">
      <div class="detail-content">
        <div class="detail-header">
          <n-tag type="error">高风险相似</n-tag>
          <span>{{ documents[fromIdx] }} ↔ {{ documents[toIdx] }}</span>
        </div>

        <div class="comparison-view">
          <div class="comparison-item">
            <div class="comparison-label">{{ documents[fromIdx] }}</div>
            <div class="comparison-text" v-html="highlightText(texts[fromIdx])"></div>
          </div>
          <div class="comparison-item">
            <div class="comparison-label">{{ documents[toIdx] }}</div>
            <div class="comparison-text" v-html="highlightText(texts[toIdx])"></div>
          </div>
        </div>

        <div class="similarity-stats">
          <n-statistic label="相似段落数" :value="similarParagraphs" />
          <n-statistic label="平均相似度" :value="avgSimilarity + '%'" />
        </div>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = withDefaults(defineProps<{
  documents: string[]
  matrix: number[][]
  texts?: string[]
}>(), {
  texts: () => []
})

const emit = defineEmits<{
  cellClick: [row: number, col: number, value: number]
}>()

const showDetail = ref(false)
const fromIdx = ref(0)
const toIdx = ref(0)
const similarParagraphs = ref(12)
const avgSimilarity = ref(94)

const getCellClass = (value: number) => {
  if (value > 85) return 'cell-high'
  if (value > 50) return 'cell-medium'
  if (value > 0) return 'cell-low'
  return ''
}

const handleCellClick = (row: number, col: number, value: number) => {
  if (row === col || value <= 0) return
  fromIdx.value = row
  toIdx.value = col
  showDetail.value = true
  emit('cellClick', row, col, value)
}

const highlightText = (text: string) => {
  // 简化的高亮显示
  return text || '未提供原文'
}
</script>

<style scoped lang="scss">
.similarity-matrix {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

.matrix-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  h4 {
    margin: 0;
    font-size: 14px;
  }

  .legend {
    display: flex;
    gap: 16px;
    font-size: 12px;
  }
}

.matrix-container {
  overflow-x: auto;
}

.matrix-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;

  th, td {
    padding: 8px 12px;
    text-align: center;
    border: 1px solid #e8e8e8;
  }

  th {
    background: #fafafa;
    font-weight: 600;
    position: sticky;
    top: 0;
  }

  .row-label {
    background: #fafafa;
    font-weight: 600;
    position: sticky;
    left: 0;
  }
}

.matrix-cell {
  cursor: pointer;
  transition: all 0.2s;

  &:hover:not(.diagonal) {
    transform: scale(1.1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .diagonal {
    color: #ddd;
  }

  &.cell-high {
    background: #fff1f0;
    color: #cf1322;
    font-weight: 600;
  }

  &.cell-medium {
    background: #fffbe6;
    color: #d46b08;
  }

  &.cell-low {
    background: #f6ffed;
    color: #389e0d;
  }
}

.detail-content {
  .detail-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }
}

.comparison-view {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;

  .comparison-label {
    font-weight: 600;
    margin-bottom: 8px;
    color: #666;
  }

  .comparison-text {
    background: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    font-size: 13px;
    line-height: 1.6;
    max-height: 200px;
    overflow-y: auto;
  }
}

.similarity-stats {
  display: flex;
  gap: 24px;
}
</style>
