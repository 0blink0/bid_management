<template>
  <AppLayout>
    <div class="project-detail-page">
      <PageHeader
        title="某市政府云平台建设项目"
        subtitle="审查时间：2024-03-15 14:30"
        back-link="/projects"
      />

      <!-- Stats -->
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <n-gi>
          <StatCard :value="3" label="投标单位" :icon="PeopleOutline" color="primary" />
        </n-gi>
        <n-gi>
          <StatCard :value="12" label="发现问题" :icon="AlertCircleOutline" color="warning" />
        </n-gi>
        <n-gi>
          <StatCard :value="2" label="风险预警" :icon="ShieldOutline" color="danger" />
        </n-gi>
        <n-gi>
          <StatCard :value="'无异常'" label="围串标检测" :icon="CheckmarkCircleOutline" color="success" />
        </n-gi>
      </n-grid>

      <!-- Project Info -->
      <n-card class="info-card" title="项目信息">
        <n-descriptions :column="2">
          <n-descriptions-item label="项目名称">某市政府云平台建设项目</n-descriptions-item>
          <n-descriptions-item label="预算">¥500万</n-descriptions-item>
          <n-descriptions-item label="招标单位">某市政府采购中心</n-descriptions-item>
          <n-descriptions-item label="审查时间">2024-03-15 14:30</n-descriptions-item>
        </n-descriptions>
      </n-card>

      <!-- Bidder List -->
      <n-card class="bidder-card" title="投标单位">
        <div class="bidder-list">
          <div v-for="bidder in bidders" :key="bidder.id" class="bidder-item">
            <div class="bidder-avatar">{{ bidder.name.charAt(0) }}</div>
            <div class="bidder-info">
              <span class="bidder-name">{{ bidder.name }}</span>
              <span class="bidder-file">{{ bidder.file }}</span>
            </div>
            <n-tag :type="bidder.status === 'passed' ? 'success' : 'warning'" size="small">
              {{ bidder.status === 'passed' ? '通过' : '有问题' }}
            </n-tag>
          </div>
        </div>
      </n-card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NGrid, NGi, NDescriptions, NDescriptionsItem, NTag } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import StatCard from '@/components/common/StatCard.vue'
import {
  PeopleOutline,
  AlertCircleOutline,
  ShieldOutline,
  CheckmarkCircleOutline
} from '@vicons/ionicons5'

const bidders = ref([
  { id: 1, name: '华夏科技有限公司', file: '投标文件_A.pdf', status: 'passed' },
  { id: 2, name: '中兴系统集成有限公司', file: '投标文件_B.pdf', status: 'warning' },
  { id: 3, name: '云端科技股份有限公司', file: '投标文件_C.pdf', status: 'passed' }
])
</script>

<style scoped lang="scss">
.project-detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.info-card,
.bidder-card {
  margin-top: 24px;
}

.bidder-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bidder-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--gray-100);
  border-radius: 8px;
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
</style>
