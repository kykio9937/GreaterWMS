<template>
  <div class="finance-list-page">
    <q-card flat bordered class="filter-card">
      <div class="filter-grid">
        <q-input v-model="filters.waybill" outlined dense clearable label="运单编号" @keyup.enter="applyFilters" />
        <q-input v-model="filters.orderNo" outlined dense clearable label="订单编号" @keyup.enter="applyFilters" />
        <q-select
          v-model="filters.status"
          outlined
          dense
          emit-value
          map-options
          :options="statusOptions"
          label="对账状态"
        />
        <div class="filter-actions">
          <q-btn unelevated color="primary" icon="search" label="查询" @click="applyFilters" />
        </div>
      </div>
    </q-card>

    <q-card flat bordered class="table-card">
      <div class="table-toolbar">
        <div class="toolbar-tabs">
          <button type="button" class="toolbar-tab" @click="$router.push({ name: 'supplierasnlist' })">承运商汇总</button>
          <button type="button" class="toolbar-tab toolbar-tab--active">承运商明细</button>
        </div>
        <div class="toolbar-left">
          <q-btn flat color="primary" icon="task_alt" label="确认对账" @click="confirmSelected" />
          <q-btn flat color="primary" icon="file_download" label="导出明细" @click="exportData" />
          <q-btn flat color="primary" icon="print" label="打印" />
          <q-btn flat round dense color="primary" icon="settings" />
        </div>
      </div>

      <q-table
        flat
        :data="pagedRows"
        :columns="columns"
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
            <q-td key="dn_code" :props="props">{{ props.row.dn_code }}</q-td>
            <q-td key="order_no" :props="props">{{ props.row.order_no }}</q-td>
            <q-td key="supplier" :props="props">{{ props.row.supplier }}</q-td>
            <q-td key="vehicle" :props="props">{{ props.row.vehicle }}</q-td>
            <q-td key="payable_fee" :props="props" class="number-cell">{{ props.row.payable_fee }}</q-td>
            <q-td key="reward_fee" :props="props" class="number-cell">{{ props.row.reward_fee }}</q-td>
            <q-td key="other_fee" :props="props" class="number-cell">{{ props.row.other_fee }}</q-td>
            <q-td key="status" :props="props">
              <span :class="['status-badge', props.row.status === '已对账' ? 'status-badge--done' : 'status-badge--wait']">
                {{ props.row.status }}
              </span>
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
import { getauth, postauth } from 'boot/axios_request'

export default {
  name: 'Pageasnfinish',
  data () {
    return {
      current: 1,
      pagination: { rowsPerPage: 12 },
      selectedIds: [],
      filters: {
        waybill: '',
        orderNo: '',
        status: 'all'
      },
      statusOptions: [
        { label: '全部状态', value: 'all' },
        { label: '待对账', value: '待对账' },
        { label: '已对账', value: '已对账' }
      ],
      rows: [],
      columns: [
        { name: 'dn_code', label: '运单编号', field: 'dn_code', align: 'left' },
        { name: 'order_no', label: '订单编号', field: 'order_no', align: 'left' },
        { name: 'supplier', label: '承运商名称', field: 'supplier', align: 'left' },
        { name: 'vehicle', label: '车辆信息', field: 'vehicle', align: 'left' },
        { name: 'payable_fee', label: '应付运输费', field: 'payable_fee', align: 'right' },
        { name: 'reward_fee', label: '司机奖励', field: 'reward_fee', align: 'right' },
        { name: 'other_fee', label: '其他费用', field: 'other_fee', align: 'right' },
        { name: 'status', label: '对账状态', field: 'status', align: 'center' }
      ]
    }
  },
  computed: {
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
      return this.rows.filter(row => {
        const matchWaybill = !this.filters.waybill || row.dn_code.includes(this.filters.waybill)
        const matchOrder = !this.filters.orderNo || row.order_no.includes(this.filters.orderNo)
        const matchStatus = this.filters.status === 'all' || row.status === this.filters.status
        return matchWaybill && matchOrder && matchStatus
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
    formatAmount (value) {
      return Number(value || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    applyFilters () {
      this.current = 1
    },
    async getList () {
      try {
        if (this.$q.localStorage.has('auth')) {
          const res = await getauth('dn/reconcile/carrier/detail/', {})
          this.rows = (Array.isArray(res) ? res : []).map(item => ({
            id: item.id,
            dn_code: item.dn_code,
            order_no: item.order_no,
            supplier: item.supplier,
            vehicle: item.vehicle,
            payable_fee: this.formatAmount(item.payable_fee),
            reward_fee: this.formatAmount(item.reward_fee),
            other_fee: this.formatAmount(item.other_fee),
            status: item.status
          }))
        } else {
          this.rows = []
        }
      } catch (err) {
        this.rows = []
      }
    },
    async confirmSelected () {
      if (!this.selectedIds.length) {
        this.$q.notify({ message: '请选择需要确认对账的承运单', color: 'orange', icon: 'warning' })
        return
      }
      try {
        await Promise.all(this.selectedIds.map(id => postauth(`dn/reconcile/carrier/${id}/`, {})))
        this.$q.notify({ message: '承运商对账已确认', color: 'positive', icon: 'task_alt' })
        this.selectedIds = []
        this.getList()
      } catch (err) {}
    },
    exportData () {
      const header = ['运单编号', '订单编号', '承运商名称', '车辆信息', '应付运输费', '司机奖励', '其他费用', '对账状态']
      const body = this.filteredRows.map(item => [item.dn_code, item.order_no, item.supplier, item.vehicle, item.payable_fee, item.reward_fee, item.other_fee, item.status])
      const content = [header].concat(body).map(line => line.join(',')).join('\r\n')
      exportFile('承运商对账明细.csv', '\ufeff' + content, 'text/csv')
    }
  },
  created () {
    this.getList()
  }
}
</script>

<style scoped>
.finance-list-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-card,
.table-card {
  border-radius: 16px;
  background: #fff;
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

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid #ebeef5;
  padding: 0 8px 0 0;
  flex-wrap: wrap;
}

.toolbar-tabs {
  display: flex;
  align-items: flex-end;
}

.toolbar-tab {
  min-width: 108px;
  height: 34px;
  border: 1px solid #d8def0;
  border-bottom: 0;
  background: #fff;
  color: #51607a;
  font-size: 13px;
  cursor: pointer;
}

.toolbar-tab + .toolbar-tab {
  margin-left: 2px;
}

.toolbar-tab--active {
  color: #5b33d6;
  font-weight: 700;
  box-shadow: inset 0 2px 0 #6b41f2;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px 0 0;
}

.finance-table {
  margin-top: -1px;
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
  .filter-grid {
    grid-template-columns: 1fr;
  }

  .table-toolbar,
  .table-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .toolbar-tabs,
  .toolbar-left {
    width: 100%;
    overflow-x: auto;
  }

  .finance-table {
    overflow-x: auto;
  }
}
</style>
