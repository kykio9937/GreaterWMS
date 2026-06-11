<template>
  <q-page class="biz-page">
    <div class="outbound-shell">
      <div class="section-tabs">
        <q-tabs
          v-model="detaillink"
          inline-label
          active-color="primary"
          indicator-color="transparent"
          class="section-tabs-inner"
        >
          <q-route-tab
            v-for="item in tabs"
            :key="item.name"
            v-bind="item"
            class="section-route-tab"
            exact
          />
        </q-tabs>
      </div>

      <div class="main-table biz-content">
        <router-view />
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Pageoutbound',
  data () {
    return {
      detaillink: this.$route.name || 'dn',
      tabs: [
        { name: 'dn', label: '全部', to: { name: 'dn' } },
        { name: 'freshorder', label: '计划运单', to: { name: 'freshorder' } },
        { name: 'neworder', label: '待受理', to: { name: 'neworder' } },
        { name: 'pickstock', label: '已受理', to: { name: 'pickstock' } },
        { name: 'shippedstock', label: '运输中', to: { name: 'shippedstock' } },
        { name: 'pod', label: '已完成', to: { name: 'pod' } },
        { name: 'backorder', label: '作废记录', to: { name: 'backorder' } }
      ]
    }
  },
  watch: {
    '$route.name' (value) {
      this.detaillink = value
    }
  }
}
</script>

<style scoped>
.biz-page {
  padding: 0;
}

.outbound-shell {
  overflow: hidden;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 10px 24px rgba(33, 42, 79, 0.06);
}

.section-tabs {
  border-bottom: 1px solid #d9d3ff;
  background: #fff;
}

.section-tabs-inner {
  min-height: 42px;
  padding: 0 10px;
}

.section-route-tab {
  min-height: 42px;
  padding: 0 20px;
  border-right: 1px solid #ebeef6;
  color: #5f6480;
  font-size: 13px;
}

.section-route-tab.q-tab--active {
  background: #fff;
  color: #4d34d2;
  box-shadow: inset 0 2px 0 #7b61ff;
}

.biz-content {
  margin-top: 0;
}
</style>
