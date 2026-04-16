<template>
  <AppLayout>
    <div class="report-full-page">
      <PageHeader
        title="某市政府云平台建设项目"
        subtitle="审查时间：2024-03-15 14:30"
        back-link="/reports"
      >
        <template #actions>
          <n-button @click="goToChat">智能问答</n-button>
          <n-button type="primary">导出 PDF</n-button>
        </template>
      </PageHeader>

      <!-- Overview Stats -->
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <n-gi>
          <div class="stat-card">
            <div class="stat-value primary">3</div>
            <div class="stat-label">投标单位</div>
          </div>
        </n-gi>
        <n-gi>
          <div class="stat-card">
            <div class="stat-value warning">12</div>
            <div class="stat-label">发现问题</div>
          </div>
        </n-gi>
        <n-gi>
          <div class="stat-card">
            <div class="stat-value danger">2</div>
            <div class="stat-label">风险预警</div>
          </div>
        </n-gi>
        <n-gi>
          <div class="stat-card">
            <div class="stat-value success">无异常</div>
            <div class="stat-label">围串标检测</div>
          </div>
        </n-gi>
      </n-grid>

      <!-- Issues Section -->
      <n-card class="section-card" title="需要关注的问题">
        <div class="issue-list">
          <div v-for="issue in issues" :key="issue.id" class="issue-item">
            <div class="issue-indicator" :class="issue.severity"></div>
            <div class="issue-content">
              <div class="issue-header">
                <n-tag :type="issue.severity === 'danger' ? 'error' : 'warning'" size="small">
                  {{ issue.type }}
                </n-tag>
                <span class="issue-source">{{ issue.source }}</span>
                <span class="issue-location">[{{ issue.location }}]</span>
              </div>
              <div class="issue-title">{{ issue.title }}</div>
            </div>
          </div>
        </div>
      </n-card>

      <!-- Bidding Document Check -->
      <n-card class="section-card" title="招标文件检测">
        <div class="check-grid">
          <div v-for="check in biddingChecks" :key="check.key" class="check-item">
            <div class="check-status" :class="check.status">
              <n-icon v-if="check.status === 'pass'"><CheckmarkCircleOutline /></n-icon>
              <n-icon v-else><AlertCircleOutline /></n-icon>
            </div>
            <span class="check-name">{{ check.name }}</span>
            <n-tag v-if="check.status === 'pass'" type="success" size="small">通过</n-tag>
            <n-tag v-else type="error" size="small">未通过</n-tag>
          </div>
        </div>
      </n-card>

      <!-- Bidder Results -->
      <n-card class="section-card" title="投标方审查结果">
        <div class="bidder-list">
          <div v-for="bidder in bidders" :key="bidder.id" class="bidder-card">
            <div class="bidder-header">
              <div class="bidder-avatar">{{ bidder.name.charAt(0) }}</div>
              <div class="bidder-info">
                <span class="bidder-name">{{ bidder.name }}</span>
                <span class="bidder-file">{{ bidder.file }}</span>
              </div>
              <div class="bidder-score">
                <span class="score-value">{{ bidder.score }}</span>
                <span class="score-label">分</span>
              </div>
            </div>
            <div class="bidder-checks">
              <div class="check-section">
                <span class="check-section-title">资质核验</span>
                <n-tag type="success" size="small">通过</n-tag>
              </div>
              <div class="check-section">
                <span class="check-section-title">响应比对</span>
                <n-tag type="warning" size="small">部分偏离</n-tag>
              </div>
            </div>
          </div>
        </div>
      </n-card>

      <!-- Collusion Detection -->
      <n-card class="section-card" title="围串标检测">
        <div class="detection-grid">
          <div class="detection-item">
            <div class="detection-status pass">
              <n-icon><CheckmarkCircleOutline /></n-icon>
            </div>
            <span class="detection-label">投标文件雷同性</span>
            <n-tag type="success" size="small">正常</n-tag>
          </div>
          <div class="detection-item">
            <div class="detection-status pass">
              <n-icon><CheckmarkCircleOutline /></n-icon>
            </div>
            <span class="detection-label">企业关联分析</span>
            <n-tag type="success" size="small">无关联</n-tag>
          </div>
        </div>
      </n-card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NGrid, NGi, NCard, NTag, NButton, NIcon } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { CheckmarkCircleOutline, AlertCircleOutline } from '@vicons/ionicons5'

const router = useRouter()

const goToChat = () => {
  router.push('/report/1/chat')
}

const issues = ref([
  {
    id: 1,
    severity: 'danger',
    type: '招标文件',
    source: '华夏科技',
    location: '第30页',
    title: '存在错敏词问题'
  },
  {
    id: 2,
    severity: 'warning',
    type: '投标文件',
    source: '中兴系统',
    location: '第15页',
    title: '资质证书即将过期'
  }
])

const biddingChecks = ref([
  { key: 'sensitive', name: '错敏词检查', status: 'pass' },
  { key: 'compliance', name: '合规性检查', status: 'fail' },
  { key: 'completeness', name: '条款完整性', status: 'pass' },
  { key: 'evaluation', name: '评标办法', status: 'pass' }
])

const bidders = ref([
  {
    id: 1,
    name: '华夏科技有限公司',
    file: '投标文件_A.pdf',
    score: 92
  },
  {
    id: 2,
    name: '中兴系统集成有限公司',
    file: '投标文件_B.pdf',
    score: 85
  },
  {
    id: 3,
    name: '云端科技股份有限公司',
    file: '投标文件_C.pdf',
    score: 78
  }
])
</script>

<style scoped lang="scss">
.report-full-page {
  max-width: 1000px;
  margin: 0 auto;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--gray-800);

  &.primary {
    color: var(--primary-color);
  }

  &.warning {
    color: var(--warning-color);
  }

  &.danger {
    color: var(--danger-color);
  }

  &.success {
    color: var(--success-color);
  }
}

.stat-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 4px;
}

.section-card {
  margin-top: 24px;
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.issue-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.issue-indicator {
  width: 4px;
  border-radius: 2px;

  &.danger {
    background: var(--danger-color);
  }

  &.warning {
    background: var(--warning-color);
  }
}

.issue-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.issue-source {
  font-size: 13px;
  color: var(--gray-600);
}

.issue-location {
  font-size: 12px;
  color: var(--gray-500);
}

.issue-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-800);
}

.check-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.check-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.check-status {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  &.pass {
    background: var(--success-bg);
    color: var(--success-color);
  }

  &.fail {
    background: var(--danger-bg);
    color: var(--danger-color);
  }
}

.check-name {
  font-size: 13px;
  color: var(--gray-700);
}

.bidder-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bidder-card {
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.bidder-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.bidder-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.bidder-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.bidder-name {
  font-weight: 500;
  color: var(--gray-800);
}

.bidder-file {
  font-size: 12px;
  color: var(--gray-500);
}

.bidder-score {
  display: flex;
  align-items: baseline;
}

.score-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.score-label {
  font-size: 12px;
  color: var(--gray-500);
  margin-left: 2px;
}

.bidder-checks {
  display: flex;
  gap: 24px;
}

.check-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.check-section-title {
  font-size: 13px;
  color: var(--gray-600);
}

.detection-grid {
  display: flex;
  gap: 24px;
}

.detection-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detection-status {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  &.pass {
    background: var(--success-bg);
    color: var(--success-color);
  }
}

.detection-label {
  font-size: 14px;
  color: var(--gray-700);
}
</style>
