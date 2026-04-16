<template>
  <AppLayout>
    <div class="admin-page">
      <PageHeader
        title="用户管理"
        subtitle="管理系统用户和权限"
      >
        <template #actions>
          <n-button type="primary" @click="showAddModal = true">
            <template #icon>
              <n-icon><AddOutline /></n-icon>
            </template>
            添加用户
          </n-button>
        </template>
      </PageHeader>

      <!-- Filters -->
      <n-card class="filter-card">
        <div class="filters">
          <SearchInput v-model="searchKey" placeholder="搜索用户名或姓名" />
          <FilterSelect
            v-model="roleFilter"
            :options="roleOptions"
            placeholder="全部角色"
          />
          <FilterSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="全部状态"
          />
        </div>
      </n-card>

      <!-- User Table -->
      <n-card>
        <n-table :columns="columns" :data="users" :pagination="false">
          <template #empty>
            <n-empty description="暂无用户" />
          </template>
        </n-table>

        <Pagination
          :total="total"
          :current-page="currentPage"
          @change="handlePageChange"
        />
      </n-card>

      <!-- Add/Edit User Modal -->
      <Modal
        v-model:show="showAddModal"
        :title="editingUser ? '编辑用户' : '添加用户'"
        width="500px"
      >
        <n-form :model="formValue" label-placement="top">
          <n-form-item label="用户名">
            <n-input v-model:value="formValue.username" placeholder="请输入用户名" />
          </n-form-item>
          <n-form-item label="姓名">
            <n-input v-model:value="formValue.name" placeholder="请输入姓名" />
          </n-form-item>
          <n-form-item label="角色">
            <n-radio-group v-model:value="formValue.role">
              <n-space>
                <n-radio value="admin">管理员</n-radio>
                <n-radio value="reviewer">审查员</n-radio>
                <n-radio value="viewer">查看者</n-radio>
              </n-space>
            </n-radio-group>
          </n-form-item>
          <n-form-item v-if="!editingUser" label="初始密码">
            <n-input v-model:value="formValue.password" type="password" placeholder="请输入初始密码" />
          </n-form-item>
        </n-form>
        <template #footer>
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button type="primary" @click="saveUser">保存</n-button>
        </template>
      </Modal>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NCard, NTable, NTag, NButton, NIcon, NForm, NFormItem, NRadioGroup, NSpace, NRadio, NInput } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import Pagination from '@/components/common/Pagination.vue'
import Modal from '@/components/common/Modal.vue'
import { AddOutline, CreateOutline, TrashOutline } from '@vicons/ionicons5'
import type { SelectOption } from 'naive-ui'

const searchKey = ref('')
const roleFilter = ref(null)
const statusFilter = ref(null)
const showAddModal = ref(false)
const editingUser = ref<any>(null)

const total = ref(12)
const currentPage = ref(1)

const formValue = ref({
  username: '',
  name: '',
  role: 'viewer',
  password: ''
})

const roleOptions: SelectOption[] = [
  { label: '全部角色', value: null },
  { label: '管理员', value: 'admin' },
  { label: '审查员', value: 'reviewer' },
  { label: '查看者', value: 'viewer' }
]

const statusOptions: SelectOption[] = [
  { label: '全部状态', value: null },
  { label: '启用', value: 'enabled' },
  { label: '禁用', value: 'disabled' }
]

const users = ref([
  { id: 1, username: 'admin', name: '管理员', role: 'admin', department: '技术部', status: 'enabled', lastLogin: '2024-03-15 14:30' },
  { id: 2, username: 'zhangsan', name: '张三', role: 'reviewer', department: '审查部', status: 'enabled', lastLogin: '2024-03-15 10:20' },
  { id: 3, username: 'lisi', name: '李四', role: 'viewer', department: '财务部', status: 'enabled', lastLogin: '2024-03-14 16:45' },
  { id: 4, username: 'wangwu', name: '王五', role: 'reviewer', department: '审查部', status: 'disabled', lastLogin: '2024-03-10 09:00' }
])

const roleTypeMap: Record<string, string> = {
  admin: 'error',
  reviewer: 'warning',
  viewer: 'success'
}

const columns = [
  {
    title: '用户',
    key: 'user',
    render(row) {
      return h('div', { class: 'user-cell' }, [
        h('div', { class: 'user-avatar' }, row.name.charAt(0)),
        h('div', { class: 'user-info' }, [
          h('span', { class: 'user-name' }, row.name),
          h('span', { class: 'user-username' }, row.username)
        ])
      ])
    }
  },
  {
    title: '角色',
    key: 'role',
    render(row) {
      return h(NTag, { type: roleTypeMap[row.role] as any, size: 'small' }, () => {
        const roleMap: Record<string, string> = { admin: '管理员', reviewer: '审查员', viewer: '查看者' }
        return roleMap[row.role]
      })
    }
  },
  { title: '部门', key: 'department' },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'warning', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  { title: '最后登录', key: 'lastLogin' },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('div', { class: 'action-buttons' }, [
        h(NButton, { quaternary: true, size: 'small', onClick: () => editUser(row) }, () => h(NIcon, null, { default: () => h(CreateOutline) })),
        h(NButton, { quaternary: true, size: 'small', type: 'error', onClick: () => deleteUser(row.id) }, () => h(NIcon, null, { default: () => h(TrashOutline) }))
      ])
    }
  }
]

const handlePageChange = (page: number) => {
  currentPage.value = page
}

const editUser = (user: any) => {
  editingUser.value = user
  formValue.value = { ...user, password: '' }
  showAddModal.value = true
}

const deleteUser = (id: number) => {
  // Delete user
}

const saveUser = () => {
  showAddModal.value = false
  editingUser.value = null
}
</script>

<style scoped lang="scss">
.admin-page {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 16px;
}

.filters {
  display: flex;
  gap: 16px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: var(--gray-800);
}

.user-username {
  font-size: 12px;
  color: var(--gray-500);
}

.action-buttons {
  display: flex;
  gap: 4px;
}
</style>
