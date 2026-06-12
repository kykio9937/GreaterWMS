<template>
  <q-page class="home-dashboard-page">
    <div class="page-shell">
      <div class="tab-header">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          type="button"
          :class="['header-tab', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <div v-if="activeTab === 'workbench'" class="dashboard-layout">
        <section class="main-column">
          <div class="section-card overview-card">
            <div class="section-head">
              <div class="section-title-wrap">
                <div class="section-title">运单状态</div>
                <button type="button" class="link-action" @click="refreshTransitData">刷新</button>
              </div>
              <div class="switch-group">
                <button
                  v-for="item in statusRangeOptions"
                  :key="item"
                  type="button"
                  :class="['switch-btn', { active: activeStatusRange === item }]"
                  @click="activeStatusRange = item"
                >
                  {{ item }}
                </button>
              </div>
            </div>

            <div class="status-grid">
              <div v-for="item in statusCards" :key="item.label" class="status-card">
                <div class="status-icon" :style="{ background: item.tint }">{{ item.short }}</div>
                <div class="status-content">
                  <div class="status-label">{{ item.label }}</div>
                  <div class="status-value">{{ item.value }}</div>
                  <div class="status-unit">单</div>
                </div>
              </div>
            </div>
          </div>

          <div class="section-card audit-card">
            <div class="section-head audit-head">
              <div class="section-title-wrap">
                <div class="section-title">审核中心</div>
                <button type="button" class="link-action" @click="refreshAuditRows">刷新</button>
              </div>
              <div class="switch-group">
                <button
                  v-for="item in auditRangeOptions"
                  :key="item"
                  type="button"
                  :class="['switch-btn', { active: activeAuditRange === item }]"
                  @click="activeAuditRange = item"
                >
                  {{ item }}
                </button>
              </div>
            </div>

            <div class="audit-tabs">
              <button
                v-for="tab in auditTabs"
                :key="tab.key"
                type="button"
                :class="['audit-tab', { active: activeAuditTab === tab.key }]"
                @click="activeAuditTab = tab.key"
              >
                {{ tab.label }}
              </button>
            </div>

            <div class="audit-summary-grid">
              <div
                v-for="item in auditSummaryCards"
                :key="item.key"
                :class="['audit-summary-card', { selected: activeAuditCategory === item.key }]"
                @click="activeAuditCategory = item.key"
              >
                <div class="summary-title">{{ item.title }}</div>
                <div class="summary-subtitle">{{ item.subtitle }}</div>
                <div class="summary-value">{{ item.value }}</div>
                <button
                  type="button"
                  class="summary-link"
                  @click.stop="openAuditList(item.key)"
                >
                  列表 >
                </button>
              </div>
            </div>

            <div class="table-block">
              <div class="table-head">
                <div class="table-title">{{ activeAuditConfig.tableTitle }}</div>
                <button
                  v-if="activeAuditConfig.routeName"
                  type="button"
                  class="table-link"
                  @click="goPage(activeAuditConfig.routeName, activeAuditConfig.menuKey)"
                >
                  查看全部
                </button>
              </div>
              <div class="table-wrap">
                <table class="audit-table">
                  <thead>
                    <tr>
                      <th>单据编号</th>
                      <th>审核状态</th>
                      <th>申请人</th>
                      <th>费用名称</th>
                      <th>金额</th>
                      <th>客户</th>
                      <th>项目</th>
                      <th>司机</th>
                      <th>车牌</th>
                      <th>申请时间</th>
                      <th>审核备注</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="row in visibleAuditRows"
                      :key="row.id"
                      class="table-row-clickable"
                      @click="openAuditRow(row)"
                    >
                      <td>{{ row.order_no }}</td>
                      <td>
                        <span :class="['table-badge', badgeClass(row.audit_status)]">
                          {{ row.audit_status }}
                        </span>
                      </td>
                      <td>{{ row.applicant }}</td>
                      <td>{{ row.fee_name }}</td>
                      <td>{{ row.amount }}</td>
                      <td>{{ row.customer }}</td>
                      <td>{{ row.project }}</td>
                      <td>{{ row.driver }}</td>
                      <td>{{ row.plate_number }}</td>
                      <td>{{ row.apply_time }}</td>
                      <td>{{ row.audit_remark }}</td>
                      <td>
                        <div class="table-actions">
                          <button
                            v-for="action in row.actions"
                            :key="action.label"
                            type="button"
                            class="text-action"
                            @click.stop="handleAuditAction(action, row)"
                          >
                            {{ action.label }}
                          </button>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="!visibleAuditRows.length">
                      <td colspan="12" class="empty-cell">暂无审核数据</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>

        <aside class="side-column">
          <div class="section-card shortcut-card">
            <div class="shortcut-head">
              <div class="section-title">常用功能</div>
              <div class="shortcut-hint">快速进入高频业务页面</div>
            </div>
            <div class="shortcut-grid">
              <button
                v-for="item in shortcutItems"
                :key="item.title"
                type="button"
                class="shortcut-btn"
                @click="goPage(item.routeName, item.menuKey)"
              >
                {{ item.title }}
              </button>
            </div>
          </div>

          <div class="section-card quick-panel-card">
            <div class="section-title">工作台说明</div>
            <p class="panel-note">
              首页分为工作台和业务流程两个入口。工作台更适合查看状态、处理审核和进入常用页面，业务流程更适合演示从创建运单到结算的完整链路。
            </p>
          </div>
        </aside>
      </div>

      <div v-else class="flow-layout">
        <div class="flow-banner">
          <div class="flow-banner-title">业务流程</div>
          <div class="flow-banner-desc">按照业务推进顺序查看从创建运单到签收结算的完整链路。</div>
        </div>

        <div class="flow-timeline">
          <div v-for="(group, groupIndex) in flowGroups" :key="group.title" class="flow-group">
            <div class="flow-group-title">{{ group.title }}</div>
            <div class="flow-step-grid">
              <div
                v-for="(step, index) in group.steps"
                :key="step.title"
                class="flow-step-card"
                @click="goPage(step.routeName, step.menuKey)"
              >
                <div class="step-index">{{ groupIndex + 1 }}-{{ index + 1 }}</div>
                <div class="step-title">{{ step.title }}</div>
                <div class="step-desc">{{ step.desc }}</div>
                <div class="step-route">进入模块 ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { getauth } from 'boot/axios_request'

