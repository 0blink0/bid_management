import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workspace/new',
    name: 'WorkspaceNew',
    component: () => import('@/pages/WorkspaceNew.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workspace/progress',
    name: 'WorkspaceProgress',
    component: () => import('@/pages/WorkspaceProgress.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workspace/processing',
    name: 'WorkspaceProcessing',
    component: () => import('@/pages/WorkspaceProcessing.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/pages/Reports.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id',
    name: 'ReportDetail',
    component: () => import('@/pages/ReportDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id/chat',
    name: 'ReportChat',
    component: () => import('@/pages/ReportChat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id/full',
    name: 'ReportFull',
    component: () => import('@/pages/ReportFull.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pdf/:id',
    name: 'PdfPreview',
    component: () => import('@/pages/PdfPreview.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('@/pages/Upload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/document-parser',
    name: 'DocumentParser',
    component: () => import('@/pages/DocumentParser.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/compliance-review',
    name: 'ComplianceReview',
    component: () => import('@/pages/ComplianceReview.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/comparison',
    name: 'Comparison',
    component: () => import('@/pages/Comparison.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/qualification-verify',
    name: 'QualificationVerify',
    component: () => import('@/pages/QualificationVerify.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/qualification/:id',
    name: 'QualificationCheck',
    component: () => import('@/pages/QualificationCheck.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/risk-detection',
    name: 'RiskDetection',
    component: () => import('@/pages/RiskDetection.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/evaluation-assist',
    name: 'EvaluationAssist',
    component: () => import('@/pages/EvaluationAssist.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/expert-selection',
    name: 'ExpertSelection',
    component: () => import('@/pages/ExpertSelection.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/archive-management',
    name: 'ArchiveManagement',
    component: () => import('@/pages/ArchiveManagement.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/pages/Statistics.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/knowledge-base',
    name: 'KnowledgeBase',
    component: () => import('@/pages/KnowledgeBase.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/pages/Admin.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: () => import('@/pages/UserManagement.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/projects',
    name: 'ProjectList',
    component: () => import('@/pages/ProjectList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/project/:id',
    name: 'ProjectDetail',
    component: () => import('@/pages/ProjectDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/responses',
    name: 'ResponseList',
    component: () => import('@/pages/ResponseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/pages/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    // Redirect to login if not authenticated
    next('/login')
  } else if (to.path === '/login' && userStore.isAuthenticated) {
    // Redirect to home if already authenticated
    next('/home')
  } else {
    next()
  }
})

export default router
