<template>
  <div class="module-page">
    <q-card flat bordered class="module-shortcuts">
      <q-tabs
        v-model="activeShortcut"
        inline-label
        active-color="primary"
        indicator-color="transparent"
        class="shortcut-tabs"
      >
        <q-route-tab
          v-for="item in shortcutItems"
          :key="item.name"
          :name="item.name"
          :label="item.label"
          :to="{ name: item.name }"
          class="shortcut-tab"
          exact
        />
      </q-tabs>
    </q-card>

    <q-card flat bordered class="module-hero">
      <div>
        <div class="module-title">{{ pageConfig.title }}</div>
        <div class="module-desc">{{ pageConfig.desc }}</div>
      </div>
      <div class="module-actions">
        <q-btn flat color="primary" icon="file_download" label="导出" @click="exportData" />
        <q-btn flat color="primary" icon="print" label="打印" />
        <q-btn flat round dense color="primary" icon="settings" />
      </div>
    </q-card>

    <q-card flat bordered class="filter-card">
      <div class="filter-grid">
        <q-input v-model="filters.keyword" outlined dense clearable :label="pageConfig.keywordLabel" @keyup.enter="applyFilters" />
        <q-input v-model="filters.dateRange" outlined dense clearable label="创建时间" placeholder="26-05-09~26-06-09" @keyup.enter="applyFilters" />
        <q-select
          v-model="filters.status"
          outlined
          dense
          emit-value
          map-options
          :options="statusOptions"
          label="状态"
        />
        <div class="filter-actions">
          <q-btn unelevated color="primary" icon="search" label="查询" @click="applyFilters" />
        </div>
      </div>
    </q-card>

    <q-card flat bordered class="table-card">
      <q-table
        flat
        :data="pagedRows"
        :columns="pageConfig.columns"
        row-key="id"
        hide-bottom
        :pagination.sync="pagination"
        class="finance-table"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width>
              <q-checkbox v-model="allSelected" color="primary" size="sm" />
            </q-th>
            <q-th v-for="col in props.cols" :key="col.name">{{ col.label }}</q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td auto-width>
              <q-checkbox v-model="selectedIds" :val="props.row.id" color="primary" size="sm" />
            </q-td>
            <q-td
              v-for="col in pageConfig.columns"
              :key="col.name"
              :props="props"
              :class="{ 'number-cell': col.align === 'right' }"
            >
              <span v-if="col.name === 'status'" :class="['status-badge', props.row.status === '已完成' || props.row.status === '已对账' ? 'status-badge--done' : 'status-badge--wait']">
                {{ props.row[col.field || col.name] }}
              </span>
              <span v-else>{{ props.row[col.field || col.name] }}</span>
            </q-td>
          </q-tr>
        </template>
      </q-table>

      <div class="table-footer">
        <div class="footer-count">共 {{ filteredRows.length }} 条</div>
        <q-pagination v-model="current" color="primary" :max="maxPage" :max-pages="6" boundary-links />
      </div>
    </q-card>
  </div>
</template>

<script>
import { exportFile } from 'quasar'