const transportFeeMeta = (row) => {
  if (row && row.transportation_fee && typeof row.transportation_fee === 'object') {
    return row.transportation_fee
  }
  return {}
}

export default {
  name: 'PageIndex',
  data () {
    return {
      activeTab: 'workbench',
      activeStatusRange: '周',
      activeAuditRange: '近7天',
      activeAuditTab: 'pending',
      activeAuditCategory: 'waybill_review',
      rawTransitRows: [],
      rawAuditRows: [],
      tabs: [
        { key: 'workbench', label: '工作台' },
        { key: 'flow', label: '业务流程' }
      ],
      statusRangeOptions: ['日', '周', '月'],
      auditRangeOptions: ['近7天', '近30天', '近90天'],
      auditTabs: [
        { key: 'pending', label: '待我审核' },
        { key: 'mine', label: '我发起的' }
      ],
      shortcutItems: [
        { title: '运单列表', routeName: 'dn', menuKey: 'outbound' },
        { title: '运单修改记录', routeName: 'neworder', menuKey: 'outbound' },
        { title: '在途费用', routeName: 'dispatchlist', menuKey: 'driver' },
        { title: '在途费用明细', routeName: 'driverexpense', menuKey: 'finance' },
        { title: '收款单', routeName: 'receiptbill', menuKey: 'finance' },
        { title: '付款单', routeName: 'paybill', menuKey: 'finance' },
        { title: '司机报销单', routeName: 'driverCheck', menuKey: 'finance' },
        { title: '收支汇总', routeName: 'dailyincome', menuKey: 'finance' }
      ],
      auditCategoryMeta: {
        waybill_review: { tableTitle: '运单修改审核列表', routeName: 'freshorder', menuKey: 'outbound' },
        transit_fee: { tableTitle: '在途费用待审核列表', routeName: 'dispatchlist', menuKey: 'driver' },
        reimburse: { tableTitle: '报销单待审核列表', routeName: 'driverCheck', menuKey: 'finance' },
        receipt_order: { tableTitle: '收款单-订单待审核列表', routeName: 'receiptbill', menuKey: 'finance' },
        receipt_waybill: { tableTitle: '收款单-运单待审核列表', routeName: 'receiptbill', menuKey: 'finance' },
        pay_order: { tableTitle: '付款单待审核列表', routeName: 'paybill', menuKey: 'finance' },
        daily_io: { tableTitle: '日常收支待审核列表', routeName: 'dailyincome', menuKey: 'finance' },
        customer_check: { tableTitle: '客户考核待审核列表', routeName: 'customerAssessment', menuKey: 'finance' },
        carrier_check: { tableTitle: '运力考核待审核列表', routeName: 'capacityAssessment', menuKey: 'finance' },
        driver_borrow: { tableTitle: '司机借支待审核列表', routeName: 'borrowmanage', menuKey: 'finance' },
        vehicle_borrow: { tableTitle: '车辆借支待审核列表', routeName: 'borrowmanage', menuKey: 'finance' },
        staff_borrow: { tableTitle: '员工借支待审核列表', routeName: 'borrowmanage', menuKey: 'finance' }
      },
      flowGroups: [
        {
          title: '订单受理',
          steps: [
            { title: '创建运单', desc: '录入客户、线路、费用、车辆和司机信息。', routeName: 'createwaybill', menuKey: 'outbound' },
            { title: '运单列表', desc: '查看运单总表，跟踪审核、派单和状态变化。', routeName: 'dn', menuKey: 'outbound' },
            { title: '运单审核', desc: '对已创建运单进行审核通过或退回修改。', routeName: 'freshorder', menuKey: 'outbound' }
          ]
        },
        {
          title: '在途执行',
          steps: [
            { title: '在途管理', desc: '查看运输中运单、司机和车牌执行信息。', routeName: 'driverlist', menuKey: 'driver' },
            { title: '在途费用', desc: '跟踪司机借支、费用支出和运输成本。', routeName: 'dispatchlist', menuKey: 'driver' },
            { title: '签收回单', desc: '运单签收后回传回单与签收结果。', routeName: 'pod', menuKey: 'outbound' }
          ]
        },
        {
          title: '对账结算',
          steps: [
            { title: '收款单', desc: '管理客户应收与收款跟进。', routeName: 'receiptbill', menuKey: 'finance' },
            { title: '付款单', desc: '管理承运付款和日常支出。', routeName: 'paybill', menuKey: 'finance' },
            { title: '财务汇总', desc: '查看收支、流水和结算模块。', routeName: 'capitalflow', menuKey: 'finance' }
          ]
        }
      ]
    }
  },
  computed: {
    statusCards () {
      const rows = this.rawTransitRows
      const countByStatus = (matcher) => rows.filter(row => matcher(this.normalizeTransitStatus(row))).length
      return [
        { label: '待接单', value: countByStatus(status => status === '待接单' || status === '待审核'), short: '接', tint: '#7d58f2' },
        { label: '待签到', value: countByStatus(status => status === '待签到'), short: '到', tint: '#ffbe55' },
        { label: '待靠台', value: countByStatus(status => status === '待靠台'), short: '台', tint: '#ff8a47' },
        { label: '待发车', value: countByStatus(status => status === '待发车' || status === '已审核'), short: '发', tint: '#ffbd4a' },
        { label: '运输中', value: countByStatus(status => status === '运输中'), short: '运', tint: '#5ac486' }
      ]
    },
    auditSummaryCards () {
      const countPending = (category) => this.rawAuditRows.filter(item => item.category === category && item.audit_status === '待审核').length
      return [
        { key: 'waybill_review', title: '运单修改审核', subtitle: '待审核', value: countPending('waybill_review') },
        { key: 'transit_fee', title: '在途费用', subtitle: '待审核', value: countPending('transit_fee') },
        { key: 'reimburse', title: '报销单', subtitle: '待审核', value: countPending('reimburse') },
        { key: 'receipt_order', title: '收款单-订单', subtitle: '待审核', value: countPending('receipt_order') },
        { key: 'receipt_waybill', title: '收款单-运单', subtitle: '待审核', value: countPending('receipt_waybill') },
        { key: 'pay_order', title: '付款单', subtitle: '待审核', value: countPending('pay_order') },
        { key: 'daily_io', title: '日常收支', subtitle: '待审核', value: countPending('daily_io') },
        { key: 'customer_check', title: '客户考核', subtitle: '待审核', value: countPending('customer_check') },
        { key: 'carrier_check', title: '运力考核', subtitle: '待审核', value: countPending('carrier_check') },
        { key: 'driver_borrow', title: '司机借支', subtitle: '待审核', value: countPending('driver_borrow') },
        { key: 'vehicle_borrow', title: '车辆借支', subtitle: '待审核', value: countPending('vehicle_borrow') },
        { key: 'staff_borrow', title: '员工借支', subtitle: '待审核', value: countPending('staff_borrow') }
      ]
    },
    activeAuditConfig () {
      return this.auditCategoryMeta[this.activeAuditCategory] || {
        tableTitle: '审核列表',
        routeName: '',
        menuKey: 'outbound'
      }
    },
    visibleAuditRows () {
      const rows = this.rawAuditRows.filter(item => item.category === this.activeAuditCategory)
      if (this.activeAuditTab === 'mine') {
        const loginName = LocalStorage.getItem('login_name') || ''
        return rows.filter(item => item.applicant === loginName)
      }
      return rows.filter(item => item.audit_status === '待审核')
    }
  },
  created () {
    LocalStorage.set('menulink', '')
    this.refreshTransitData()
    this.refreshAuditRows()
  },
  methods: {
    normalizeTransitStatus (row) {
      const fee = transportFeeMeta(row)
      if (row.waybill_status) {
        return row.waybill_status
      }
      if (fee.waybill_status) {
        return fee.waybill_status
      }
      if (row.audit_status === '待审核') {
        return '待接单'
      }
      if (row.dn_status >= 5) {
        return '运输中'
      }
      if (row.audit_status === '已审核') {
        return '待发车'
      }
      return '待接单'
    },
    normalizeAuditRow (row, index) {
      const fee = transportFeeMeta(row)
      const auditStatus = fee.audit_status || row.audit_status || '待审核'
      return {
        id: row.id || index,
        category: 'waybill_review',
        order_no: row.dn_code || `DN${String(index + 1).padStart(4, '0')}`,
        applicant: fee.dispatcher || row.creater || '--',
        fee_name: fee.cargo_name || fee.line_name || '运单费用',
        amount: Number(row.total_cost || fee.arrival_freight || 0).toFixed(2),
        customer: row.customer || '--',
        project: fee.project_name || fee.organization || '--',
        driver: fee.main_driver || '--',
        plate_number: fee.plate_number || '--',
        apply_time: this.formatDateTime(row.create_time),
        audit_remark: fee.audit_remark || '--',
        audit_status: auditStatus,
        actions: auditStatus === '待审核'
          ? [
              { label: '去审核', type: 'route', routeName: 'freshorder', menuKey: 'outbound', query: { focus: row.id } },
              { label: '查看运单', type: 'route', routeName: 'dn', menuKey: 'outbound' }
            ]
          : [
              { label: '查看详情', type: 'route', routeName: 'dn', menuKey: 'outbound' }
            ]
      }
    },
    buildDemoAuditRows () {
      const loginName = LocalStorage.getItem('login_name') || '当前用户'
      return [
        this.demoAuditRow('transit_fee_1', 'transit_fee', 'TF20260612001', '在途油费', '680.00', '西安莲湖白金线', '干线运输', '王师傅', '陕A12345', 'dispatchlist', 'driver', loginName),
        this.demoAuditRow('receipt_order_1', 'receipt_order', 'SK20260612002', '收款单-订单', '3520.00', '西安北郊项目', '客户对账', '--', '--', 'receiptbill', 'finance', loginName),
        this.demoAuditRow('pay_order_1', 'pay_order', 'FK20260612003', '付款单', '2180.00', '承运付款', '运力结算', '李师傅', '陕A67890', 'paybill', 'finance', loginName),
        this.demoAuditRow('reimburse_1', 'reimburse', 'BX20260612004', '司机报销单', '450.00', '项目费用', '司机报销', '赵师傅', '陕A99881', 'driverCheck', 'finance', loginName),
        this.demoAuditRow('daily_io_1', 'daily_io', 'RC20260612005', '日常收支', '120.00', '日常费用', '运营支出', '--', '--', 'dailyincome', 'finance', loginName)
      ]
    },
    demoAuditRow (id, category, orderNo, feeName, amount, customer, project, driver, plate, routeName, menuKey, applicant) {
      return {
        id,
        category,
        order_no: orderNo,
        audit_status: '待审核',
        applicant,
        fee_name: feeName,
        amount,
        customer,
        project,
        driver,
        plate_number: plate,
        apply_time: '2026-06-12 15:30',
        audit_remark: '待审核',
        actions: [
          { label: '进入模块', type: 'route', routeName, menuKey }
        ]
      }
    },
    formatDateTime (value) {
      if (!value) {
        return '--'
      }
      return String(value).replace('T', ' ').slice(0, 16)
    },
    async refreshTransitData () {
      try {
        const res = await getauth('dn/transit/', {})
        const rows = Array.isArray(res.results) ? res.results : (Array.isArray(res) ? res : [])
        this.rawTransitRows = rows
      } catch (error) {
        this.rawTransitRows = []
      }
    },
    async refreshAuditRows () {
      try {
        const res = await getauth('dn/list/?page=1', {})
        const rows = Array.isArray(res.results) ? res.results : []
        this.rawAuditRows = [
          ...rows.map((item, index) => this.normalizeAuditRow(item, index)),
          ...this.buildDemoAuditRows()
        ]
      } catch (error) {
        this.rawAuditRows = this.buildDemoAuditRows()
      }
    },
    badgeClass (status) {
      if (status === '已审核') {
        return 'badge-green'
      }
      if (status === '退回修改') {
        return 'badge-red'
      }
      return 'badge-orange'
    },
    handleAuditAction (action, row) {
      if (action.type === 'route') {
        LocalStorage.set('menulink', action.menuKey || row.menuKey || 'outbound')
        this.$router.push({
          name: action.routeName || row.routeName,
          query: action.query || {}
        })
      }
    },
    openAuditList (categoryKey) {
      const config = this.auditCategoryMeta[categoryKey]
      if (!config || !config.routeName) {
        return
      }
      LocalStorage.set('menulink', config.menuKey || 'outbound')
      this.$router.push({
        name: config.routeName,
        query: {
          from: 'home_audit',
          category: categoryKey
        }
      })
    },
    openAuditRow (row) {
      const config = this.auditCategoryMeta[row.category] || {}
      const routeName = config.routeName || (row.actions && row.actions[0] && row.actions[0].routeName)
      const menuKey = config.menuKey || (row.actions && row.actions[0] && row.actions[0].menuKey) || 'outbound'
      if (!routeName) {
        return
      }
      LocalStorage.set('menulink', menuKey)
      this.$router.push({
        name: routeName,
        query: {
          from: 'home_audit',
          category: row.category,
          focus: row.id,
          keyword: row.order_no
        }
      })
    },
    goPage (routeName, menuKey) {
      LocalStorage.set('menulink', menuKey)
      this.$router.push({ name: routeName })
    }
  }
}
</script>

