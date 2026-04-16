<template>
  <AppLayout>
    <div class="knowledge-base-page">
      <PageHeader title="知识库管理" subtitle="管理法规库、规则库、模板库等知识资源" />

      <div class="kb-container">
        <!-- Tabs -->
        <div class="kb-tabs">
          <div
            v-for="tab in tabs"
            :key="tab.key"
            :class="['kb-tab', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </div>
        </div>

        <!-- Toolbar -->
        <div class="kb-toolbar">
          <div class="toolbar-left">
            <SearchInput v-model="searchKey" placeholder="搜索..." />
            <FilterSelect
              v-model="statusFilter"
              :options="statusOptions"
              placeholder="状态"
            />
          </div>
          <div class="toolbar-right">
            <n-button @click="handleImport">批量导入</n-button>
            <n-button @click="handleExport">导出</n-button>
            <n-button type="primary" @click="showAddModal = true">新增</n-button>
          </div>
        </div>

        <!-- Table Content -->
        <n-card>
          <!-- Regulation Table -->
          <n-table v-if="activeTab === 'regulation'" :columns="regulationColumns" :data="regulations">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>

          <!-- Rules Table -->
          <n-table v-else-if="activeTab === 'rules'" :columns="rulesColumns" :data="rules">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>

          <!-- Sensitive Words Table -->
          <n-table v-else-if="activeTab === 'sensitive'" :columns="sensitiveColumns" :data="sensitiveWords">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>

          <!-- Templates Table -->
          <n-table v-else-if="activeTab === 'templates'" :columns="templateColumns" :data="templates">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>

          <!-- Cases Table -->
          <n-table v-else-if="activeTab === 'cases'" :columns="caseColumns" :data="cases">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>

          <!-- Activation Table -->
          <n-table v-else-if="activeTab === 'activation'" :columns="activationColumns" :data="activations">
            <template #empty>
              <n-empty description="暂无数据" />
            </template>
          </n-table>
        </n-card>
      </div>

      <!-- Add/Edit Modal -->
      <Modal
        v-model:show="showAddModal"
        :title="editingItem ? '编辑' : '新增'"
        width="600px"
      >
        <n-form :model="formValue" label-placement="top">
          <n-form-item label="法规名称">
            <n-input v-model:value="formValue.name" placeholder="请输入法规名称" />
          </n-form-item>
          <n-form-item label="文号">
            <n-input v-model:value="formValue.number" placeholder="请输入文号" />
          </n-form-item>
          <n-form-item label="发布部门">
            <n-input v-model:value="formValue.department" placeholder="请输入发布部门" />
          </n-form-item>
          <n-form-item label="实施日期">
            <n-date-picker v-model:value="formValue.date" type="date" style="width: 100%" />
          </n-form-item>
          <n-form-item label="状态">
            <n-radio-group v-model:value="formValue.status">
              <n-space>
                <n-radio value="enabled">启用</n-radio>
                <n-radio value="disabled">禁用</n-radio>
              </n-space>
            </n-radio-group>
          </n-form-item>
        </n-form>
        <template #footer>
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button type="primary" @click="saveItem">保存</n-button>
        </template>
      </Modal>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NCard, NTable, NTag, NButton, NIcon, NForm, NFormItem, NRadioGroup, NSpace, NRadio, NInput, NDatePicker, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import Modal from '@/components/common/Modal.vue'
import { AddOutline, DownloadOutline, EyeOutline, CreateOutline } from '@vicons/ionicons5'
import type { SelectOption } from 'naive-ui'

const activeTab = ref('regulation')
const searchKey = ref('')
const statusFilter = ref(null)
const showAddModal = ref(false)
const editingItem = ref<any>(null)

const formValue = ref({
  name: '',
  number: '',
  department: '',
  date: null,
  status: 'enabled'
})

const tabs = [
  { key: 'regulation', label: '法规库' },
  { key: 'rules', label: '规则库' },
  { key: 'sensitive', label: '错敏词库' },
  { key: 'templates', label: '模板库' },
  { key: 'cases', label: '案例库' },
  { key: 'activation', label: '规则生效' }
]

const statusOptions: SelectOption[] = [
  { label: '全部状态', value: null },
  { label: '启用', value: 'enabled' },
  { label: '禁用', value: 'disabled' }
]

const regulations = ref([
  { id: 1, name: '政府采购法', number: '主席令第68号', department: '全国人大', date: '2003-01-01', status: 'enabled' },
  { id: 2, name: '招投标法', number: '主席令第21号', department: '全国人大', date: '2000-01-01', status: 'enabled' }
])

