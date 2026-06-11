<template>
  <div class="finance-detail-page">
    <q-card flat bordered class="filter-card">
      <div class="filter-grid">
        <q-select
          v-model="filters.organization"
          outlined
          dense
          emit-value
          map-options
          :options="organizationOptions"
          label="所属组织"
        />
        <q-input
          v-model="filters.dateRange"
          outlined
          dense
          clearable
          label="创建时间"
          placeholder="26-05-09~26-06-09"
          @keyup.enter="applyFilters"
        />
        <q-select
          v-model="filters.customerName"
          outlined
          dense
          emit-value
          map-options
          :options="customerOptions"
          label="客户名称"
        />
        <div class="filter-actions">
          <q-btn unelevated color="primary" icon="search" label="查询" @click="applyFilters" />
        </div>
      </div>
    </q-card>

    <q-card flat bordered class="table-card">
      <div class="table-toolbar">
        <div class="toolbar-tabs">
          <button type="button" class="toolbar-tab toolbar-tab--active">客户汇总</button>
          <button type="button" class="toolbar-tab" @click="$router.push({ name: 'customerpod' })">客户明细</button>
        </div>
        <div class="toolbar-left">
          <q-btn flat color="primary" icon="file_download" label="导出" @click="exportData" />
          <q-btn flat color="primary" icon="print" label="打印" />
          <q-btn flat round dense color="primary" icon="settings" />
        </div>
      </div>

      <q-table
        flat
        :data="pagedRows"
        :columns="columns"
        row-key="id"
        :loading="loading"
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
          <q-tr class="filter-head-row">
            <q-th auto-width class="filter-head-label">筛选</q-th>
            <q-th v-for="col in props.cols" :key="`${col.name}-filter`">
              <q-input
                v-if="tableFilters[col.name] !== undefined"
                v-model="tableFilters[col.name]"
                dense
                outlined
                clearable
                class="table-filter-input"
                @input="applyFilters"
              />
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td auto-width>
              <q-checkbox v-model="selectedIds" :val="props.row.id" color="primary" size="sm" />
            </q-td>
            <q-td key="action" :props="props">
              <q-btn flat dense color="primary" label="[明细]" @click="$router.push({ name: 'customerpod' })" />
            </q-td>
            <q-td key="organization" :props="props">{{ props.row.organization }}</q-td>
            <q-td key="customer_name" :props="props">{{ props.row.customer_name }}</q-td>
            <q-td key="checked_total" :props="props" class="number-cell">{{ formatAmount(props.row.checked_total) }}</q-td>
            <q-td key="unchecked_total" :props="props" class="number-cell">{{ formatAmount(props.row.unchecked_total) }}</q-td>
            <q-td key="total_count" :props="props" class="number-cell">{{ props.row.total_count }}</q-td>
            <q-td key="checked_receivable" :props="props" class="number-cell">{{ formatAmount(props.row.checked_receivable) }}</q-td>
            <q-td key="unchecked_receivable" :props="props" class="number-cell">{{ formatAmount(props.row.unchecked_receivable) }}</q-td>
            <q-td key="checked_payable" :props="props" class="number-cell">{{ formatAmount(props.row.checked_payable) }}</q-td>
            <q-td key="unchecked_payable" :props="props" class="number-cell">{{ formatAmount(props.row.unchecked_payable) }}</q-td>
            <q-td key="checked_other" :props="props" class="number-cell">{{ formatAmount(props.row.checked_other) }}</q-td>
            <q-td key="unchecked_other" :props="props" class="number-cell">{{ formatAmount(props.row.unchecked_other) }}</q-td>
          </q-tr>
        </template>
        <template v-slot:bottom-row>
          <q-tr class="summary-row">
            <q-td auto-width>合计</q-td>
            <q-td />
            <q-td />
            <q-td />
            <q-td class="number-cell">{{ formatAmount(summary.checked_total) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.unchecked_total) }}</q-td>
            <q-td class="number-cell">{{ summary.total_count }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.checked_receivable) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.unchecked_receivable) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.checked_payable) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.unchecked_payable) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.checked_other) }}</q-td>
            <q-td class="number-cell">{{ formatAmount(summary.unchecked_other) }}</q-td>
          </q-tr>
        </template>
      </q-table>

      <div class="table-footer">
        <div class="footer-count">共 {{ filteredRows.length }} 条</div>
        <q-pagination
          v-model="current"
          color="primary"
          :max="maxPage"
          :max-pages="6"
          boundary-links
        />
      </div>
    </q-card>
  </div>