<style scoped>
.home-dashboard-page {
  min-height: 100%;
  padding: 0;
  background: #f5f6fb;
}

.page-shell {
  min-height: 100%;
  padding: 0 10px 12px;
}

.tab-header {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  height: 58px;
  padding: 0 8px;
  border-bottom: 1px solid #d9ccff;
  background: #fff;
}

.header-tab {
  min-width: 112px;
  height: 42px;
  margin-bottom: -1px;
  border: 1px solid transparent;
  border-bottom: 0;
  border-radius: 12px 12px 0 0;
  background: transparent;
  color: #6b5aa6;
  font-size: 16px;
  cursor: pointer;
}

.header-tab.active {
  background: #fff;
  border-color: #cdbdff;
  color: #6a3df0;
  box-shadow: 0 8px 16px rgba(120, 86, 255, 0.08);
}

.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 238px;
  gap: 16px;
  padding-top: 14px;
}

.main-column,
.side-column {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-card {
  border: 1px solid #e5e8f4;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 8px 20px rgba(39, 62, 109, 0.06);
}

.overview-card,
.audit-card {
  padding: 16px 18px 18px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.section-title-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
}

.section-title {
  font-size: 17px;
  font-weight: 700;
  color: #1f2737;
}

.link-action,
.table-link {
  border: 0;
  background: transparent;
  color: #6b3ff0;
  font-size: 14px;
  cursor: pointer;
}

.switch-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.switch-btn {
  min-width: 56px;
  height: 34px;
  padding: 0 14px;
  border: 1px solid #eceef5;
  border-radius: 8px;
  background: #f7f7fa;
  color: #657080;
  cursor: pointer;
}

.switch-btn.active {
  background: #6936f5;
  border-color: #6936f5;
  color: #fff;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  border: 1px solid #edf0f7;
  border-radius: 12px;
  overflow: hidden;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 96px;
  padding: 18px 16px;
  background: #fcfcfe;
  border-right: 1px solid #eceff6;
}

.status-card:last-child {
  border-right: 0;
}

.status-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
}

