<template>
  <header class="topbar">
    <div class="topbar-logo">
      <svg viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg" width="40" height="40">
        <defs>
          <linearGradient id="shieldMain" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1E5AA8"/>
            <stop offset="50%" stop-color="#2C7BE5"/>
            <stop offset="100%" stop-color="#1E5AA8"/>
          </linearGradient>
          <linearGradient id="goldBadge" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
          </linearGradient>
          <filter id="shieldShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#1E5AA8" flood-opacity="0.3"/>
          </filter>
          <filter id="badgeShadow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#000" flood-opacity="0.25"/>
          </filter>
        </defs>
        <g filter="url(#shieldShadow)">
          <path d="M22 2L4 9v10c0 10 8 17 18 17s18-7 18-17V9L22 2z" fill="url(#shieldMain)"/>
        </g>
        <path d="M22 2L4 9v10c0 10 8 17 18 17" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
        <path d="M22 36c8.5 0 15-5.5 16-13" fill="none" stroke="rgba(0,0,0,0.15)" stroke-width="1.5"/>
        <path d="M22 2L4 9v10c0 10 8 17 18 17s18-7 18-17V9L22 2z" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
        <g transform="translate(14, 11)">
          <path d="M12 0H4a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V6l-4-6z" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 0v6h4" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M5 10h6M5 13h4" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </g>
        <g filter="url(#badgeShadow)" transform="translate(28, 26)">
          <circle cx="8" cy="8" r="7" fill="url(#goldBadge)" stroke="#B8860B" stroke-width="0.5"/>
          <circle cx="8" cy="8" r="5.5" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
          <path d="M5 8l2 2 4-4" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
      </svg>
      <span class="topbar-title">智能招投标审查平台</span>
    </div>
    <div class="topbar-actions">
      <div class="topbar-user-dropdown">
        <div class="topbar-user">
          <div class="topbar-user-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <span class="topbar-user-name">张三</span>
          <svg class="topbar-user-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--topbar-height);
  background: linear-gradient(135deg, var(--primary-color) 0%, #144a82 100%);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 24px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.topbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.topbar-title {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 2px;
  white-space: nowrap;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.topbar-user-dropdown {
  position: relative;
}

.topbar-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
}

.topbar-user-avatar {
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 18px;
    height: 18px;
  }
}

.topbar-user-name {
  font-size: 14px;
  color: white;
}

.topbar-user-arrow {
  width: 16px;
  height: 16px;
  opacity: 0.8;
}
</style>
