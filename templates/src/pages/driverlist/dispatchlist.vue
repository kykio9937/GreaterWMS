<template>
  <div class="fee-page">
    <div class="fee-summary">
      <q-card v-for="card in feeCards" :key="card.label" flat bordered class="fee-card">
        <div class="fee-card__label">{{ card.label }}</div>
        <div class="fee-card__value">{{ card.value }}</div>
        <div class="fee-card__desc">{{ card.desc }}</div>
      </q-card>
    </div>

    <q-card flat bordered class="fee-table-card">
      <div class="fee-table-head">
        <div>
          <div class="fee-title">在途费用</div>
          <div class="fee-subtitle">按运单查看运输费用、奖励、异常和结算状态</div>
        </div>
        <q-btn outline color="primary" icon="file_download" label="导出费用表" @click="exportData" />
      </div>

      <q-table
        flat
        :data="rows"
        :columns="columns"
        row-key="id"
        hide-bottom
      />
    </q-card>
  </div>
</template>

<script>
import { exportFile } from 'quasar'
import { getauth } from 'boot/axios_request'

export default {
  name: 'Pagedispatchlist',
  data () {
    return {
      rows: [],
      columns: [
        { name: 'dn_code', label: '运单编号', field: 'dn_code', align: 'left' },
        { name: 'customer', label: '客户名称', field: 'customer', align: 'left' },
        { name: 'line_name', label: '车线名称', field: 'line_name', align: 'left' },
        { name: 'freight', label: '运输费用', field: 'freight', align: 'right' },
        { name: 'reward', label: '司机奖励', field: 'reward', align: 'right' },
        { name: 'exception_fee', label: '异常费用', field: 'exception_fee', align: 'right' },
        { name: 'settle_status', label: '结算状态', field: 'settle_status', align: 'center' }
      ]
    }
  },
  computed: {
    feeCards () {
      const parseAmount = value => Number(String(value || 0).replace(/,/g, ''))
      const totalFreight = this.rows.reduce((sum, item) => sum + parseAmount(item.freight), 0).toFixed(2)
      const totalReward = this.rows.reduce((sum, item) => sum + parseAmount(item.reward), 0).toFixed(2)
      const totalException = this.rows.reduce((sum, item) => sum + parseAmount(item.exception_fee), 0).toFixed(2)
      return [
        { label: '在途运费', value: `¥ ${totalFreight}`, desc: '当前在途运单累计运费' },
        { label: '司机奖励', value: `¥ ${totalReward}`, desc: '按在途计划同步奖励金额' },
        { label: '异常费用', value: `¥ ${totalException}`, desc: '包含停车、绕路等异常费用' }
      ]
    }
  },
  methods: {
    formatAmount (value) {
      return Number(value || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    async getList () {
      try {
        if (this.$q.localStorage.has('auth')) {
          const res = await getauth('dn/transit/', {})
          this.rows = (Array.isArray(res) ? res : []).map(item => ({
            id: item.id,
            dn_code: item.dn_code,
            customer: item.customer,
            line_name: item.line_name,
            freight: this.formatAmount(item.carrier_cost),
            reward: this.formatAmount(item.reward_fee),
            exception_fee: this.formatAmount(item.other_fee),
            settle_status: item.carrier_reconcile_status
          }))
        } else {
          this.rows = []
        }
      } catch (err) {
        this.rows = []
        this.$q.notify({
          message: '在途费用数据暂不可用',
          icon: 'warning',
          color: 'orange'
        })
      }
    },
    exportData () {
      const header = ['运单编号', '客户名称', '车线名称', '运输费用', '司机奖励', '异常费用', '结算状态']
      const body = this.rows.map(item => [item.dn_code, item.customer, item.line_name, item.freight, item.reward, item.exception_fee, item.settle_status])
      const content = [header].concat(body).map(line => line.join(',')).join('\r\n')
      exportFile('在途费用.csv', '\ufeff' + content, 'text/csv')
    }
  },
  created () {
    this.getList()
  }
}
</script>

<style scoped>
.fee-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fee-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.fee-card,
.fee-table-card {
  border-radius: 16px;
  background: #fff;
}

.fee-card {
  padding: 18px;
}

.fee-card__label {
  font-size: 14px;
  color: #5c6c87;
}

.fee-card__value {
  margin-top: 8px;
  font-size: 28px;
  font-weight: 700;
  color: #1f4fd8;
}

.fee-card__desc {
  margin-top: 8px;
  font-size: 12px;
  color: #8b97ad;
}

.fee-table-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px 10px;
  flex-wrap: wrap;
}

.fee-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2a44;
}

.fee-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #7d889f;
}

@media (max-width: 960px) {
  .fee-summary {
    grid-template-columns: 1fr;
  }

  .fee-table-head {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .fee-page {
    overflow-x: auto;
  }
}
</style>