.status-content {
  display: grid;
  grid-template-columns: auto auto;
  column-gap: 4px;
  align-items: baseline;
}

.status-label {
  grid-column: 1 / -1;
  margin-bottom: 6px;
  font-size: 14px;
  color: #424d5f;
}

.status-value {
  color: #ff7a1a;
  font-size: 36px;
  font-weight: 700;
  line-height: 1;
}

.status-unit {
  color: #7f8898;
  font-size: 14px;
}

.audit-tabs {
  display: flex;
  gap: 24px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eceef6;
}

.audit-tab {
  position: relative;
  border: 0;
  background: transparent;
  padding: 0 0 10px;
  color: #616b7d;
  font-size: 15px;
  cursor: pointer;
}

.audit-tab.active {
  color: #643ef1;
  font-weight: 700;
}

.audit-tab.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 3px;
  border-radius: 999px;
  background: #643ef1;
}

.audit-summary-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.audit-summary-card {
  padding: 14px 14px 12px;
  border: 1px solid #edf0f6;
  border-radius: 12px;
  background: #fafbfe;
  cursor: pointer;
}

.audit-summary-card.selected {
  border-color: #6c43f3;
  box-shadow: inset 0 0 0 1px #6c43f3;
}

.summary-title {
  font-size: 14px;
  font-weight: 700;
  color: #202a3a;
}

