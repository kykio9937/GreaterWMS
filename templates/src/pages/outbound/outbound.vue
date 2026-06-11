<template>
  <q-page class="biz-page">
    <div class="outbound-shell">
      <div class="main-table biz-content">
        <router-view />
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Pageoutbound'
}
</script>

<style scoped>
.biz-page {
  padding: 0;
}

.outbound-shell {
  overflow: hidden;
  border-radius: 8px;
  background: transparent;
  box-shadow: none;
}

.biz-content {
  margin-top: 0;
}
</style>
