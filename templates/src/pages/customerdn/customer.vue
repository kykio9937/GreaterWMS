<template>
  <q-page class="finance-page">
    <div class="nav-strip-card">
      <div class="nav-strip-header">
        <div>
          <div class="nav-strip-title">财务管理</div>
          <div class="nav-strip-desc">围绕上游对账、客户汇总和客户明细，集中查看应收应付与运输费用。</div>
        </div>
        <q-btn
          flat
          round
          dense
          color="primary"
          :icon="navExpanded ? 'expand_less' : 'expand_more'"
          @click="navExpanded = !navExpanded"
        />
      </div>

      <q-slide-transition>
        <div v-show="navExpanded" class="nav-strip-body">
          <q-tabs
            v-model="detaillink"
            inline-label
            active-color="primary"
            indicator-color="transparent"
            class="compact-tabs"
          >
            <q-route-tab
              v-for="item in tabs"
              :key="item.name"
              v-bind="item"
              class="compact-route-tab"
              exact
            />
          </q-tabs>
        </div>
      </q-slide-transition>
    </div>

    <div class="biz-content">
      <router-view />
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Pagecustomerdn',
  data () {
    return {
      detaillink: this.$route.name || 'customerdnlist',
      navExpanded: true,
      tabs: [
        { name: 'customerdnlist', label: '客户汇总', icon: 'summarize', to: { name: 'customerdnlist' } },
        { name: 'customerpod', label: '客户明细', icon: 'article', to: { name: 'customerpod' } }
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
.finance-page {
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
  gap: 16px;
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

.nav-strip-body {
  margin-top: 10px;
}

.compact-tabs {
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 8px;
}

.compact-route-tab {
  min-height: 34px;
  margin-right: 8px;
  margin-bottom: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f3f6fb;
  color: #607089;
  font-size: 12px;
}

.compact-route-tab.q-tab--active {
  background: linear-gradient(135deg, #4f2bd8 0%, #6a3ff1 100%);
  color: #fff;
  box-shadow: 0 8px 20px rgba(79, 43, 216, 0.22);
}

.biz-content {
  margin-top: 12px;
}
</style>