.summary-subtitle,
.summary-link {
  margin-top: 8px;
  font-size: 12px;
  color: #7f8797;
}

.summary-link {
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.summary-value {
  margin-top: 10px;
  color: #ff7b10;
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}

.table-block {
  margin-top: 16px;
  border: 1px solid #edf0f6;
  border-radius: 12px;
  overflow: hidden;
}

.table-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 14px;
  background: #fbfbfe;
  border-bottom: 1px solid #edf0f6;
}

.table-title {
  font-size: 15px;
  font-weight: 700;
  color: #5c6480;
}

.table-wrap {
  overflow-x: auto;
}

.audit-table {
  width: 100%;
  min-width: 1120px;
  border-collapse: collapse;
}

.audit-table th,
.audit-table td {
  padding: 12px 10px;
  border-bottom: 1px solid #eef1f6;
  text-align: left;
  font-size: 13px;
  color: #4c5668;
  white-space: nowrap;
}

.audit-table th {
  background: #f8f9fd;
  color: #3f4960;
  font-weight: 700;
}

.table-row-clickable {
  cursor: pointer;
}

.table-row-clickable:hover td {
  background: #f7f5ff;
}

.table-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 70px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.badge-green {
  color: #27814d;
  background: #e7f6ed;
}

.badge-orange {
  color: #d67a10;
  background: #fff2df;
}

