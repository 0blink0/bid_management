import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const userInfo = ref<{
    id: string
    name: string
    email?: string
    role?: string
  } | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('auth_token', newToken)
  }

  const setUser = (user: typeof userInfo.value) => {
    userInfo.value = user
  }

  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('auth_token')
  }

  return {
    token,
    userInfo,
    isAuthenticated,
    setToken,
    setUser,
    logout
  }
})
