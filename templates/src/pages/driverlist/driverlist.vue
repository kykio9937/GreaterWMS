<template>
  <div class="tracking-page">
    <q-card flat bordered class="filter-card">
      <div class="filter-grid">
        <q-select
          v-model="filters.keywordType"
          outlined
          dense
          emit-value
          map-options
          :options="keywordTypeOptions"
          label="运单 / 事件类型"
        />
        <q-input
          v-model="filters.keyword"
          outlined
          dense
          clearable
          label="关键字"
          placeholder="支持运单号 / 客户 / 车牌 / 路线"
          @keyup.enter="applyFilters"
        />
        <q-select
          v-model="filters.status"
          outlined
          dense
          emit-value
          map-options
          :options="statusOptions"
          label="运单状态"
        />
        <q-input
          v-model="filters.dateRange"
          outlined
          dense
          clearable
          label="创建时间"
          placeholder="如：2026-06-09"
          @keyup.enter="applyFilters"
        />
        <q-select
          v-model="filters.eventType"
          outlined
          dense
          emit-value
          map-options
          :options="eventTypeOptions"
          label="事件类型"
        />
        <q-select
          v-model="filters.eventStatus"
          outlined
          dense
          emit-value
          map-options
          :options="eventStatusOptions"
          label="事件状态"
        />
        <div class="filter-actions">
          <q-btn unelevated color="primary" icon="search" label="查询" @click="applyFilters" />
          <q-btn flat color="grey-7" label="重置" @click="resetFilters" />
        </div>
      </div>
    </q-card>

    <div class="stats-row">
      <q-card
        v-for="card in summaryCards"
        :key="card.key"
        flat
        bordered
        class="stat-card"
      >
        <div class="stat-label">{{ card.label }}</div>
        <div class="stat-value">
          <span>{{ card.value }}</span>
          <small>单</small>
        </div>
      </q-card>
    </div>

    <q-card flat bordered class="table-card">
      <div class="table-toolbar">
        <div class="table-title">
          <div class="table-title-main">在线跟踪</div>
          <div class="table-title-sub">按照运单实时展示在途位置、监控报警和进度信息</div>
        </div>
        <div class="table-toolbar-actions">
          <q-btn flat color="primary" icon="settings" label="客户直单配置" />
          <q-btn outline color="primary" icon="file_download" label="导出" @click="exportData" />
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
        class="tracking-table"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width>
              <q-checkbox v-model="allSelected" color="primary" size="sm" />
            </q-th>
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              {{ col.label }}
            </q-th>
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
              <q-checkbox
                v-model="selectedIds"
                :val="props.row.id"
                color="primary"
                size="sm"
              />
            </q-td>
            <q-td key="waybill_no" :props="props">
              <div class="waybill-code">{{ props.row.waybill_no }}</div>
            </q-td>
            <q-td key="order_no" :props="props">{{ props.row.order_no }}</q-td>
            <q-td key="customer_name" :props="props">{{ props.row.customer_name }}</q-td>
            <q-td key="line_name" :props="props">{{ props.row.line_name }}</q-td>
            <q-td key="waybill_status" :props="props">
              <div class="status-pill">
                <span class="status-dot" />
                <span>{{ props.row.waybill_status }}</span>
              </div>
            </q-td>
            <q-td key="waybill_tags" :props="props">
              <div class="tag-row">
                <span
                  v-for="tag in props.row.waybill_tags"
                  :key="tag.text"
                  class="mini-tag"
                  :class="`mini-tag--${tag.tone}`"
                >
                  {{ tag.text }}
                </span>
              </div>
            </q-td>
            <q-td key="plate_number" :props="props">
              <div class="plate-wrap">
                <span class="plate-text">{{ props.row.plate_number }}</span>
                <span class="plate-badge">G7</span>
              </div>
            </q-td>
            <q-td key="location_track" :props="props">
              <div class="location-wrap">
                <q-icon :name="props.row.location_icon" :color="props.row.location_color" size="16px" />
                <span class="ellipsis-text">{{ props.row.location_track }}</span>
              </div>
            </q-td>
            <q-td key="monitor_alarm" :props="props">
              <span :class="['alarm-text', { 'alarm-text--warn': props.row.monitor_alarm !== '正常' }]">
                {{ props.row.monitor_alarm }}
              </span>
            </q-td>
            <q-td key="mileage_progress" :props="props">
              <div class="progress-cell">
                <span class="progress-number">{{ props.row.mileage_progress }}%</span>
                <q-linear-progress
                  size="8px"
                  rounded
                  :value="props.row.mileage_progress / 100"
                  color="grey-5"
                  track-color="grey-3"
                  class="progress-bar"
                />
                <q-btn flat dense color="primary" label="详情" class="detail-link" />
              </div>
            </q-td>
            <q-td key="temperature" :props="props">{{ props.row.temperature }}</q-td>
            <q-td key="humidity" :props="props">{{ props.row.humidity }}</q-td>
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