const PAGE_CONFIG = {
  customerAssessment: {
    title: '客户考核',
    desc: '按客户统计签收、时效和结算完成情况，支持财务考核。',
    keywordLabel: '客户名称',
    columns: [
      { name: 'name', label: '客户名称', field: 'name', align: 'left' },
      { name: 'score', label: '考核得分', field: 'score', align: 'right' },
      { name: 'timely_rate', label: '时效达成率', field: 'timely_rate', align: 'right' },
      { name: 'settle_rate', label: '结算完成率', field: 'settle_rate', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, name: '西安莲湖', score: '95', timely_rate: '98%', settle_rate: '93%', status: '已完成' }
    ]
  },
  capacityAssessment: {
    title: '运力考核',
    desc: '按承运司机与车辆执行情况进行运力评分与费用核查。',
    keywordLabel: '运力主体',
    columns: [
      { name: 'name', label: '运力主体', field: 'name', align: 'left' },
      { name: 'vehicle', label: '车辆', field: 'vehicle', align: 'left' },
      { name: 'score', label: '考核得分', field: 'score', align: 'right' },
      { name: 'completion', label: '完成率', field: 'completion', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, name: '张师傅', vehicle: '冀RP7833', score: '92', completion: '96%', status: '已完成' }
    ]
  },
  directSettlement: {
    title: '直接结算',
    desc: '处理直客业务的结算单、费用确认与回款闭环。',
    keywordLabel: '结算单号',
    columns: [
      { name: 'bill_no', label: '结算单号', field: 'bill_no', align: 'left' },
      { name: 'customer', label: '客户名称', field: 'customer', align: 'left' },
      { name: 'amount', label: '结算金额', field: 'amount', align: 'right' },
      { name: 'create_time', label: '创建时间', field: 'create_time', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, bill_no: 'JS202606090001', customer: '西安莲湖', amount: '18,520.00', create_time: '2026-06-09', status: '待处理' }
    ]
  },
  driverCheck: {
    title: '司机对账',
    desc: '汇总司机运输、补贴和报销费用，形成司机对账单。',
    keywordLabel: '司机名称',
    columns: [
      { name: 'name', label: '司机名称', field: 'name', align: 'left' },
      { name: 'vehicle', label: '车牌号', field: 'vehicle', align: 'left' },
      { name: 'transport_fee', label: '运输费', field: 'transport_fee', align: 'right' },
      { name: 'expense_fee', label: '报销费', field: 'expense_fee', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, name: '张师傅', vehicle: '冀RP7833', transport_fee: '7,129.16', expense_fee: '320.00', status: '待对账' }
    ]
  },
  vehicleCheck: {
    title: '车辆对账',
    desc: '按车辆维度核对运费、油补、路桥等成本科目。',
    keywordLabel: '车牌号',
    columns: [
      { name: 'vehicle', label: '车牌号', field: 'vehicle', align: 'left' },
      { name: 'line_name', label: '线路名称', field: 'line_name', align: 'left' },
      { name: 'transport_fee', label: '运输费', field: 'transport_fee', align: 'right' },
      { name: 'other_fee', label: '其他费用', field: 'other_fee', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, vehicle: '冀RP8113', line_name: '无锡冷链专线', transport_fee: '8,350.42', other_fee: '420.00', status: '待对账' }
    ]
  },
  receiptbill: {
    title: '收款单',
    desc: '查看客户回款登记、到账确认与核销状态。',
    keywordLabel: '收款单号',
    columns: [
      { name: 'bill_no', label: '收款单号', field: 'bill_no', align: 'left' },
      { name: 'customer', label: '客户名称', field: 'customer', align: 'left' },
      { name: 'amount', label: '收款金额', field: 'amount', align: 'right' },
      { name: 'channel', label: '收款方式', field: 'channel', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, bill_no: 'SK202606090001', customer: '西安莲湖', amount: '15,000.00', channel: '银行转账', status: '已完成' }
    ]
  },
  paybill: {
    title: '付款单',
    desc: '统一管理承运商、司机等付款申请和付款执行。',
    keywordLabel: '付款单号',
    columns: [
      { name: 'bill_no', label: '付款单号', field: 'bill_no', align: 'left' },
      { name: 'supplier', label: '付款对象', field: 'supplier', align: 'left' },
      { name: 'amount', label: '付款金额', field: 'amount', align: 'right' },
      { name: 'channel', label: '付款方式', field: 'channel', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, bill_no: 'FK202606090001', supplier: '陕西卡运联盟', amount: '20,000.00', channel: '银行转账', status: '待处理' }
    ]
  },
  driverexpense: {
    title: '司机报销单',
    desc: '管理司机餐补、住宿、油费与临时报销单据。',
    keywordLabel: '报销单号',
    columns: [
      { name: 'bill_no', label: '报销单号', field: 'bill_no', align: 'left' },
      { name: 'driver', label: '司机名称', field: 'driver', align: 'left' },
      { name: 'category', label: '费用类别', field: 'category', align: 'left' },
      { name: 'amount', label: '报销金额', field: 'amount', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, bill_no: 'BX202606090001', driver: '张师傅', category: '高速路费', amount: '320.00', status: '待处理' }
    ]
  },
  borrowmanage: {
    title: '借支管理',
    desc: '跟踪司机、项目预借款的申请、审批与核销情况。',
    keywordLabel: '借支单号',
    columns: [
      { name: 'bill_no', label: '借支单号', field: 'bill_no', align: 'left' },
      { name: 'applicant', label: '申请人', field: 'applicant', align: 'left' },
      { name: 'purpose', label: '借支用途', field: 'purpose', align: 'left' },
      { name: 'amount', label: '借支金额', field: 'amount', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, bill_no: 'JZ202606090001', applicant: '张师傅', purpose: '过路费预支', amount: '1,000.00', status: '待处理' }
    ]
  },
  costmanage: {
    title: '成本管理',
    desc: '按线路、车辆和客户汇总运输成本，便于利润分析。',
    keywordLabel: '成本主题',
    columns: [
      { name: 'subject', label: '成本主题', field: 'subject', align: 'left' },
      { name: 'line_name', label: '线路名称', field: 'line_name', align: 'left' },
      { name: 'cost_amount', label: '成本金额', field: 'cost_amount', align: 'right' },
      { name: 'ratio', label: '成本占比', field: 'ratio', align: 'right' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, subject: '冷链运输成本', line_name: '无锡冷链专线', cost_amount: '32,500.00', ratio: '42%', status: '已完成' }
    ]
  },
  dailyincome: {
    title: '日常收支',
    desc: '记录日常经营中的零星收款、付款和杂项支出。',
    keywordLabel: '收支主题',
    columns: [
      { name: 'subject', label: '收支主题', field: 'subject', align: 'left' },
      { name: 'type', label: '类型', field: 'type', align: 'left' },
      { name: 'amount', label: '金额', field: 'amount', align: 'right' },
      { name: 'operator', label: '经办人', field: 'operator', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, subject: '办公费用', type: '支出', amount: '860.00', operator: '财务专员', status: '已完成' }
    ]
  },
  capitalflow: {
    title: '资金流水',
    desc: '查看账户资金进出流水，支持按业务单据追溯。',
    keywordLabel: '流水单号',
    columns: [
      { name: 'flow_no', label: '流水单号', field: 'flow_no', align: 'left' },
      { name: 'account', label: '账户', field: 'account', align: 'left' },
      { name: 'amount', label: '流水金额', field: 'amount', align: 'right' },
      { name: 'direction', label: '方向', field: 'direction', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, flow_no: 'LS202606090001', account: '建行主账户', amount: '15,000.00', direction: '收入', status: '已完成' }
    ]
  },
  documentcenter: {
    title: '单据中心',
    desc: '统一查看财务单据、对账单、付款单和报销单的生成记录。',
    keywordLabel: '单据编号',
    columns: [
      { name: 'doc_no', label: '单据编号', field: 'doc_no', align: 'left' },
      { name: 'doc_type', label: '单据类型', field: 'doc_type', align: 'left' },
      { name: 'owner', label: '业务主体', field: 'owner', align: 'left' },
      { name: 'create_time', label: '创建时间', field: 'create_time', align: 'left' },
      { name: 'status', label: '状态', field: 'status', align: 'center' }
    ],
    rows: [
      { id: 1, doc_no: 'DJ202606090001', doc_type: '客户对账单', owner: '西安莲湖', create_time: '2026-06-09', status: '已完成' }
    ]
  }
}

