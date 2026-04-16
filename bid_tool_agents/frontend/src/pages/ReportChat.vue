<template>
  <AppLayout>
    <div class="report-chat-page">
      <div class="report-layout">
        <!-- Main Content -->
        <div class="report-main">
          <PageHeader
            title="某市政府云平台建设项目"
            subtitle="选择投标单位进行围串标检测分析"
            back-link="/risk-detection"
          >
            <template #actions>
              <n-button>导出报告</n-button>
              <n-button type="primary">开始检测</n-button>
            </template>
          </PageHeader>

          <!-- Stats -->
          <n-grid :cols="4" :x-gap="16" :y-gap="16">
            <n-gi>
              <div class="stat-card">
                <n-icon :size="24" color="#1E5AA8"><PeopleOutline /></n-icon>
                <div class="stat-info">
                  <span class="stat-value">3</span>
                  <span class="stat-label">投标单位</span>
                </div>
              </div>
            </n-gi>
            <n-gi>
              <div class="stat-card">
                <n-icon :size="24" color="#722ed1"><SwapHorizontalOutline /></n-icon>
                <div class="stat-info">
                  <span class="stat-value">3</span>
                  <span class="stat-label">检测组合</span>
                </div>
              </div>
            </n-gi>
            <n-gi>
              <div class="stat-card">
                <n-icon :size="24" color="#faad14"><AlertCircleOutline /></n-icon>
                <div class="stat-info">
                  <span class="stat-value">2</span>
                  <span class="stat-label">可疑组合</span>
                </div>
              </div>
            </n-gi>
            <n-gi>
              <div class="stat-card">
                <n-icon :size="24" color="#ff4d4f"><ShieldOutline /></n-icon>
                <div class="stat-info">
                  <span class="stat-value danger">高风险</span>
                  <span class="stat-label">整体风险</span>
                </div>
              </div>
            </n-gi>
          </n-grid>

          <!-- Bidder Selection -->
          <n-card class="bidder-section" title="选择投标单位">
            <template #header-extra>
              <span class="selection-hint">已选择 {{ selectedBidders.length }} 家（需≥2家）</span>
            </template>
            <div class="bidder-actions">
              <n-button size="small" @click="selectAll">全选</n-button>
              <n-button size="small" @click="clearSelection">清空</n-button>
            </div>
            <div class="bidder-grid">
              <div
                v-for="bidder in bidders"
                :key="bidder.id"
                :class="['bidder-card', { selected: selectedBidders.includes(bidder.id) }]"
                @click="toggleBidder(bidder.id)"
              >
                <div class="bidder-avatar">{{ bidder.name.charAt(0) }}</div>
                <div class="bidder-name">{{ bidder.name }}</div>
                <RiskBadge :level="bidder.risk" />
                <div class="bidder-checkbox">
                  <div class="checkbox-inner"></div>
                </div>
              </div>
            </div>
          </n-card>

          <!-- Detection Results -->
          <n-card v-if="showResults" class="results-section" title="检测结果">
            <!-- Heat Map -->
            <div class="result-subsection">
              <h4>关联度矩阵</h4>
              <div class="heatmap">
                <table>
                  <tr>
                    <th></th>
                    <th v-for="b in bidders" :key="b.id">{{ b.name }}</th>
                  </tr>
                  <tr v-for="row in heatmapData" :key="row.bidder1">
                    <th>{{ row.bidder1Name }}</th>
                    <td
                      v-for="cell in row.cells"
                      :key="cell.bidder2"
                      :class="['heat-cell', cell.level]"
                    >
                      {{ cell.value }}%
                    </td>
                  </tr>
                </table>
              </div>
            </div>

            <!-- Suspicious Combinations -->
            <div class="result-subsection">
              <h4>可疑组合详情</h4>
              <div class="suspicious-list">
                <div v-for="item in suspiciousItems" :key="item.id" class="suspicious-item">
                  <div class="suspicious-header">
                    <span class="suspicious-pair">{{ item.bidder1 }} × {{ item.bidder2 }}</span>
                    <n-tag type="warning">{{ item.riskLevel }}</n-tag>
                  </div>
                  <div class="evidence-grid">
                    <div class="evidence-item">
                      <span class="evidence-label">人员重叠</span>
                      <span class="evidence-value">{{ item.personOverlap }}</span>
                    </div>
                    <div class="evidence-item">
                      <span class="evidence-label">联系方式重叠</span>
                      <span class="evidence-value">{{ item.contactOverlap }}</span>
                    </div>
                    <div class="evidence-item">
                      <span class="evidence-label">文件相似度</span>
                      <span class="evidence-value">{{ item.fileSimilarity }}</span>
                    </div>
                    <div class="evidence-item">
                      <span class="evidence-label">资质重叠</span>
                      <span class="evidence-value">{{ item.qualificationOverlap }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </n-card>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NGrid, NGi, NCard, NTag, NButton, NIcon } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import RiskBadge from '@/components/common/RiskBadge.vue'