</template>

<script>
import { exportFile } from 'quasar'
import { getauth } from 'boot/axios_request'

export default {
  name: 'Pagecustomerdnlist',
  data () {
    return {
      loading: false,
      current: 1,
      pagination: {
        rowsPerPage: 12
      },
      sourceRows: [],
      selectedIds: [],
      filters: {
        organization: 'all',
        dateRange: '26-05-09~26-06-09',
        customerName: 'all'
      },
      tableFilters: {
        action: '',
        organization: '',
        customer_name: '',
        checked_total: '',
        unchecked_total: '',
        total_count: '',
        checked_receivable: '',
        unchecked_receivable: '',
        checked_payable: '',
        unchecked_payable: '',
        checked_other: '',
        unchecked_other: ''
      },
      columns: [
        { name: 'action', label: '操作', field: 'action', align: 'left' },
        { name: 'organization', label: '所属组织', field: 'organization', align: 'left' },
        { name: 'customer_name', label: '客户名称', field: 'customer_name', align: 'left' },
        { name: 'checked_total', label: '对账合计', field: 'checked_total', align: 'right' },
        { name: 'unchecked_total', label: '未对账合计', field: 'unchecked_total', align: 'right' },
        { name: 'total_count', label: '总单数', field: 'total_count', align: 'right' },
        { name: 'checked_receivable', label: '已结应收运输费合计', field: 'checked_receivable', align: 'right' },
        { name: 'unchecked_receivable', label: '未结应收运输费合计', field: 'unchecked_receivable', align: 'right' },
        { name: 'checked_payable', label: '已结应付运输费合计', field: 'checked_payable', align: 'right' },
        { name: 'unchecked_payable', label: '未结应付运输费合计', field: 'unchecked_payable', align: 'right' },
        { name: 'checked_other', label: '已结其他运输费合计', field: 'checked_other', align: 'right' },
        { name: 'unchecked_other', label: '未结其他运输费合计', field: 'unchecked_other', align: 'right' }
      ]
    }
  },
  computed: {
    allSelected: {
      get () {
        return this.pagedRows.length > 0 && this.pagedRows.every(row => this.selectedIds.includes(row.id))
      },
      set (value) {
        if (value) {
          const pageIds = this.pagedRows.map(row => row.id)
          this.selectedIds = Array.from(new Set(this.selectedIds.concat(pageIds)))
        } else {
          const pageIds = this.pagedRows.map(row => row.id)
          this.selectedIds = this.selectedIds.filter(id => !pageIds.includes(id))
        }
      }
    },
    organizationOptions () {
      const options = this.sourceRows.map(item => item.organization).filter(Boolean)
      return [{ label: '全部组织', value: 'all' }].concat(Array.from(new Set(options)).map(item => ({ label: item, value: item })))
    },
    customerOptions () {
      const options = this.sourceRows.map(item => item.customer_name).filter(Boolean)
      return [{ label: '全部客户', value: 'all' }].concat(Array.from(new Set(options)).map(item => ({ label: item, value: item })))
    },
    filteredRows () {
      return this.sourceRows.filter(row => {
        const matchesOrganization = this.filters.organization === 'all' || row.organization === this.filters.organization
        const matchesCustomer = this.filters.customerName === 'all' || row.customer_name === this.filters.customerName
        const matchesColumns = Object.entries(this.tableFilters).every(([key, value]) => {
          if (!value) return true
          return String(row[key] != null ? row[key] : '').includes(value)
        })
        return matchesOrganization && matchesCustomer && matchesColumns
      })
    },
    pagedRows () {
      const start = (this.current - 1) * this.pagination.rowsPerPage
      return this.filteredRows.slice(start, start + this.pagination.rowsPerPage)
    },
    maxPage () {
      const pages = Math.ceil(this.filteredRows.length / this.pagination.rowsPerPage)
      return pages > 0 ? pages : 1
    },
    summary () {
      return this.filteredRows.reduce((acc, item) => {
        acc.checked_total += Number(item.checked_total || 0)
        acc.unchecked_total += Number(item.unchecked_total || 0)
        acc.total_count += Number(item.total_count || 0)
        acc.checked_receivable += Number(item.checked_receivable || 0)
        acc.unchecked_receivable += Number(item.unchecked_receivable || 0)
        acc.checked_payable += Number(item.checked_payable || 0)
        acc.unchecked_payable += Number(item.unchecked_payable || 0)
        acc.checked_other += Number(item.checked_other || 0)
        acc.unchecked_other += Number(item.unchecked_other || 0)
        return acc
      }, {
        checked_total: 0,
        unchecked_total: 0,
        total_count: 0,
        checked_receivable: 0,
        unchecked_receivable: 0,
        checked_payable: 0,
        unchecked_payable: 0,
        checked_other: 0,
        unchecked_other: 0
      })
    }
  },
  methods: {
    formatAmount (value) {
      return Number(value || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    applyFilters () {
      this.current = 1
    },
    exportData () {
      const header = ['所属组织', '客户名称', '对账合计', '未对账合计', '总单数', '已结应收运输费合计', '未结应收运输费合计', '已结应付运输费合计', '未结应付运输费合计', '已结其他运输费合计', '未结其他运输费合计']
      const body = this.filteredRows.map(item => [
        item.organization,
        item.customer_name,
        item.checked_total,
        item.unchecked_total,
        item.total_count,
        item.checked_receivable,
        item.unchecked_receivable,
        item.checked_payable,
        item.unchecked_payable,
        item.checked_other,
        item.unchecked_other
      ])
      const content = [header].concat(body).map(line => line.join(',')).join('\r\n')
      exportFile('客户运单对账汇总.csv', '\ufeff' + content, 'text/csv')
    },
    buildSummaryRows (rows) {
      return Array.isArray(rows) ? rows : []
    },
    async getList () {
      this.loading = true
      try {
        if (this.$q.localStorage.has('auth')) {
          const res = await getauth('dn/reconcile/customer/summary/', {})
          this.sourceRows = this.buildSummaryRows(res)
        } else {
          this.sourceRows = []
        }
      } catch (err) {
        this.sourceRows = []
      } finally {
        this.loading = false
      }
    }
  },
  watch: {
    maxPage (value) {
      if (this.current > value) {
        this.current = value
      }
    }
  },
  created () {
    this.getList()
  }
}
</script>

<style scoped>
.finance-detail-page {
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
  min-width: 98px;
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

.finance-table :deep(.q-table) {
  table-layout: fixed;
}

.finance-table :deep(.q-table th) {
  white-space: nowrap;
  font-size: 12px;
}

.finance-table :deep(.q-table td) {
  white-space: nowrap;
}

.finance-table :deep(.q-table thead tr:first-child th) {
  border-top: 1px solid #d7dff0;
}

.finance-table :deep(.q-table tbody tr:hover) {
  background: #fafbff;
}

.finance-table :deep(.q-checkbox__inner) {
  font-size: 28px;
}

.filter-head-row :deep(.q-field__native),
.filter-head-row :deep(.q-field__input) {
  font-size: 12px;
}

.number-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: #2f3a52;
}

.summary-row {
  background: #fafbfd;
  font-weight: 700;
}

.summary-row :deep(td) {
  border-top: 1px solid #dfe5f2;
}

.table-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-head-row {
  background: #fbfcff;
}

.filter-head-label {
  color: #55657f;
  font-size: 12px;
}

.table-filter-input {
  min-width: 90px;
}

.table-filter-input :deep(.q-field__control) {
  min-height: 30px;
  background: #fff;
}

.footer-count {
  color: #6f7b92;
  font-size: 13px;
}

@media (max-width: 1200px) {
  .filter-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .table-toolbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 0;
  }

  .toolbar-left {
    padding: 8px 10px 10px;
  }
}

@media (max-width: 768px) {
  .filter-grid {
    grid-template-columns: 1fr;
  }

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
