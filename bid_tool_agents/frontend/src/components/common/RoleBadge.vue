<template>
  <span :class="['role-badge', `role-${type}`]">
    {{ roleText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type RoleType = 'admin' | 'reviewer' | 'viewer' | 'user'

const props = defineProps<{
  type: RoleType
}>()

const roleText = computed(() => {
  const textMap: Record<RoleType, string> = {
    admin: '管理员',
    reviewer: '审查员',
    viewer: '查看者',
    user: '用户'
  }
  return textMap[props.type] || props.type
})
</script>

<style scoped lang="scss">
.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.role-admin {
  background-color: rgba(255, 77, 79, 0.1);
  color: var(--danger-color);
}

.role-reviewer {
  background-color: var(--purple-bg);
  color: var(--purple-color);
}

.role-viewer {
  background-color: var(--success-bg);
  color: var(--success-color);
}

.role-user {
  background-color: var(--gray-200);
  color: var(--gray-600);
}
</style>
