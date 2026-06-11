<template>
  <q-page class="audit-page">
    <div class="page-card">
      <div class="panel-head">
        <div>
          <div class="panel-title">运单审核</div>
          <div class="panel-subtitle">审核数据直接从运单列表读取，并回写审核状态</div>
        </div>
        <q-btn flat color="grey-7" label="刷新" @click="getList()" />
      </div>

      <div class="summary-strip">
        <div class="summary-box">
          <div class="summary-label">待审核</div>
          <div class="summary-value">{{ pendingCount }}</div>
        </div>
        <div class="summary-box">
          <div class="summary-label">已审核</div>
          <div class="summary-value">{{ approvedCount }}</div>
        </div>
        <div class="summary-box">
          <div class="summary-label">当前页合计金额</div>
          <div class="summary-value">¥{{ visibleIncome }}</div>
        </div>
      </div>

      <div class="filter-grid">
        <q-input v-model="filter.keyword" dense outlined label="运单号 / 客户 / 货物" />
        <q-select
          v-model="filter.audit_status"
          dense
          outlined
          emit-value
          map-options
          label="审核状态"
          :options="auditOptions"
        />
        <q-btn unelevated color="primary" label="查询" />
        <q-btn flat color="grey-7" label="重置" @click="resetFilter()" />
      </div>

      <div class="table-scroll">
        <table class="audit-table">
          <thead>
            <tr>
              <th>序号</th>
              <th>运单号</th>
              <th>客户名称</th>
              <th>货物名称</th>
              <th>车牌号</th>
              <th>到车运费</th>
              <th>承运成本</th>
              <th>审核状态</th>
              <th>审核备注</th>
              <th>开单时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody v-if="displayRows.length">
            <tr v-for="(row, index) in displayRows" :key="row.id">
              <td>{{ row.row_index || index + 1 }}</td>
              <td>{{ row.dn_code }}</td>
              <td>{{ row.customer }}</td>
              <td>{{ row.goods_name }}</td>
              <td>{{ row.plate_number }}</td>
              <td>{{ money(row.freight_amount) }}</td>
              <td>{{ money(row.transport_cost) }}</td>
              <td>
                <span :class="['badge-lite', row.audit_status === '已审核' ? 'badge-green' : 'badge-orange']">
                  {{ row.audit_status }}
                </span>
              </td>
              <td>{{ row.audit_remark || '--' }}</td>
              <td>{{ row.create_time }}</td>
              <td class="action-cell">
                <button class="text-link" @click="openAuditDialog(row, 'approved')">审核通过</button>
                <button class="text-link danger" @click="openAuditDialog(row, 'rejected')">退回修改</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!displayRows.length" class="empty-block">暂无需要审核的运单</div>
      </div>

      <div class="footer-bar">
        <div>共 {{ total }} 条</div>
        <q-pagination
          v-model="current"
          color="primary"
          :max="max"
          :max-pages="6"
          boundary-links
          @input="getList"
        />
      </div>
    </div>

    <q-dialog v-model="auditDialog.visible">
      <q-card class="audit-dialog">
        <q-card-section class="dialog-title">
          {{ auditDialog.mode === 'approved' ? '审核通过' : '退回修改' }}
        </q-card-section>
        <q-card-section>
          <div class="dialog-tip">运单号：{{ auditDialog.row ? auditDialog.row.dn_code : '--' }}</div>
          <q-input v-model="auditDialog.remark" dense outlined type="textarea" rows="4" label="审核备注" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="取消" v-close-popup />
          <q-btn color="primary" label="确认" @click="submitAudit()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { getauth, patchauth } from 'boot/axios_request'
import Bus from 'boot/bus.js'

