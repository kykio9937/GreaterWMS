<template>
  <q-page class="change-log-page">
    <div class="page-card">
      <div class="panel-head">
        <div>
          <div class="panel-title">运单修改记录</div>
          <div class="panel-subtitle">展示待修改或已变更的运单记录，便于追踪运单调整情况</div>
        </div>
        <q-btn flat color="grey-7" label="刷新" @click="getList()" />
      </div>

      <div class="filter-bar">
        <q-input
          v-model="filter"
          dense
          outlined
          label="搜索运单号"
          @keyup.enter="getSearchList()"
        >
          <template v-slot:append>
            <q-icon name="search" class="cursor-pointer" @click="getSearchList()" />
          </template>
        </q-input>
      </div>

      <div class="table-scroll">
        <table class="change-table">
          <thead>
            <tr>
              <th>运单号</th>
              <th>货物编码</th>
              <th>货物名称</th>
              <th>数量</th>
              <th>重量</th>
              <th>体积</th>
              <th>客户</th>
              <th>创建人</th>
              <th>创建时间</th>
              <th>更新时间</th>
            </tr>
          </thead>
          <tbody v-if="tableList.length">
            <tr v-for="row in tableList" :key="row.id">
              <td>{{ row.dn_code }}</td>
              <td>{{ row.goods_code }}</td>
              <td>{{ row.goods_desc }}</td>
              <td>{{ row.goods_qty }}</td>
              <td>{{ row.goods_weight }}</td>
              <td>{{ row.goods_volume }}</td>
              <td>{{ row.customer }}</td>
              <td>{{ row.creater }}</td>
              <td>{{ formatDateTime(row.create_time) }}</td>
              <td>{{ formatDateTime(row.update_time) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!tableList.length" class="empty-block">暂无运单修改记录</div>
      </div>

      <div class="footer-bar">
        <div>共 {{ total }} 条</div>
        <div class="page-tools">
          <q-pagination
            v-if="max > 1"
            v-model="current"
            color="primary"
            :max="max"
            :max-pages="6"
            boundary-links
            @input="getList"
          />
          <input
            v-if="max > 1"
            v-model="paginationInput"
            class="page-input"
            @blur="changePageEnter"
            @keyup.enter="changePageEnter"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { getauth } from 'boot/axios_request'

export default {
  name: 'Pagednneworder',
  data () {
    return {
      pathname: 'dn/detail/?dn_status=2',
      loading: false,
      tableList: [],
      filter: '',
      current: 1,
      max: 0,
      total: 0,
      paginationInput: 1
    }
  },
  methods: {
    formatDateTime (value) {
      if (!value) {
        return '--'
      }
      return String(value).replace('T', ' ').slice(0, 16)
    },
    buildUrl () {
      const searchPart = this.filter ? `&dn_code__icontains=${encodeURIComponent(this.filter)}` : ''
      return `${this.pathname}${searchPart}&page=${this.current}`
    },
    updatePaging (count) {
      this.total = Number(count || 0)
      this.max = this.total <= 30 ? 0 : Math.ceil(this.total / 30)
      if (this.max === 0) {
        this.paginationInput = 1
      }
    },
    async getList () {
      if (!this.$q.localStorage.has('auth')) {
        return
      }
      this.loading = true
      try {
        const res = await getauth(this.buildUrl(), {})
        this.tableList = res.results || []
        this.updatePaging(res.count)
      } catch (err) {
        this.$q.notify({
          message: err.detail || '运单修改记录加载失败',
          icon: 'close',
          color: 'negative'
        })
      } finally {
        this.loading = false
      }
    },
    getSearchList () {
      this.current = 1
      this.paginationInput = 1
      this.getList()
    },
    changePageEnter () {
      if (Number(this.paginationInput) < 1) {
        this.current = 1
        this.paginationInput = 1
      } else if (this.max > 0 && Number(this.paginationInput) > this.max) {
        this.current = this.max
        this.paginationInput = this.max
      } else {
        this.current = Number(this.paginationInput) || 1
      }
      this.getList()
    }
  },
  created () {
    this.getList()
  }
}
</script>

<style scoped>
.change-log-page {
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

.filter-bar {
  margin: 18px 0 14px;
  max-width: 320px;
}

.table-scroll {
  overflow: auto;
  border: 1px solid #e5edf6;
  border-radius: 10px;
}

.change-table {
  width: 100%;
  min-width: 1120px;
  border-collapse: collapse;
}

.change-table th,
.change-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #edf2f7;
  white-space: nowrap;
  text-align: left;
  font-size: 13px;
}

.change-table th {
  position: sticky;
  top: 0;
  background: #f8fbff;
  color: #27486f;
  z-index: 1;
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

.page-tools {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-input {
  width: 60px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d0d9ea;
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 900px) {
  .panel-head,
  .footer-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-bar {
    max-width: none;
  }
}
</style>
