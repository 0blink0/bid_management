<template>
  <AppLayout>
    <div class="user-management-page">
      <PageHeader
        title="用户管理"
        back-link="/admin"
      >
        <template #actions>
          <n-button type="primary" @click="showModal = true">
            <template #icon>
              <n-icon><AddOutline /></n-icon>
            </template>
            添加用户
          </n-button>
        </template>
      </PageHeader>

      <n-card>
        <n-table :columns="columns" :data="users" :pagination="false">
          <template #empty>
            <n-empty description="暂无用户" />
          </template>
        </n-table>
      </n-card>

      <!-- User Modal -->
      <div :class="['modal-overlay', { active: showModal }]" @click.self="showModal = false">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ editingUser ? '编辑用户' : '添加用户' }}</h3>
            <n-button quaternary circle @click="showModal = false">
              <template #icon>
                <n-icon><CloseOutline /></n-icon>
              </template>
            </n-button>
          </div>
          <div class="modal-body">
            <div class="form-item">
              <label>用户名</label>
              <n-input v-model:value="formValue.username" placeholder="请输入用户名" />
            </div>
            <div class="form-item">
              <label>姓名</label>
              <n-input v-model:value="formValue.name" placeholder="请输入姓名" />
            </div>
            <div class="form-item">
              <label>角色</label>
              <n-radio-group v-model:value="formValue.role">
                <n-space>
                  <n-radio value="admin">管理员</n-radio>
                  <n-radio value="user">用户</n-radio>
                </n-space>
              </n-radio-group>
            </div>
            <div v-if="!editingUser" class="form-item">
              <label>初始密码</label>
              <n-input v-model:value="formValue.password" type="password" placeholder="请输入初始密码" />
            </div>
          </div>
          <div class="modal-footer">
            <n-button @click="showModal = false">取消</n-button>
            <n-button type="primary" @click="saveUser">保存</n-button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NCard, NTable, NTag, NButton, NIcon, NInput, NRadioGroup, NSpace, NRadio, NEmpty } from 'naive-ui'
import AppLayout from '@/components/layout/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { AddOutline, CreateOutline, CloseOutline } from '@vicons/ionicons5'

const showModal = ref(false)
const editingUser = ref<any>(null)

const formValue = ref({
  username: '',
  name: '',
  role: 'user',
  password: ''
})

const users = ref([
  { id: 1, username: 'admin', name: '管理员', role: 'admin', status: 'enabled' },
  { id: 2, username: 'zhangsan', name: '张三', role: 'user', status: 'enabled' },
  { id: 3, username: 'lisi', name: '李四', role: 'user', status: 'enabled' }
])

const columns = [
  { title: '用户名', key: 'username' },
  { title: '姓名', key: 'name' },
  {
    title: '角色',
    key: 'role',
    render(row) {
      return h(NTag, { type: row.role === 'admin' ? 'error' : 'info', size: 'small' }, () => row.role === 'admin' ? '管理员' : '用户')
    }
  },
  {
    title: '状态',
    key: 'status',
    render(row) {
      return h(NTag, { type: row.status === 'enabled' ? 'success' : 'warning', size: 'small' }, () => row.status === 'enabled' ? '启用' : '禁用')
    }
  },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      return h('div', { class: 'action-buttons' }, [
        h(NButton, { quaternary: true, size: 'small', onClick: () => editUser(row) }, () => h(NIcon, null, { default: () => h(CreateOutline) })),
        h(NButton, { quaternary: true, size: 'small', type: 'error', onClick: () => toggleStatus(row) }, () => row.status === 'enabled' ? '禁用' : '启用')
      ])
    }
  }
]

const editUser = (user: any) => {
  editingUser.value = user
  formValue.value = { ...user, password: '' }
  showModal.value = true
}

const toggleStatus = (user: any) => {
  user.status = user.status === 'enabled' ? 'disabled' : 'enabled'
}

const saveUser = () => {
  showModal.value = false
  editingUser.value = null
}
</script>

<style scoped lang="scss">
.user-management-page {
  max-width: 900px;
  margin: 0 auto;
}

.action-buttons {
  display: flex;
  gap: 4px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;

  &.active {
    opacity: 1;
    pointer-events: auto;
  }
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gray-200);

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }
}

.modal-body {
  padding: 20px;
}

.form-item {
  margin-bottom: 16px;

  label {
    display: block;
    font-size: 14px;
    color: var(--gray-600);
    margin-bottom: 8px;
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--gray-200);
  background: var(--gray-100);
}
</style>