.badge-red {
  color: #c44e4e;
  background: #feecec;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.text-action {
  border: 0;
  background: transparent;
  color: #5b38e7;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}

.empty-cell {
  text-align: center;
  color: #98a1b2;
  padding: 28px 10px;
}

.shortcut-card,
.quick-panel-card {
  padding: 14px;
}

.shortcut-head {
  margin-bottom: 12px;
}

.shortcut-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #8a94a6;
}

.shortcut-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.shortcut-btn {
  min-height: 44px;
  padding: 0 10px;
  border: 1px solid #dfebfb;
  border-radius: 10px;
  background: #edf5ff;
  color: #2d4869;
  font-size: 13px;
  cursor: pointer;
}

.panel-note {
  margin: 12px 0 0;
  color: #6c7488;
  font-size: 13px;
  line-height: 1.8;
}

.flow-layout {
  padding-top: 14px;
}

.flow-banner {
  padding: 20px 22px;
  border: 1px solid #e4e8f5;
  border-radius: 16px;
  background: linear-gradient(135deg, #fff 0%, #f6f2ff 100%);
}

.flow-banner-title {
  font-size: 24px;
  font-weight: 700;
  color: #322450;
}

.flow-banner-desc {
  margin-top: 8px;
  font-size: 14px;
  color: #6d7286;
}

.flow-timeline {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.flow-group {
  padding: 18px;
  border: 1px solid #e6e9f4;
  border-radius: 16px;
  background: #fff;
}

.flow-group-title {
  margin-bottom: 14px;
  font-size: 18px;
  font-weight: 700;
  color: #2b3142;
}

.flow-step-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.flow-step-card {
  padding: 18px;
  border: 1px solid #ebeef7;
  border-radius: 14px;
  background: #fafbff;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.flow-step-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(60, 84, 128, 0.08);
}

.step-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 54px;
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  background: #ede5ff;
  color: #6d41f3;
  font-size: 12px;
  font-weight: 700;
}

.step-title {
  margin-top: 12px;
  font-size: 17px;
  font-weight: 700;
  color: #1d2637;
}

.step-desc {
  margin-top: 10px;
  min-height: 44px;
  font-size: 13px;
  line-height: 1.7;
  color: #6c7487;
}

.step-route {
  margin-top: 14px;
  color: #6b3ff0;
  font-size: 13px;
  font-weight: 700;
}

@media (max-width: 1600px) {
  .status-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .audit-summary-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 1280px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }

  .shortcut-grid,
  .flow-step-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .status-grid,
  .audit-summary-grid,
  .shortcut-grid,
  .flow-step-grid {
    grid-template-columns: 1fr;
  }

  .section-head,
  .section-title-wrap {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
