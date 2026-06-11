<template>
  <q-page class="finance-wrapper-page">
    <div class="nav-strip-card">
      <div class="nav-strip-header">
        <div>
          <div class="nav-strip-title">财务管理</div>
          <div class="nav-strip-desc">统一承载考核、对账、收付款、报销、借支与资金流水等财务业务模块。</div>
        </div>
      </div>
    </div>

    <div class="biz-content">
      <router-view />
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'PageFinanceCenter'
}
</script>

<style scoped>
.finance-wrapper-page {
  padding: 4px;
}

.nav-strip-card {
  padding: 12px 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 10px 26px rgba(32, 62, 103, 0.08);
}

.nav-strip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-strip-title {
  font-size: 16px;
  font-weight: 700;
  color: #173056;
}

.nav-strip-desc {
  margin-top: 4px;
  font-size: 12px;
  color: #73829b;
}

.biz-content {
  margin-top: 12px;
}
</style>
