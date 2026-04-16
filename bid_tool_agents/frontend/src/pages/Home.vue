<template>
  <AppLayout>
    <div class="home-page">
      <div class="welcome-header">
        <h1>欢迎回来，张三</h1>
      </div>

      <!-- Statistics Grid -->
      <n-grid :cols="4" :x-gap="24" :y-gap="24">
        <n-gi>
          <StatCard
            :value="stats.totalReviews"
            label="总审查任务"
            :icon="DocumentTextOutline"
            color="primary"
          />
        </n-gi>
        <n-gi>
          <StatCard
            :value="stats.completed"
            label="已完成"
            :icon="CheckmarkCircleOutline"
            color="success"
          />
        </n-gi>
        <n-gi>
          <StatCard
            :value="stats.inProgress"
            label="进行中"
            :icon="TimeOutline"
            color="warning"
          />
        </n-gi>
        <n-gi>
          <StatCard
            :value="stats.riskWarnings"
            label="风险预警"
            :icon="AlertCircleOutline"
            color="danger"
          />
        </n-gi>
      </n-grid>

      <!-- Quick Entry Section -->
      <n-card class="quick-entry" title="快捷入口">
        <n-grid :cols="4" :x-gap="16" :y-gap="16">
          <n-gi>
            <div class="quick-entry-card" @click="goTo('/workspace/new')">
              <div class="entry-icon" style="background-color: rgba(30, 90, 168, 0.1);">
                <n-icon :size="24" color="#1E5AA8">
                  <AddOutline />
                </n-icon>
              </div>
              <span class="entry-text">新建审查</span>
            </div>
          </n-gi>
          <n-gi>
            <div class="quick-entry-card" @click="goTo('/risk-detection')">
              <div class="entry-icon" style="background-color: rgba(250, 173, 20, 0.1);">
                <n-icon :size="24" color="#faad14">
                  <AlertCircleOutline />
                </n-icon>
              </div>
              <span class="entry-text">围串标检测</span>
            </div>
          </n-gi>
          <n-gi>
            <div class="quick-entry-card" @click="goTo('/qualification-verify')">
              <div class="entry-icon" style="background-color: rgba(82, 196, 26, 0.1);">
                <n-icon :size="24" color="#52c41a">
                  <ShieldCheckmarkOutline />
                </n-icon>
              </div>
              <span class="entry-text">资质核验</span>
            </div>
          </n-gi>
          <n-gi>
            <div class="quick-entry-card" @click="goTo('/report/1')">
              <div class="entry-icon" style="background-color: rgba(114, 46, 209, 0.1);">
                <n-icon :size="24" color="#722ed1">
                  <DocumentTextOutline />
                </n-icon>
              </div>
              <span class="entry-text">查看报告</span>
            </div>
          </n-gi>
        </n-grid>
      </n-card>

      <!-- Recent Projects -->
      <n-card class="recent-projects" title="最近任务">
        <template #header-extra>
          <a class="view-all" @click="goTo('/reports')">查看全部</a>
        </template>
        <n-table :columns="columns" :data="recentTasks" :pagination="false">
          <template #empty>
            <n-empty description="暂无任务" />
          </template>
        </n-table>
      </n-card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NGrid, NGi, NTable, NTag, NIcon, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import StatCard from '@/components/common/StatCard.vue'
import {
  DocumentTextOutline,
  CheckmarkCircleOutline,
  TimeOutline,
  AlertCircleOutline,
  AddOutline,
  ShieldCheckmarkOutline
} from '@vicons/ionicons5'

const router = useRouter()

const stats = ref({
  totalReviews: 156,
  completed: 128,
  inProgress: 12,
  riskWarnings: 16
})

const recentTasks = ref([
  {
    id: 1,
    name: '某市政府云平台建设项目',
    type: '综合审查',
    status: '已完成',
    time: '2024-03-15 14:30'
  },
  {
    id: 2,
    name: '某高校智慧校园项目',
    type: '招标文件检测',
    status: '进行中',
    time: '2024-03-15 10:20'
  },
  {
    id: 3,
    name: '某医院信息化建设项目',
    type: '资质核验',
    status: '已完成',
    time: '2024-03-14 16:45'
  }
])

const columns = [
  {
    title: '项目名称',
    key: 'name'
  },
  {
    title: '审查类型',
    key: 'type'
  },
  {
    title: '状态',
    key: 'status',
    render(row) {
      const status = row.status === '已完成' ? 'success' : 'warning'
      return h(NTag, { type: status, size: 'small' }, () => row.status)
    }
  },
  {
    title: '完成时间',
    key: 'time'
  },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('a', {
        class: 'action-link',
        onClick: () => goTo(row.status === '已完成' ? `/report/${row.id}` : '/workspace/progress')
      }, row.status === '已完成' ? '查看报告' : '查看进度')
    }
  }
]

const goTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped lang="scss">
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-header {
  margin-bottom: 24px;

  h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: var(--gray-800);
  }
}

.quick-entry {
  margin-top: 24px;
}

.quick-entry-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  background: var(--gray-100);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: var(--gray-200);
    transform: translateY(-2px);
  }
}

.entry-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.entry-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-700);
}

.recent-projects {
  margin-top: 24px;
}

.view-all {
  color: var(--primary-color);
  font-size: 13px;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}

.action-link {
  color: var(--primary-color);
  font-size: 13px;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}
</style>
