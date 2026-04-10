import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/pages/Home.vue')
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('@/pages/Upload.vue')
  },
  {
    path: '/document-parser',
    name: 'DocumentParser',
    component: () => import('@/pages/DocumentParser.vue')
  },
  {
    path: '/compliance-review',
    name: 'ComplianceReview',
    component: () => import('@/pages/ComplianceReview.vue')
  },
  {
    path: '/comparison',
    name: 'Comparison',
    component: () => import('@/pages/Comparison.vue')
  },
  {
    path: '/qualification-verify',
    name: 'QualificationVerify',
    component: () => import('@/pages/QualificationVerify.vue')
  },
  {
    path: '/risk-detection',
    name: 'RiskDetection',
    component: () => import('@/pages/RiskDetection.vue')
  },
  {
    path: '/evaluation-assist',
    name: 'EvaluationAssist',
    component: () => import('@/pages/EvaluationAssist.vue')
  },
  {
    path: '/expert-selection',
    name: 'ExpertSelection',
    component: () => import('@/pages/ExpertSelection.vue')
  },
  {
    path: '/archive-management',
    name: 'ArchiveManagement',
    component: () => import('@/pages/ArchiveManagement.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/pages/Statistics.vue')
  },
  {
    path: '/knowledge-base',
    name: 'KnowledgeBase',
    component: () => import('@/pages/KnowledgeBase.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/pages/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
