<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 60 60" fill="none">
            <defs>
              <linearGradient id="shieldGradLogin" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#1E5AA8" />
                <stop offset="100%" style="stop-color:#2C7BE5" />
              </linearGradient>
            </defs>
            <path d="M30 4L8 12v15c0 14.25 9.4 27.1 22 31 12.6-3.9 22-16.75 22-31V12L30 4z" fill="url(#shieldGradLogin)" />
            <path d="M24 28l-4.5-4.5 2.1-2.1 2.4 2.4 8.4-8.4 2.1 2.1-10.5 10.5z" fill="#fff" />
            <circle cx="44" cy="18" r="9" fill="#faad14" />
            <path d="M41 18l2 2 4-4" stroke="#fff" stroke-width="2" fill="none" />
          </svg>
        </div>
        <h1 class="title">智能招投标审查平台</h1>
        <p class="subtitle">AI 驱动的招投标文档智能审查系统</p>
      </div>

      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        @submit.prevent="handleLogin"
      >
        <n-form-item path="username" label="用户名">
          <n-input
            v-model:value="formValue.username"
            placeholder="请输入用户名"
            size="large"
          />
        </n-form-item>

        <n-form-item path="password" label="密码">
          <n-input
            v-model:value="formValue.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password-on="click"
          />
        </n-form-item>

        <n-form-item>
          <n-button
            type="primary"
            size="large"
            block
            :loading="loading"
            @click="handleLogin"
          >
            登 录
          </n-button>
        </n-form-item>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NForm, NFormItem, NInput, NButton, useMessage } from 'naive-ui'
import type { FormInst } from 'naive-ui'

const router = useRouter()
const message = useMessage()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const formValue = ref({
  username: '',
  password: ''
})

const rules = {
  username: {
    required: true,
    message: '请输入用户名',
    trigger: 'blur'
  },
  password: {
    required: true,
    message: '请输入密码',
    trigger: 'blur'
  }
}

const handleLogin = () => {
  formRef.value?.validate((errors) => {
    if (errors) return

    loading.value = true

    // Simulate login
    setTimeout(() => {
      loading.value = false
      message.success('登录成功')
      router.push('/home')
    }, 1000)
  })
}
</script>

<style scoped lang="scss">
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1E5AA8 0%, #2C7BE5 50%, #1E5AA8 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 48px 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.logo-icon {
  width: 72px;
  height: 72px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-800);
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: var(--gray-500);
}
</style>