import {
  PeopleOutline,
  SwapHorizontalOutline,
  AlertCircleOutline,
  ShieldOutline
} from '@vicons/ionicons5'

const selectedBidders = ref<number[]>([])
const showResults = ref(false)

const bidders = ref([
  { id: 1, name: '华夏科技有限公司', risk: 'none' as const },
  { id: 2, name: '中兴系统集成有限公司', risk: 'high' as const },
  { id: 3, name: '云端科技股份有限公司', risk: 'medium' as const }
])

const heatmapData = ref([
  {
    bidder1: 1, bidder1Name: '华夏科技',
    cells: [
      { bidder2: 1, value: '-', level: '' },
      { bidder2: 2, value: '78', level: 'high' },
      { bidder2: 3, value: '45', level: 'medium' }
    ]
  },
  {
    bidder1: 2, bidder1Name: '中兴系统',
    cells: [
      { bidder2: 1, value: '78', level: 'high' },
      { bidder2: 2, value: '-', level: '' },
      { bidder2: 3, value: '82', level: 'high' }
    ]
  },
  {
    bidder1: 3, bidder1Name: '云端科技',
    cells: [
      { bidder2: 1, value: '45', level: 'medium' },
      { bidder2: 2, value: '82', level: 'high' },
      { bidder2: 3, value: '-', level: '' }
    ]
  }
])

const suspiciousItems = ref([
  {
    id: 1,
    bidder1: '中兴系统',
    bidder2: '云端科技',
    riskLevel: '高风险',
    personOverlap: '3人',
    contactOverlap: '2个',
    fileSimilarity: '89%',
    qualificationOverlap: '5个'
  }
])

const toggleBidder = (id: number) => {
  const index = selectedBidders.value.indexOf(id)
  if (index > -1) {
    selectedBidders.value.splice(index, 1)
  } else {
    selectedBidders.value.push(id)
  }
}

const selectAll = () => {
  selectedBidders.value = bidders.value.map(b => b.id)
}

const clearSelection = () => {
  selectedBidders.value = []
}
</script>

<style scoped lang="scss">
.report-chat-page {
  height: 100%;
}

.report-layout {
  display: flex;
  gap: 24px;
}

.report-main {
  flex: 1;
  min-width: 0;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-800);

  &.danger {
    color: var(--danger-color);
  }
}

.stat-label {
  font-size: 12px;
  color: var(--gray-500);
}

.bidder-section {
  margin-top: 24px;
}

.selection-hint {
  font-size: 13px;
  color: var(--gray-500);
}

.bidder-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.bidder-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.bidder-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--primary-color);
  }

  &.selected {
    border-color: var(--primary-color);
    background: var(--primary-bg);

    .bidder-checkbox .checkbox-inner {
      background: var(--primary-color);
      border-color: var(--primary-color);
    }
  }
}

.bidder-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
}

.bidder-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
  text-align: center;
}

.bidder-checkbox {
  position: absolute;
  top: 12px;
  right: 12px;
}

.checkbox-inner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--gray-300);
  border-radius: 4px;
  transition: all 0.2s;
}

.results-section {
  margin-top: 24px;
}

.result-subsection {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }

  h4 {
    margin: 0 0 16px;
    font-size: 14px;
    font-weight: 600;
    color: var(--gray-700);
  }
}

.heatmap {
  overflow-x: auto;

  table {
    width: 100%;
    border-collapse: collapse;

    th, td {
      padding: 12px;
      text-align: center;
      border: 1px solid var(--gray-200);
    }

    th {
      background: var(--gray-100);
      font-weight: 500;
      font-size: 13px;
    }
  }
}

.heat-cell {
  font-weight: 600;

  &.high {
    background: var(--danger-bg);
    color: var(--danger-color);
  }

  &.medium {
    background: var(--warning-bg);
    color: var(--warning-color);
  }

  &.low {
    background: var(--success-bg);
    color: var(--success-color);
  }
}

.suspicious-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.suspicious-item {
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.suspicious-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.suspicious-pair {
  font-weight: 600;
  color: var(--gray-800);
}

.evidence-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.evidence-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.evidence-label {
  font-size: 12px;
  color: var(--gray-500);
}

.evidence-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
}
</style>