export default {
  name: 'WaybillAuditPage',
  data () {
    return {
      current: 1,
      max: 1,
      total: 0,
      rawRows: [],
      filter: {
        keyword: '',
        audit_status: 'all'
      },
      auditOptions: [
        { label: '全部', value: 'all' },
        { label: '待审核', value: '待审核' },
        { label: '已审核', value: '已审核' },
        { label: '退回修改', value: '退回修改' }
      ],
      auditDialog: {
        visible: false,
        mode: 'approved',
        row: null,
        remark: ''
      }
    }
  },
  computed: {
    displayRows () {
      return this.rawRows.filter(row => {
        const keyword = this.filter.keyword.trim()
        const matchKeyword = !keyword || [row.dn_code, row.customer, row.goods_name].some(item => String(item || '').includes(keyword))
        const matchAudit = this.filter.audit_status === 'all' || row.audit_status === this.filter.audit_status
        return matchKeyword && matchAudit
      })
    },
    pendingCount () {
      return this.rawRows.filter(item => item.audit_status === '待审核').length
    },
    approvedCount () {
      return this.rawRows.filter(item => item.audit_status === '已审核').length
    },
    visibleIncome () {
      return this.displayRows.reduce((sum, item) => sum + Number(item.freight_amount || 0), 0).toFixed(2)
    }
  },
  methods: {
    money (value) {
      return Number(value || 0).toFixed(2)
    },
    mapRow (row, index) {
      const fee = row.transportation_fee || {}
      return {
        ...row,
        row_index: (this.current - 1) * 30 + index + 1,
        goods_name: fee.goods_name || '标准普货',
        plate_number: fee.plate_number || '--',
        freight_amount: fee.business_income || row.total_cost || 0,
        transport_cost: fee.carrier_cost || 0,
        audit_status: fee.audit_status || '待审核',
        audit_remark: fee.audit_remark || ''
      }
    },
    async getList () {
      try {
        const res = await getauth(`dn/list/?page=${this.current}`)
        this.total = Number(res.count || 0)
        this.max = Math.max(1, Math.ceil(this.total / 30))
        this.rawRows = (res.results || []).map((item, index) => this.mapRow(item, index))
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: err.detail || '运单审核列表加载失败'
        })
        this.rawRows = []
      }
    },
    resetFilter () {
      this.filter = {
        keyword: '',
        audit_status: 'all'
      }
    },
    openAuditDialog (row, mode) {
      this.auditDialog = {
        visible: true,
        mode,
        row,
        remark: row.audit_remark || ''
      }
    },
    async submitAudit () {
      if (!this.auditDialog.row) {
        return
      }
      const row = this.auditDialog.row
      const fee = Object.assign({}, row.transportation_fee || {})
      fee.audit_status = this.auditDialog.mode === 'approved' ? '已审核' : '退回修改'
      fee.audit_remark = this.auditDialog.remark || (this.auditDialog.mode === 'approved' ? '审核通过' : '请按审核意见调整')
      try {
        await patchauth(`dn/list/${row.id}/`, {
          transportation_fee: fee
        })
        this.$q.notify({
          type: 'positive',
          message: '审核状态已更新'
        })
        this.auditDialog.visible = false
        Bus.$emit('waybillChanged', { type: 'audit', id: row.id })
        this.getList()
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: err.detail || '审核保存失败'
        })
      }
    },
    handleWaybillChanged () {
      this.getList()
    }
  },
  created () {
    this.getList()
  },
  mounted () {
    Bus.$on('waybillChanged', this.handleWaybillChanged)
  },
  beforeDestroy () {
    Bus.$off('waybillChanged', this.handleWaybillChanged)
  }
}
</script>

<style scoped>
.audit-page {
  padding: 12px;
  background: #f5f7fb;
}

.page-card {
  background: #fff;
  border: 1px solid #d8e1ef;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 24px rgba(16, 37, 63, 0.06);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.panel-title {
  font-size: 22px;
  font-weight: 700;
  color: #1b365d;
}

.panel-subtitle {
  margin-top: 6px;
  font-size: 13px;
  color: #70839b;
}

.summary-strip {
  margin: 18px 0 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.summary-box {
  padding: 14px;
  border: 1px solid #e5edf6;
  border-radius: 10px;
  background: #f8fbff;
}

.summary-label {
  font-size: 12px;
  color: #6f839b;
}

.summary-value {
  margin-top: 8px;
  font-size: 22px;
  font-weight: 700;
  color: #1b365d;
}

.filter-grid {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr auto auto;
  gap: 12px;
  margin-bottom: 14px;
}

.table-scroll {
  overflow: auto;
  border: 1px solid #e5edf6;
  border-radius: 10px;
}

.audit-table {
  width: 100%;
  min-width: 1180px;
  border-collapse: collapse;
}

.audit-table th,
.audit-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #edf2f7;
  white-space: nowrap;
  text-align: left;
  font-size: 13px;
}

.audit-table th {
  position: sticky;
  top: 0;
  background: #f8fbff;
  color: #27486f;
  z-index: 1;
}

.action-cell {
  display: flex;
  gap: 10px;
}

.text-link {
  border: 0;
  background: transparent;
  color: #1c63b8;
  cursor: pointer;
  padding: 0;
}

.text-link.danger {
  color: #d44b43;
}

.badge-lite {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.badge-green {
  background: #e8f7ee;
  color: #2f8f52;
}

.badge-orange {
  background: #fff3df;
  color: #d28b21;
}

.empty-block {
  padding: 40px 12px;
  text-align: center;
  color: #7c8ea6;
}

.footer-bar {
  margin-top: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.audit-dialog {
  width: 460px;
  max-width: calc(100vw - 24px);
}

.dialog-title {
  font-size: 18px;
  font-weight: 700;
}

.dialog-tip {
  margin-bottom: 12px;
  color: #57708d;
}

@media (max-width: 900px) {
  .summary-strip,
  .filter-grid {
    grid-template-columns: 1fr;
  }

  .panel-head,
  .footer-bar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