const regulationColumns = [
  { title: '法规名称', key: 'name' },
  { title: '文号', key: 'number' },
  { title: '发布部门', key: 'department' },
  { title: '实施日期', key: 'date' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'error', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  {
    title: '操作',
    key: 'actions',
    render() {
      return h('div', { class: 'action-buttons' }, [
        h(NButton, { quaternary: true, size: 'small', onClick: () => {} }, () => h(NIcon, null, { default: () => h(CreateOutline) })),
        h(NButton, { quaternary: true, size: 'small', type: 'error', onClick: () => {} }, () => '删除')
      ])
    }
  }
]

const rules = ref([
  { id: 1, name: '错敏词检查规则', type: '符合性检查', severity: 'high', status: 'enabled' },
  { id: 2, name: '资质有效期规则', type: '有效性检查', severity: 'medium', status: 'enabled' }
])

const rulesColumns = [
  { title: '规则名称', key: 'name' },
  { title: '规则类型', key: 'type' },
  {
    title: '严重程度',
    key: 'severity',
    render(row) {
      const typeMap: Record<string, 'error' | 'warning' | 'info'> = { high: 'error', medium: 'warning', low: 'info' }
      return h(NTag, { type: typeMap[row.severity], size: 'small' }, () => row.severity === 'high' ? '高' : row.severity === 'medium' ? '中' : '低')
    }
  },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'error', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  { title: '操作', key: 'actions' }
]

const sensitiveWords = ref([
  { id: 1, word: '贪污', type: 'sensitive', category: '腐败类', replacement: '违规', status: 'enabled' },
  { id: 2, word: '行贿', type: 'sensitive', category: '腐败类', replacement: '违规', status: 'enabled' }
])

const sensitiveColumns = [
  { title: '错敏词', key: 'word' },
  {
    title: '类型',
    key: 'type',
    render(row) {
      return h(NTag, { type: row.type === 'error' ? 'warning' : 'error', size: 'small' }, () => row.type === 'error' ? '错别字' : '敏感词')
    }
  },
  { title: '分类', key: 'category' },
  { title: '替换建议', key: 'replacement' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'error', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  { title: '操作', key: 'actions' }
]

const templates = ref([
  { id: 1, name: '投标函模板', type: '投标文件', format: 'DOCX', version: 'v1.2', updateTime: '2024-03-01' },
  { id: 2, name: '技术方案模板', type: '技术文件', format: 'DOCX', version: 'v2.0', updateTime: '2024-02-15' }
])

const templateColumns = [
  { title: '模板名称', key: 'name' },
  { title: '类型', key: 'type' },
  { title: '文件格式', key: 'format' },
  { title: '版本', key: 'version' },
  { title: '更新时间', key: 'updateTime' },
  {
    title: '操作',
    key: 'actions',
    render() {
      return h('div', { class: 'action-buttons' }, [
        h(NButton, { quaternary: true, size: 'small', onClick: () => {} }, () => '预览'),
        h(NButton, { quaternary: true, size: 'small', onClick: () => {} }, () => h(NIcon, null, { default: () => h(DownloadOutline) }))
      ])
    }
  }
]

const cases = ref([
  { id: 1, name: '某市教育局设备采购案', type: '设备采购', result: 'warning', problems: 3, importTime: '2024-03-10' },
  { id: 2, name: '某医院信息化建设案', type: '信息化建设', result: 'pass', problems: 0, importTime: '2024-03-08' }
])

const caseColumns = [
  { title: '案例名称', key: 'name' },
  { title: '项目类型', key: 'type' },
  {
    title: '审查结果',
    key: 'result',
    render(row) {
      const typeMap: Record<string, 'success' | 'warning' | 'error'> = { pass: 'success', warning: 'warning', danger: 'error' }
      return h(NTag, { type: typeMap[row.result], size: 'small' }, () => row.result === 'pass' ? '通过' : row.result === 'warning' ? '警告' : '危险')
    }
  },
  { title: '问题数量', key: 'problems' },
  { title: '导入时间', key: 'importTime' },
  { title: '操作', key: 'actions' }
]

const activations = ref([
  { id: 1, name: '错敏词检查规则', type: '符合性检查', effectiveTime: '2024-03-01', expiryTime: '2025-03-01', priority: 'high', status: 'enabled' }
])

const activationColumns = [
  { title: '规则名称', key: 'name' },
  { title: '规则类型', key: 'type' },
  { title: '生效时间', key: 'effectiveTime' },
  { title: '失效时间', key: 'expiryTime' },
  {
    title: '优先级',
    key: 'priority',
    render(row) {
      const typeMap: Record<string, 'error' | 'warning' | 'info'> = { high: 'error', medium: 'warning', low: 'info' }
      return h(NTag, { type: typeMap[row.priority], size: 'small' }, () => row.priority === 'high' ? '高' : row.priority === 'medium' ? '中' : '低')
    }
  },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'error', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  { title: '操作', key: 'actions' }
]

const handleImport = () => {}
const handleExport = () => {}
const saveItem = () => {
  showAddModal.value = false
}
</script>

<style scoped lang="scss">
.knowledge-base-page {
  max-width: 1100px;
  margin: 0 auto;
}

.kb-container {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.kb-tabs {
  display: flex;
  border-bottom: 1px solid var(--gray-200);
  background: var(--gray-100);
}

.kb-tab {
  padding: 14px 24px;
  font-size: 14px;
  color: var(--gray-600);
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;

  &:hover {
    color: var(--gray-800);
  }

  &.active {
    color: var(--primary-color);
    background: #fff;
    border-bottom-color: var(--primary-color);
  }
}

.kb-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gray-200);
}

.toolbar-left {
  display: flex;
  gap: 12px;
}

.toolbar-right {
  display: flex;
  gap: 12px;
}

.action-buttons {
  display: flex;
  gap: 4px;
}
</style>
