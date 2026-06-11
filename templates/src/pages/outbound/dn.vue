<template>
  <q-page class="waybill-list-page">
    <div class="page-card">
      <div class="panel-head">
        <div>
          <div class="panel-title">运单列表</div>
          <div class="panel-subtitle">只保留核心运单字段、修改和删除操作</div>
        </div>
        <div class="panel-actions">
          <q-btn color="primary" label="创建运单" @click="$router.push({ name: 'createwaybill' })" />
          <q-btn flat color="grey-7" label="刷新" @click="getList()" />
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
        <q-select
          v-model="filter.dn_status"
          dense
          outlined
          emit-value
          map-options
          label="运单状态"
          :options="statusOptions"
        />
        <div class="filter-buttons">
          <q-btn unelevated color="primary" label="查询" @click="applyFilter()" />
          <q-btn flat color="grey-7" label="重置" @click="resetFilter()" />
        </div>
      </div>

      <div class="table-scroll">
        <table class="waybill-table">
          <thead>
            <tr>
              <th>序号</th>
              <th>操作</th>
              <th>审核状态</th>
              <th>运单号</th>
              <th>客户名称</th>
              <th>货物名称</th>
              <th>车线名称</th>
              <th>所属组织</th>
              <th>派单员</th>
              <th>车牌号</th>
              <th>到车运费</th>
              <th>承运成本</th>
              <th>运单状态</th>
              <th>开单时间</th>
            </tr>
          </thead>
          <tbody v-if="displayRows.length">
            <tr v-for="(row, index) in displayRows" :key="row.id">
              <td>{{ row.row_index || index + 1 }}</td>
              <td class="action-cell">
                <button class="text-link" @click="editData(row)">修改运单</button>
                <button class="text-link danger" @click="deleteData(row)">删除</button>
              </td>
              <td>
                <span :class="['badge-lite', row.audit_status === '已审核' ? 'badge-green' : 'badge-orange']">
                  {{ row.audit_status }}
                </span>
              </td>
              <td>{{ row.dn_code }}</td>
              <td>{{ row.customer }}</td>
              <td>{{ row.goods_name }}</td>
              <td>{{ row.line_name }}</td>
              <td>{{ row.organization }}</td>
              <td>{{ row.dispatcher }}</td>
              <td>{{ row.plate_number }}</td>
              <td>{{ money(row.freight_amount) }}</td>
              <td>{{ money(row.transport_cost) }}</td>
              <td>{{ row.dn_status_label }}</td>
              <td>{{ row.create_time }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!displayRows.length" class="empty-block">暂无运单数据</div>
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
  </q-page>
</template>

<script>
import { deleteauth, getauth } from 'boot/axios_request'
import Bus from 'boot/bus.js'

const STATUS_LABEL_MAP = {
  1: '待受理',
  2: '待受理',
  3: '已受理',
  4: '已受理',
  5: '运输中',
  6: '已完成'
}

export default {
  name: 'WaybillListPage',
  data () {
    return {
      loading: false,
      current: 1,
      max: 1,
      total: 0,
      rawRows: [],
      filter: {
        keyword: '',
        audit_status: 'all',
        dn_status: 'all'
      },
      auditOptions: [
        { label: '全部', value: 'all' },
        { label: '待审核', value: '待审核' },
        { label: '已审核', value: '已审核' }
      ],
      statusOptions: [
        { label: '全部', value: 'all' },
        { label: '待受理', value: '待受理' },
        { label: '已受理', value: '已受理' },
        { label: '运输中', value: '运输中' },
        { label: '已完成', value: '已完成' }
      ]
    }
  },
  computed: {
    displayRows () {
      return this.rawRows.filter(row => {
        const keyword = this.filter.keyword.trim()
        const matchKeyword = !keyword || [row.dn_code, row.customer, row.goods_name].some(item => String(item || '').includes(keyword))
        const matchAudit = this.filter.audit_status === 'all' || row.audit_status === this.filter.audit_status
        const matchStatus = this.filter.dn_status === 'all' || row.dn_status_label === this.filter.dn_status
        return matchKeyword && matchAudit && matchStatus
      })
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
        line_name: fee.line_name || `${row.customer || '默认客户'}干线`,
        organization: fee.organization || '西安莲湖白桦',
        dispatcher: fee.dispatcher || row.creater || '--',
        plate_number: fee.plate_number || '--',
        freight_amount: fee.business_income || row.total_cost || 0,
        transport_cost: fee.carrier_cost || 0,
        audit_status: fee.audit_status || '待审核',
        dn_status_label: STATUS_LABEL_MAP[row.dn_status] || '待受理'
      }
    },
    async getList () {
      this.loading = true
      try {
        const res = await getauth(`dn/list/?page=${this.current}`)
        this.total = Number(res.count || 0)
        this.max = Math.max(1, Math.ceil(this.total / 30))
        this.rawRows = (res.results || []).map((item, index) => this.mapRow(item, index))
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: err.detail || '运单列表加载失败，资源不存在'
        })
        this.rawRows = []
        this.total = 0
        this.max = 1
      } finally {
        this.loading = false
      }
    },
    applyFilter () {},
    resetFilter () {
      this.filter = {
        keyword: '',
        audit_status: 'all',
        dn_status: 'all'
      }
    },
    editData (row) {
      this.$router.push({
        name: 'createwaybill',
        query: {
          mode: 'edit',
          id: row.id
        }
      })
    },
    async deleteData (row) {
      this.$q.dialog({
        title: '删除确认',
        message: `确认删除运单 ${row.dn_code} 吗？`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await deleteauth(`dn/list/${row.id}/`)
          this.$q.notify({
            type: 'positive',
            message: '运单删除成功'
          })
          this.getList()
        } catch (err) {
          this.$q.notify({
            type: 'negative',
            message: err.detail || '运单删除失败'
          })
        }
      })
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
.waybill-list-page {
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
  gap: 16px;
  align-items: flex-start;
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

.panel-actions {
  display: flex;
  gap: 10px;
}

.filter-grid {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr 0.8fr auto;
  gap: 12px;
  margin: 18px 0 14px;
}

.filter-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-scroll {
  overflow: auto;
  border: 1px solid #e5edf6;
  border-radius: 10px;
}

.waybill-table {
  width: 100%;
  min-width: 1320px;
  border-collapse: collapse;
}

.waybill-table th,
.waybill-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #edf2f7;
  white-space: nowrap;
  text-align: left;
  font-size: 13px;
}

.waybill-table th {
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

@media (max-width: 900px) {
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