const LOCATION_PATTERNS = [
  { text: '开封市祥符区X013 X013', icon: 'navigation', color: 'primary' },
  { text: '无锡市江阴市S122花园路', icon: 'place', color: 'positive' },
  { text: '濮阳市濮阳县101省道', icon: 'room', color: 'teal' },
  { text: '咸阳市泾阳县中张镇运通线', icon: 'explore', color: 'deep-orange' },
  { text: '六安市霍邱县曹庙镇105国道', icon: 'near_me', color: 'indigo' }
]

export default {
  name: 'Pagedriverlist',
  data () {
    return {
      loading: false,
      sourceRows: [],
      current: 1,
      selectedIds: [],
      pagination: {
        rowsPerPage: 12
      },
      filters: {
        keywordType: 'waybill',
        keyword: '',
        status: 'all',
        dateRange: '',
        eventType: 'all',
        eventStatus: 'all'
      },
      tableFilters: {
        waybill_no: '',
        order_no: '',
        customer_name: '',
        line_name: '',
        waybill_status: '',
        waybill_tags: '',
        plate_number: '',
        location_track: '',
        monitor_alarm: '',
        mileage_progress: '',
        temperature: '',
        humidity: ''
      },
      keywordTypeOptions: [
        { label: '运单', value: 'waybill' },
        { label: '事件类型', value: 'event' }
      ],
      statusOptions: [
        { label: '全部', value: 'all' },
        { label: '已装车', value: '已装车' },
        { label: '运输中', value: '运输中' },
        { label: '待签收', value: '待签收' },
        { label: '已签收', value: '已签收' }
      ],
      eventTypeOptions: [
        { label: '全部', value: 'all' },
        { label: '定位跟踪', value: '定位跟踪' },
        { label: '偏移报警', value: '偏移报警' },
        { label: '停车报警', value: '停车报警' },
        { label: '设备状态', value: '设备状态' }
      ],
      eventStatusOptions: [
        { label: '全部', value: 'all' },
        { label: '正常', value: '正常' },
        { label: '预警', value: '预警' },
        { label: '离线', value: '离线' }
      ],
      columns: [
        { name: 'waybill_no', label: '运单', field: 'waybill_no', align: 'left' },
        { name: 'order_no', label: '订单编号', field: 'order_no', align: 'left' },
        { name: 'customer_name', label: '客户名称', field: 'customer_name', align: 'left' },
        { name: 'line_name', label: '车线名称', field: 'line_name', align: 'left' },
        { name: 'waybill_status', label: '运单状态', field: 'waybill_status', align: 'left' },
        { name: 'waybill_tags', label: '运单标识', field: 'waybill_tags', align: 'left' },
        { name: 'plate_number', label: '车牌号', field: 'plate_number', align: 'left' },
        { name: 'location_track', label: '位置跟踪', field: 'location_track', align: 'left' },
        { name: 'monitor_alarm', label: '监控报警', field: 'monitor_alarm', align: 'left' },
        { name: 'mileage_progress', label: '里程进度', field: 'mileage_progress', align: 'left' },
        { name: 'temperature', label: '实时温度', field: 'temperature', align: 'center' },
        { name: 'humidity', label: '实时湿度(%RH)', field: 'humidity', align: 'center' }
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
    mappedRows () {
      return this.sourceRows.map((row, index) => this.buildDisplayRow(row, index))
    },
    filteredRows () {
      return this.mappedRows.filter(row => {
        const keyword = this.filters.keyword.trim()
        const matchesKeyword = !keyword || [
          row.waybill_no,
          row.order_no,
          row.customer_name,
          row.line_name,
          row.plate_number
        ].some(item => String(item || '').includes(keyword))
        const matchesStatus = this.filters.status === 'all' || row.waybill_status === this.filters.status
        const matchesDate = !this.filters.dateRange || String(row.create_time || '').includes(this.filters.dateRange)
        const matchesEventType = this.filters.eventType === 'all' || row.event_type === this.filters.eventType
        const matchesEventStatus = this.filters.eventStatus === 'all' || row.event_status === this.filters.eventStatus
        const matchesColumns = Object.entries(this.tableFilters).every(([key, value]) => {
          if (!value) {
            return true
          }
          const cellValue = key === 'waybill_tags'
            ? row.waybill_tags.map(tag => tag.text).join('')
            : row[key]
          return String(cellValue || '').includes(value)
        })
        return matchesKeyword && matchesStatus && matchesDate && matchesEventType && matchesEventStatus && matchesColumns
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
    summaryCards () {
      const rows = this.filteredRows
      return [
        { key: 'total', label: '实时统计', value: rows.length },
        { key: 'offset', label: '线路偏移', value: rows.filter(item => item.event_type === '偏移报警').length },
        { key: 'parking', label: '超时停车', value: rows.filter(item => item.monitor_alarm === '超时停车').length },
        { key: 'highway-stop', label: '高速异常停车', value: rows.filter(item => item.monitor_alarm === '高速异常停车').length },
        { key: 'jam', label: '高速拥堵', value: rows.filter(item => item.event_type === '路况拥堵').length },
        { key: 'offline', label: '设备离线', value: rows.filter(item => item.event_status === '离线').length },
        { key: 'overspeed', label: '超速报警', value: rows.filter(item => item.monitor_alarm === '超速报警').length }
      ]
    }
  },
  methods: {
    normalizeStatus (status) {
      if (status === 1 || status === '1') return '待调度'
      if (status === 2 || status === '2') return '待装车'
      if (status === 3 || status === '3') return '待发车'
      if (status === 4 || status === '4') return '待出库'
      if (status === 5 || status === '5') return '运输中'
      if (status === 6 || status === '6') return '已签收'
      return status || '运输中'
    },
    buildDisplayRow (row, index) {
      const location = LOCATION_PATTERNS[index % LOCATION_PATTERNS.length]
      const progress = [0, 0, 12, 28, 45, 66, 80, 93][index % 8]
      const eventTypes = ['定位跟踪', '定位跟踪', '偏移报警', '停车报警', '设备状态', '路况拥堵']
      const eventStatuses = ['正常', '正常', '预警', '正常', '离线', '预警']
      const alarms = ['正常', '正常', '正常', '超时停车', '高速异常停车', '超速报警']
      const plate = row.plate_number || row.vehicle_no || `冀RP${7800 + index}`
      const tags = [
        { text: '普', tone: 'primary' },
        { text: index % 3 === 0 ? '改' : '绑', tone: index % 3 === 0 ? 'info' : 'accent' }
      ]

      return {
        id: row.id || index + 1,
        create_time: row.create_time || '',
        waybill_no: row.dn_code || row.waybill_no || `89${String(index + 1).padStart(16, '0')}`,
        order_no: row.order_no || `${plate}${String(index + 1).padStart(6, '0')}`,
        customer_name: row.customer || row.customer_name || '西安莲湖',
        line_name: row.line_name || `${row.customer || '西安莲湖'}干线`,
        waybill_status: row.waybill_status || this.normalizeStatus(row.dn_status),
        waybill_tags: tags,
        plate_number: plate,
        location_track: row.location_track || location.text,
        location_icon: location.icon,
        location_color: location.color,
        monitor_alarm: row.monitor_alarm || alarms[index % alarms.length],
        mileage_progress: row.mileage_progress != null ? Number(row.mileage_progress) : progress,
        temperature: row.temperature || (index % 4 === 0 ? '4.2°C' : '--'),
        humidity: row.humidity || (index % 4 === 0 ? '67' : '--'),
        event_type: row.event_type || eventTypes[index % eventTypes.length],
        event_status: row.event_status || eventStatuses[index % eventStatuses.length]
      }
    },
    applyFilters () {
      this.current = 1
    },
    resetFilters () {
      this.filters = {
        keywordType: 'waybill',
        keyword: '',
        status: 'all',
        dateRange: '',
        eventType: 'all',
        eventStatus: 'all'
      }
      this.tableFilters = {
        waybill_no: '',
        order_no: '',
        customer_name: '',
        line_name: '',
        waybill_status: '',
        waybill_tags: '',
        plate_number: '',
        location_track: '',
        monitor_alarm: '',
        mileage_progress: '',
        temperature: '',
        humidity: ''
      }
      this.current = 1
    },
    exportData () {
      const rows = this.filteredRows
      const header = ['运单', '订单编号', '客户名称', '车线名称', '运单状态', '车牌号', '位置跟踪', '监控报警', '里程进度', '实时温度', '实时湿度(%RH)']
      const body = rows.map(item => [
        item.waybill_no,
        item.order_no,
        item.customer_name,
        item.line_name,
        item.waybill_status,
        item.plate_number,
        item.location_track,
        item.monitor_alarm,
        `${item.mileage_progress}%`,
        item.temperature,
        item.humidity
      ])
      const content = [header].concat(body).map(line => line.join(',')).join('\r\n')
      exportFile('在途在线跟踪.csv', '\ufeff' + content, 'text/csv')
    },
    async getList () {
      this.loading = true
      try {
        if (this.$q.localStorage.has('auth')) {
          const res = await getauth('dn/transit/', {})
          this.sourceRows = Array.isArray(res) ? res : []
        } else {
          this.sourceRows = []
        }
      } catch (err) {
        this.sourceRows = []
        this.$q.notify({
          message: '在途运单数据暂不可用',
          icon: 'warning',
          color: 'orange'
        })
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
.tracking-page {
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
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
  align-items: center;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 10px;
}

.stat-card {
  padding: 14px 16px;
  border-radius: 14px;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: #31415f;
}

.stat-value {
  margin-top: 10px;
  color: #ff4d4f;
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}

.stat-value small {
  margin-left: 4px;
  font-size: 14px;
  color: #5f6880;
}

.table-card {
  overflow: auto;
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px 10px;
}

.table-title-main {
  font-size: 16px;
  font-weight: 700;
  color: #1f2a44;
}

.table-title-sub {
  margin-top: 4px;
  font-size: 12px;
  color: #7d889f;
}

.table-toolbar-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tracking-table :deep(.q-table thead tr) {
  background: #f6f8fc;
}

.tracking-table :deep(.q-table th) {
  color: #2b3d59;
  font-weight: 700;
}

.filter-head-row {
  background: #fbfcff;
}

.filter-head-label {
  color: #55657f;
  font-size: 12px;
}

.table-filter-input {
  min-width: 88px;
}

.table-filter-input :deep(.q-field__control) {
  min-height: 30px;
  background: #fff;
}

.tracking-table :deep(.q-table td),
.tracking-table :deep(.q-table th) {
  padding: 10px 8px;
}

.waybill-code {
  color: #1890ff;
  font-weight: 600;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #ff8f1f;
  font-weight: 600;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff9800;
}

.tag-row {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.mini-tag {
  min-width: 22px;
  padding: 2px 5px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.2;
  text-align: center;
}

.mini-tag--primary {
  background: #2f80ff;
  color: #fff;
}

.mini-tag--accent {
  background: #eef5ff;
  color: #2f80ff;
  border: 1px solid #cfe0ff;
}

.mini-tag--info {
  background: #eff7ff;
  color: #5a8dee;
  border: 1px solid #bfd3ff;
}

.plate-wrap {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.plate-text {
  color: #1e88e5;
  font-weight: 600;
}

.plate-badge {
  padding: 1px 5px;
  border-radius: 4px;
  background: #6f2cff;
  color: #fff;
  font-size: 11px;
}

.location-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 150px;
}

.ellipsis-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.alarm-text {
  color: #8a94ab;
}

.alarm-text--warn {
  color: #f59e0b;
  font-weight: 600;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 180px;
}

.progress-number {
  width: 28px;
  color: #1f2a44;
}

.progress-bar {
  flex: 1;
  min-width: 78px;
}

.detail-link {
  min-height: auto;
  padding: 0;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.footer-count {
  color: #6f7b92;
  font-size: 13px;
}

@media (max-width: 1600px) {
  .filter-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .stats-row {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 960px) {
  .filter-grid {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    justify-content: flex-start;
  }

  .stats-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .table-toolbar,
  .table-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .tracking-table {
    overflow-x: auto;
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .table-toolbar,
  .table-footer,
  .filter-actions,
  .table-toolbar-actions {
    width: 100%;
  }

  .table-toolbar-actions {
    justify-content: flex-start;
  }

  .location-wrap,
  .progress-cell {
    min-width: 0;
  }
}
</style>
