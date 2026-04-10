<template>
  <div class="home">
    <n-layout has-sider>
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="200"
        :collapsed="collapsed"
        show-trigger
        @collapse="collapsed = true"
        @expand="collapsed = false"
      >
        <n-menu
          v-model:value="activeKey"
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
        />
      </n-layout-sider>

      <n-layout>
        <n-layout-header bordered>
          <div class="header-content">
            <h1>智能招投标审查平台</h1>
            <n-button @click="logout">退出</n-button>
          </div>
        </n-layout-header>

        <n-layout-content content-style="padding: 24px;">
          <n-grid :cols="4" :x-gap="24" :y-gap="24">
            <n-gi>
              <n-card title="待处理任务">
                <n-statistic :value="stats.pending">
                  <template #suffix>个</template>
                </n-statistic>
              </n-card>
            </n-gi>
            <n-gi>
              <n-card title="处理中">
                <n-statistic :value="stats.processing">
                  <template #suffix>个</template>
                </n-statistic>
              </n-card>
            </n-gi>
            <n-gi>
              <n-card title="已完成">
                <n-statistic :value="stats.completed">
                  <template #suffix>个</template>
                </n-statistic>
              </n-card>
            </n-gi>
            <n-gi>
              <n-card title="风险预警">
                <n-statistic :value="stats.risks">
                  <template #suffix>个</template>
                </n-statistic>
              </n-card>
            </n-gi>
          </n-grid>

          <n-card title="最近任务" style="margin-top: 24px;">
            <n-table :columns="columns" :data="recentTasks">
              <template #empty>
                <n-empty description="暂无任务" />
              </template>
            </n-table>
          </n-card>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import type { MenuOption } from 'naive-ui'
import { NIcon } from 'naive-ui'
import {
  HomeOutline,
  DocumentOutline,
  CheckmarkCircleOutline,
  AlertCircleOutline,
  PersonOutline,
  SettingsOutline
} from '@vicons/ionicons5'

const collapsed = ref(false)
const activeKey = ref('home')

const stats = ref({
  pending: 12,
  processing: 5,
  completed: 128,
  risks: 3
})

const recentTasks = ref([])

const columns = [
  { title: '任务名称', key: 'name' },
  { title: '类型', key: 'type' },
  { title: '状态', key: 'status' },
  { title: '创建时间', key: 'createdAt' }
]

const renderIcon = (icon: any) => {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: '首页',
    key: 'home',
    icon: renderIcon(HomeOutline)
  },
  {
    label: '文件上传',
    key: 'upload',
    icon: renderIcon(DocumentOutline)
  },
  {
    label: '合规审查',
    key: 'compliance-review',
    icon: renderIcon(CheckmarkCircleOutline)
  },
  {
    label: '风险识别',
    key: 'risk-detection',
    icon: renderIcon(AlertCircleOutline)
  },
  {
    label: '专家抽取',
    key: 'expert-selection',
    icon: renderIcon(PersonOutline)
  },
  {
    label: '系统设置',
    key: 'settings',
    icon: renderIcon(SettingsOutline)
  }
]

const logout = () => {
  console.log('logout')
}
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.header-content h1 {
  font-size: 18px;
  margin: 0;
}
</style>
