<template>
  <q-page class="workbench-page">
    <div class="workbench-hero">
      <div>
        <div class="hero-eyebrow">{{ isAuthed ? '物流运营工作台' : '物流业务入口' }}</div>
        <div class="hero-title">{{ isAuthed ? '欢迎进入 GreaterWMS 中国化物流后台' : '登录后进入物流业务作业区' }}</div>
        <div class="hero-subtitle">
          {{ isAuthed ? '围绕订单、仓储、司机、库存和基础资料，集中处理日常作业与业务协同。' : '支持手机号验证码登录、密码登录和注册，登录后可直接进入运单、在途、财务等业务模块。' }}
        </div>
        <div v-if="!isAuthed" class="hero-cta-row">
          <q-btn unelevated color="primary" label="手机号登录" @click="openLogin" />
          <q-btn flat color="white" label="注册账号" @click="openRegister" />
        </div>
      </div>
      <div class="hero-side">
        <div class="hero-badge">今日状态</div>
        <div class="hero-date">{{ currentDate }}</div>
        <div class="hero-meta">
          <span>{{ warehouseName || '未选择仓库' }}</span>
          <span>{{ loginName || '未登录用户' }}</span>
        </div>
      </div>
    </div>

    <div class="kpi-grid">
      <div v-for="card in kpiCards" :key="card.title" class="kpi-card">
        <div class="kpi-label">{{ card.title }}</div>
        <div class="kpi-value">{{ card.value }}</div>
        <div class="kpi-foot">
          <span>{{ card.tip }}</span>
          <span :class="card.trendClass">{{ card.trend }}</span>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <div class="panel panel-wide">
        <div class="panel-head">
          <div>
            <div class="panel-title">快捷入口</div>
            <div class="panel-desc">常用模块一键直达，更贴近国内物流平台后台的操作习惯</div>
          </div>
        </div>
        <div class="quick-grid">
          <div
            v-for="item in quickLinks"
            :key="item.title"
            class="quick-card"
            @click="goPage(item.routeName, item.menuKey)"
          >
            <q-icon :name="item.icon" size="28px" class="quick-icon" />
            <div class="quick-title">{{ item.title }}</div>
            <div class="quick-desc">{{ item.desc }}</div>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-title">待办提醒</div>
            <div class="panel-desc">建议优先处理的关键作业</div>
          </div>
        </div>
        <div class="todo-list">
          <div v-for="item in todoList" :key="item.title" class="todo-item">
            <div class="todo-main">
              <div class="todo-title">{{ item.title }}</div>
              <div class="todo-desc">{{ item.desc }}</div>
            </div>
            <div class="todo-tag">{{ item.tag }}</div>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-title">运营看板</div>
            <div class="panel-desc">按运输与仓储两个视角快速掌握节奏</div>
          </div>
        </div>
        <div class="board-list">
          <div v-for="item in boardStats" :key="item.label" class="board-item">
            <div class="board-label">{{ item.label }}</div>
            <div class="board-track">
              <div class="board-bar" :style="{ width: item.percent + '%' }"></div>
            </div>
            <div class="board-value">{{ item.value }}</div>
          </div>
        </div>
      </div>

      <div class="panel panel-wide">
        <div class="panel-head">
          <div>
            <div class="panel-title">业务播报</div>
            <div class="panel-desc">用于承接通知、异常和班次说明</div>
          </div>
        </div>
        <div class="notice-list">
          <div v-for="notice in notices" :key="notice.title" class="notice-item">
            <div class="notice-dot"></div>
            <div>
              <div class="notice-title">{{ notice.title }}</div>
              <div class="notice-desc">{{ notice.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { database } from '../db/database'
import { LocalStorage } from 'quasar'
import Bus from 'boot/bus.js'

export default {
  name: 'PageIndex',
  data () {
    return {
      cleardata: [],
      currentDate: '',
      kpiCards: [
        { title: '今日入库单', value: '128', tip: '较昨日', trend: '+12%', trendClass: 'up' },
        { title: '今日出库单', value: '96', tip: '准时发运率', trend: '98.6%', trendClass: 'up' },
        { title: '在库 SKU', value: '2,486', tip: '库存准确率', trend: '99.2%', trendClass: 'up' },
        { title: '待处理异常', value: '7', tip: '需人工跟进', trend: '优先处理', trendClass: 'warn' }
      ],
      quickLinks: [
        { title: '运输订单中心', desc: '查看出库、发运、签收进度', routeName: 'dn', menuKey: 'outbound', icon: 'local_shipping' },
        { title: '入库作业中心', desc: '处理到货、卸货、分拣与异常', routeName: 'asn', menuKey: 'inbound', icon: 'inventory_2' },
        { title: '库存台账', desc: '查看库存明细、库位与盘点', routeName: 'stocklist', menuKey: 'stock', icon: 'stacked_line_chart' },
        { title: '司机与调度', desc: '维护司机、车辆和派车任务', routeName: 'driverlist', menuKey: 'driver', icon: 'person_pin_circle' },
        { title: '客户订单', desc: '聚焦客户侧运单与签收信息', routeName: 'customerdnlist', menuKey: 'customerdn', icon: 'receipt_long' },
        { title: '供应协同', desc: '跟进入库预约与供应商到货', routeName: 'supplierasnlist', menuKey: 'supplierasn', icon: 'warehouse' }
      ],
      todoList: [
        { title: '待分拣入库任务', desc: '建议优先处理今日已到货但未分配库位的单据', tag: '高优先级' },
        { title: '司机证照即将到期', desc: '检查司机档案并安排续期提醒', tag: '48小时内' },
        { title: '客户签收回单待确认', desc: '核对 POD 状态，避免对账延迟', tag: '待确认' },
        { title: '库存差异待复盘', desc: '关注循环盘点异常与移库记录', tag: '异常' }
      ],
      boardStats: [
        { label: '出库及时率', value: '96%', percent: 96 },
        { label: '入库完成率', value: '88%', percent: 88 },
        { label: '库存准确率', value: '99%', percent: 99 },
        { label: '司机在线率', value: '74%', percent: 74 }
      ],
      notices: [
        { title: '班次提醒', desc: '夜班请在 18:00 前确认待发运订单与承运司机安排。' },
        { title: '系统建议', desc: '可优先从“运输订单中心”和“库存台账”作为主作业入口。' },
        { title: '数据维护', desc: '客户、供应商、商品资料建议统一在主数据模块集中维护。' }
      ]
    }
  },
  computed: {
    warehouseName () {
      return LocalStorage.getItem('warehouse_name')
    },
    loginName () {
      return LocalStorage.getItem('login_name')
    },
    isAuthed () {
      return LocalStorage.has('auth')
    }
  },
  created () {
    LocalStorage.set('menulink', '')
    this.currentDate = this.formatDate(new Date())
  },
  mounted () {
    var page = database.getInstance().get().test
    page.toArray().then(res => {
      if (res.length > 0) {
        this.cleardata = []
        page.each(result => {
          this.cleardata.push(result.id)
        })
        page.bulkDelete(this.cleardata)
        this.cleardata = []
      } else {
        page.add({
          id: 1,
          test: 'next'
        })
      }
    })
  },
  methods: {
    formatDate (date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    openLogin () {
      Bus.$emit('openLoginDialog')
    },
    openRegister () {
      Bus.$emit('openRegisterDialog')
    },
    goPage (routeName, menuKey) {
      LocalStorage.set('menulink', menuKey)
      this.$router.push({ name: routeName })
    }
  }
}
</script>

<style scoped>
.workbench-page {
  min-height: 100%;
  padding: 4px;
  background:
    radial-gradient(circle at top right, rgba(32, 86, 201, 0.14), transparent 22%),
    linear-gradient(180deg, #f4f7fb 0%, #eef3f8 100%);
}

.landing-hero {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr;
  gap: 18px;
  margin-bottom: 18px;
  padding: 28px 30px;
  border-radius: 28px;
  background:
    radial-gradient(circle at top right, rgba(255, 193, 7, 0.18), transparent 26%),
    linear-gradient(135deg, #fffdf8 0%, #f8fbff 56%, #eef5ff 100%);
  border: 1px solid #e8eef9;
  box-shadow: 0 18px 50px rgba(32, 62, 103, 0.08);
}

.landing-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 999px;
  background: #fff1d6;
  color: #9a5b00;
  font-size: 12px;
  font-weight: 700;
}

.landing-title {
  margin-top: 14px;
  font-size: 36px;
  line-height: 1.2;
  font-weight: 800;
  color: #18253d;
}

.landing-subtitle {
  margin-top: 14px;
  max-width: 720px;
  font-size: 15px;
  line-height: 1.9;
  color: #61718b;
}

.landing-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.landing-primary-btn,
.landing-ghost-btn,
.landing-outline-btn {
  min-height: 44px;
  padding: 0 18px;
  border-radius: 999px;
}

.landing-primary-btn {
  box-shadow: 0 14px 30px rgba(222, 91, 18, 0.24);
}

.landing-ghost-btn {
  background: rgba(31, 99, 197, 0.08);
}

.landing-hint {
  margin-top: 14px;
  font-size: 12px;
  color: #7b879d;
}

.landing-side {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.landing-side-card {
  padding: 20px;
  border-radius: 22px;
  background: linear-gradient(135deg, #12345f 0%, #1c5ea7 100%);
  color: #fff;
  box-shadow: 0 18px 40px rgba(18, 52, 95, 0.16);
}

.landing-side-card--light {
  background: linear-gradient(180deg, #ffffff 0%, #f5f8fe 100%);
  color: #20304b;
  border: 1px solid #e4ebf8;
  box-shadow: none;
}

.landing-side-title {
  font-size: 15px;
  font-weight: 700;
}

.landing-flow {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.flow-chip {
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  font-size: 12px;
}

.landing-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 14px;
}

.landing-metric {
  padding: 14px 12px;
  border-radius: 16px;
  background: #f6f9ff;
}

.landing-metric-value {
  font-size: 22px;
  font-weight: 800;
  color: #1a3f75;
}

.landing-metric-label {
  margin-top: 6px;
  font-size: 12px;
  color: #6f7f98;
}

.workbench-hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 28px 30px;
  border-radius: 24px;
  background: linear-gradient(135deg, #0f3d75 0%, #1657a2 52%, #2d7bd8 100%);
  color: #fff;
  box-shadow: 0 18px 50px rgba(15, 61, 117, 0.18);
}

.hero-cta-row {
  display: flex;
  gap: 10px;
  margin-top: 18px;
}

.hero-eyebrow {
  font-size: 13px;
  letter-spacing: 2px;
  opacity: 0.75;
}

.hero-title {
  margin-top: 10px;
  font-size: 30px;
  font-weight: 700;
  line-height: 1.3;
}

.hero-subtitle {
  margin-top: 12px;
  max-width: 640px;
  font-size: 14px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.82);
}

.hero-side {
  min-width: 220px;
  padding: 18px 20px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
}

.hero-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  font-size: 12px;
}

.hero-date {
  margin-top: 16px;
  font-size: 24px;
  font-weight: 700;
}

.hero-meta {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.kpi-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.kpi-card,
.panel {
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 12px 34px rgba(32, 62, 103, 0.08);
}

.kpi-card {
  padding: 22px 22px 18px;
}

.kpi-label {
  font-size: 13px;
  color: #6b7a90;
}

.kpi-value {
  margin-top: 10px;
  font-size: 34px;
  font-weight: 700;
  color: #16263f;
}

.kpi-foot {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #7b8aa3;
}

.up {
  color: #16a34a;
}

.warn {
  color: #ea580c;
}

.content-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 16px;
}

.panel-wide {
  grid-column: span 2;
}

.panel {
  padding: 22px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.panel-title {
  font-size: 18px;
  font-weight: 700;
  color: #1d2d4a;
}

.panel-desc {
  margin-top: 6px;
  font-size: 12px;
  color: #7e8aa1;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.quick-card {
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%);
  border: 1px solid #e1ebf8;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.quick-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(31, 71, 128, 0.12);
}

.quick-icon {
  color: #1e63c5;
}

.quick-title {
  margin-top: 12px;
  font-size: 16px;
  font-weight: 700;
  color: #1f2f49;
}

.quick-desc {
  margin-top: 8px;
  font-size: 12px;
  line-height: 1.7;
  color: #718099;
}

.todo-list,
.notice-list,
.board-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item,
.notice-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 16px;
  background: #f7f9fc;
}

.todo-title,
.notice-title {
  font-size: 14px;
  font-weight: 700;
  color: #20304b;
}

.todo-desc,
.notice-desc {
  margin-top: 6px;
  font-size: 12px;
  line-height: 1.7;
  color: #73819a;
}

.todo-tag {
  flex-shrink: 0;
  padding: 5px 10px;
  border-radius: 999px;
  background: #e6efff;
  color: #1d5fcc;
  font-size: 12px;
}

.board-item {
  display: grid;
  grid-template-columns: 88px 1fr 52px;
  gap: 10px;
  align-items: center;
}

.board-label,
.board-value {
  font-size: 13px;
  color: #44546d;
}

.board-track {
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
  background: #e8eef6;
}

.board-bar {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1b5fc7 0%, #3ca0ff 100%);
}

.notice-item {
  justify-content: flex-start;
}

.notice-dot {
  width: 10px;
  height: 10px;
  margin-top: 6px;
  border-radius: 50%;
  background: #1f72e5;
  box-shadow: 0 0 0 4px rgba(31, 114, 229, 0.12);
}

@media (max-width: 1200px) {
  .landing-hero,
  .kpi-grid,
  .quick-grid,
  .content-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .panel-wide {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .landing-hero,
  .kpi-grid,
  .quick-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .workbench-hero {
    flex-direction: column;
    padding: 22px;
  }

  .hero-title {
    font-size: 24px;
  }

  .landing-title {
    font-size: 28px;
  }

  .landing-metrics,
  .hero-cta-row {
    grid-template-columns: 1fr;
    flex-direction: column;
  }

  .hero-side,
  .panel-wide {
    min-width: 0;
    grid-column: span 1;
  }
}
</style>
