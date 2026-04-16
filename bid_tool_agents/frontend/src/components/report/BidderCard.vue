<template>
  <div class="bidder-card">
    <div class="card-header">
      <div class="company-info">
        <n-icon :size="24" class="company-icon">
          <BusinessOutline />
        </n-icon>
        <div class="company-text">
          <h3 class="company-name">{{ bidder.name }}</h3>
          <span class="company-type">{{ bidder.type || '企业' }}</span>
        </div>
      </div>

      <StatusBadge
        v-if="bidder.status"
        :status="getStatusType(bidder.status)"
        :text="getStatusText(bidder.status)"
      />
    </div>

    <div class="card-body">
      <div class="info-grid">
        <div class="info-item" v-if="bidder.unifiedSocialCreditCode">
          <label>统一社会信用代码</label>
          <span class="info-value code">{{ bidder.unifiedSocialCreditCode }}</span>
        </div>

        <div class="info-item" v-if="bidder.legalRepresentative">
          <label>法定代表人</label>
          <span class="info-value">{{ bidder.legalRepresentative }}</span>
        </div>

        <div class="info-item" v-if="bidder.contactPerson">
          <label>联系人</label>
          <span class="info-value">{{ bidder.contactPerson }}</span>
        </div>

        <div class="info-item" v-if="bidder.contactPhone">
          <label>联系电话</label>
          <span class="info-value phone">{{ bidder.contactPhone }}</span>
        </div>

        <div class="info-item" v-if="bidder.registeredCapital">
          <label>注册资本</label>
          <span class="info-value">{{ formatCapital(bidder.registeredCapital) }}</span>
        </div>

        <div class="info-item" v-if="bidder.establishedDate">
          <label>成立日期</label>
          <span class="info-value">{{ formatDate(bidder.establishedDate) }}</span>
        </div>
      </div>

      <div class="qualifications" v-if="bidder.qualifications?.length">
        <h4>资质证书</h4>
        <div class="qualification-tags">
          <n-tag
            v-for="qual in bidder.qualifications"
            :key="qual.id || qual.name"
            size="small"
          >
            {{ qual.name }}
          </n-tag>
        </div>
      </div>

      <div class="address" v-if="bidder.address">
        <label>
          <n-icon :size="14"><LocationOutline /></n-icon>
          地址
        </label>
        <p>{{ bidder.address }}</p>
      </div>
    </div>

    <div class="card-footer" v-if="showActions">
      <n-button size="small" @click="$emit('view-detail', bidder)">
        查看详情
      </n-button>
      <n-button size="small" type="primary" @click="$emit('verify', bidder)">
        核验资质
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NIcon, NTag, NButton } from 'naive-ui'
import { BusinessOutline, LocationOutline } from '@vicons/ionicons5'
import StatusBadge from '../common/StatusBadge.vue'

export interface BidderQualification {
  id?: string
  name: string
  level?: string
  validUntil?: string
}

export interface Bidder {
  id?: string
  name: string
  type?: string
  status?: 'valid' | 'warning' | 'invalid' | 'pending'
  unifiedSocialCreditCode?: string
  legalRepresentative?: string
  contactPerson?: string
  contactPhone?: string
  registeredCapital?: number | string
  establishedDate?: string
  address?: string
  qualifications?: BidderQualification[]
}

const props = withDefaults(defineProps<{
  bidder: Bidder
  showActions?: boolean
}>(), {
  showActions: true
})

defineEmits<{
  'view-detail': [bidder: Bidder]
  'verify': [bidder: Bidder]
}>()

const getStatusType = (status: string): 'success' | 'warning' | 'danger' | 'default' => {
  const typeMap = {
    valid: 'success',
    warning: 'warning',
    invalid: 'danger',
    pending: 'default'
  }
  return typeMap[status] || 'default'
}

const getStatusText = (status: string): string => {
  const textMap = {
    valid: '有效',
    warning: '异常',
    invalid: '无效',
    pending: '待核验'
  }
  return textMap[status] || status
}

const formatCapital = (capital: number | string): string => {
  if (typeof capital === 'string') return capital
  if (capital >= 10000) {
    return `${(capital / 10000).toFixed(2)}万元`
  }
  return `${capital}万元`
}

const formatDate = (dateStr: string): string => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped lang="scss">
.bidder-card {
  background: #fff;
  border-radius: $radius-lg;
  border: 1px solid $gray-200;
  overflow: hidden;
  transition: box-shadow $transition-base;

  &:hover {
    box-shadow: $shadow-md;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg $spacing-xl;
  border-bottom: 1px solid $gray-200;
  background: $gray-100;
}

.company-info {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.company-icon {
  color: $primary-color;
}

.company-text {
  .company-name {
    margin: 0;
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
    color: $gray-800;
  }

  .company-type {
    font-size: $font-size-xs;
    color: $gray-500;
  }
}

.card-body {
  padding: $spacing-lg $spacing-xl;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-lg;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;

  label {
    font-size: $font-size-xs;
    color: $gray-500;
  }

  .info-value {
    font-size: $font-size-sm;
    color: $gray-800;

    &.code {
      font-family: monospace;
      letter-spacing: 1px;
    }

    &.phone {
      font-family: monospace;
    }
  }
}

.qualifications {
  margin-top: $spacing-lg;
  padding-top: $spacing-lg;
  border-top: 1px solid $gray-200;

  h4 {
    margin: 0 0 $spacing-sm 0;
    font-size: $font-size-xs;
    font-weight: $font-weight-semibold;
    color: $gray-500;
    text-transform: uppercase;
  }
}

.qualification-tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-xs;
}

.address {
  margin-top: $spacing-lg;
  padding-top: $spacing-lg;
  border-top: 1px solid $gray-200;

  label {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    font-size: $font-size-xs;
    color: $gray-500;
    margin-bottom: $spacing-xs;
  }

  p {
    margin: 0;
    font-size: $font-size-sm;
    color: $gray-700;
    line-height: 1.5;
  }
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-sm;
  padding: $spacing-md $spacing-xl;
  background: $gray-100;
  border-top: 1px solid $gray-200;
}
</style>