export default {
  name: 'PageFinanceModule',
  data () {
    return {
      activeShortcut: this.$route.name,
      current: 1,
      pagination: { rowsPerPage: 12 },
      selectedIds: [],
      filters: {
        keyword: '',
        dateRange: '26-05-09~26-06-09',
        status: 'all'
      },
      statusOptions: [
        { label: '全部状态', value: 'all' },
        { label: '待处理', value: '待处理' },
        { label: '待对账', value: '待对账' },
        { label: '已完成', value: '已完成' },
        { label: '已对账', value: '已对账' }
      ]
    }
  },
  computed: {
    shortcutItems () {
      return [
        { name: 'customerAssessment', label: '客户考核' },
        { name: 'capacityAssessment', label: '运力考核' },
        { name: 'directSettlement', label: '直接结算' },
        { name: 'driverCheck', label: '司机对账' },
        { name: 'vehicleCheck', label: '车辆对账' },
        { name: 'receiptbill', label: '收款单' },
        { name: 'paybill', label: '付款单' },
        { name: 'driverexpense', label: '司机报销单' },
        { name: 'borrowmanage', label: '借支管理' },
        { name: 'costmanage', label: '成本管理' },
        { name: 'dailyincome', label: '日常收支' },
        { name: 'capitalflow', label: '资金流水' },
        { name: 'documentcenter', label: '单据中心' }
      ]
    },
    pageConfig () {
      return PAGE_CONFIG[this.$route.name] || PAGE_CONFIG.directSettlement
    },
    allSelected: {
      get () {
        return this.pagedRows.length > 0 && this.pagedRows.every(row => this.selectedIds.includes(row.id))
      },
      set (value) {
        const pageIds = this.pagedRows.map(row => row.id)
        this.selectedIds = value ? Array.from(new Set(this.selectedIds.concat(pageIds))) : this.selectedIds.filter(id => !pageIds.includes(id))
      }
    },
    filteredRows () {
      const keyword = (this.filters.keyword || '').trim()
      return (this.pageConfig.rows || []).filter(row => {
        const matchKeyword = !keyword || Object.values(row).some(value => String(value || '').includes(keyword))
        const matchStatus = this.filters.status === 'all' || row.status === this.filters.status
        return matchKeyword && matchStatus
      })
    },
    pagedRows () {
      const start = (this.current - 1) * this.pagination.rowsPerPage
      return this.filteredRows.slice(start, start + this.pagination.rowsPerPage)
    },
    maxPage () {
      const pages = Math.ceil(this.filteredRows.length / this.pagination.rowsPerPage)
      return pages || 1
    }
  },
  methods: {
    applyFilters () {
      this.current = 1
    },
    exportData () {
      const header = this.pageConfig.columns.map(item => item.label)
      const body = this.filteredRows.map(row => this.pageConfig.columns.map(col => row[col.field || col.name]))
      const content = [header].concat(body).map(line => line.join(',')).join('\r\n')
      exportFile(`${this.pageConfig.title}.csv`, '\ufeff' + content, 'text/csv')
    }
  },
  watch: {
    '$route.name' () {
      this.activeShortcut = this.$route.name
      this.current = 1
      this.selectedIds = []
      this.filters.keyword = ''
      this.filters.status = 'all'
    }
  }
}
</script>

