<template>
  <AppLayout>
    <div class="qualification-check-page">
      <PageHeader
        title="资质核验"
        subtitle="某市政府云平台建设项目"
        back-link="/qualification-verify"
      />

      <!-- Stats -->
      <n-grid :cols="3" :x-gap="16" :y-gap="16">
        <n-gi>
          <div class="stat-card">
            <div class="stat-value success">5</div>
            <div class="stat-label">核验通过</div>
          </div>
        </n-gi>
        <n-gi>
          <div class="stat-card">
            <div class="stat-value warning">2</div>
            <div class="stat-label">需关注</div>
          </div>
        </n-gi>
        <n-gi>
          <div class="stat-card">
            <div class="stat-value danger">1</div>
            <div class="stat-label">核验失败</div>
          </div>
        </n-gi>
      </n-grid>

      <!-- Verification List -->
      <n-card class="verify-card" title="资质核验结果">
        <div class="verify-list">
          <div v-for="item in verifyItems" :key="item.id" class="verify-item">
            <div class="verify-indicator" :class="item.status"></div>
            <div class="verify-content">
              <div class="verify-header">
                <span class="verify-name">{{ item.name }}</span>
                <n-tag :type="getStatusType(item.status)" size="small">
                  {{ getStatusText(item.status) }}
                </n-tag>
              </div>
              <div class="verify-detail">
                <span>企业：{{ item.enterprise }}</span>
                <span>有效期：{{ item.validUntil }}</span>
              </div>
            </div>
          </div>
        </div>
      </n-card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NGrid, NGi, NTag } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

const verifyItems = ref([
  { id: 1, name: '营业执照', enterprise: '华夏科技有限公司', validUntil: '2025-03-15', status: 'pass' },
  { id: 2, name: '信息系统集成资质', enterprise: '华夏科技有限公司', validUntil: '2026-06-30', status: 'pass' },
  { id: 3, name: '安全生产许可证', enterprise: '中兴系统集成有限公司', validUntil: '2024-06-01', status: 'warning' },
  { id: 4, name: 'ISO9001认证', enterprise: '云端科技股份有限公司', validUntil: '2025-12-31', status: 'pass' },
  { id: 5, name: '软件企业认定', enterprise: '云端科技股份有限公司', validUntil: '已过期', status: 'fail' }
])

const getStatusType = (status: string) => {
  const map: Record<string, 'success' | 'warning' | 'error'> = {
    pass: 'success',
    warning: 'warning',
    fail: 'error'
  }
  return map[status]
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pass: '通过',
    warning: '即将过期',
    fail: '已过期'
  }
  return map[status]
}
</script>

<style scoped lang="scss">
.qualification-check-page {
  max-width: 900px;
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

  &.success { color: var(--success-color); }
  &.warning { color: var(--warning-color); }
  &.danger { color: var(--danger-color); }
}

.stat-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 4px;
}

.verify-card {
  margin-top: 24px;
}

.verify-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.verify-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--gray-100);
  border-radius: 8px;
}

.verify-indicator {
  width: 4px;
  border-radius: 2px;

  &.pass { background: var(--success-color); }
  &.warning { background: var(--warning-color); }
  &.fail { background: var(--danger-color); }
}

.verify-content {
  flex: 1;
}

.verify-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.verify-name {
  font-weight: 500;
  color: var(--gray-800);
}

.verify-detail {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: var(--gray-500);
}
</style>