<style scoped>
.module-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.module-shortcuts,
.module-hero,
.filter-card,
.table-card {
  border-radius: 16px;
  background: #fff;
}

.module-shortcuts {
  padding: 8px 12px;
}

.shortcut-tabs {
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 8px;
}

.shortcut-tab {
  min-height: 34px;
  margin-right: 8px;
  margin-bottom: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f3f6fb;
  color: #607089;
  font-size: 12px;
}

.shortcut-tab.q-tab--active {
  background: linear-gradient(135deg, #4f2bd8 0%, #6a3ff1 100%);
  color: #fff;
  box-shadow: 0 8px 20px rgba(79, 43, 216, 0.18);
}

.module-hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px;
}

.module-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2a44;
}

.module-desc {
  margin-top: 6px;
  font-size: 12px;
  color: #7d889f;
}

.module-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-card {
  padding: 14px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  align-items: center;
}

.filter-actions {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.finance-table :deep(.q-table thead tr) {
  background: #f6f8fc;
}

.finance-table :deep(.q-table th) {
  color: #2b3d59;
  font-weight: 700;
  white-space: nowrap;
  font-size: 12px;
}

.finance-table :deep(.q-table td) {
  padding: 9px 8px;
  white-space: nowrap;
}

.number-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.status-badge {
  display: inline-block;
  min-width: 58px;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 12px;
  text-align: center;
}

.status-badge--done {
  background: #e8f7ee;
  color: #1f9d55;
}

.status-badge--wait {
  background: #fef2e6;
  color: #d97706;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.footer-count {
  color: #6f7b92;
  font-size: 13px;
}

@media (max-width: 1200px) {
  .filter-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .module-hero,
  .table-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .finance-table {
    overflow-x: auto;
  }
}
</style>
