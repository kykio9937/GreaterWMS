<template>
  <q-page class="create-waybill-page">
    <div class="waybill-shell">
      <div class="page-head">
        <div class="head-left">
          <span class="head-label">运单号:</span>
          <span class="head-code">{{ form.dn_code || '自动生成' }}</span>
          <label class="head-check"><input type="checkbox" v-model="flags.transit"> 往返运单</label>
          <label class="head-check"><input type="checkbox" v-model="flags.returnCargo"> 返程配货</label>
          <label class="head-check"><input type="checkbox" v-model="flags.emptyTask"> 空驶任务</label>
        </div>
        <div class="head-title">{{ isEditMode ? '修 改 运 单' : '创 建 运 单' }}</div>
        <div class="head-right">
          <span class="operator">{{ form.dispatcher || loginName }}</span>
          <span class="time-label">开单时间:</span>
          <span>{{ currentTime }}</span>
        </div>
      </div>

      <div class="section-block">
        <div class="section-caption">客户信息</div>
        <div class="line-form line-form-4">
          <div class="field-item wide-org">
            <div class="field-label required">所属组织:</div>
            <q-input v-model="form.organization" dense borderless class="table-input highlight-input" />
          </div>
          <div class="field-item wide-line">
            <div class="field-label required">车线名称:</div>
            <q-input v-model="form.line_name" dense borderless class="table-input" placeholder="请输入车线名称" />
          </div>
          <div class="field-item">
            <div class="field-label">项目名称:</div>
            <q-input v-model="form.project_name" dense borderless class="table-input" />
          </div>
          <div class="field-item">
            <div class="field-label required">客户名称:</div>
            <q-input v-model="form.customer_name" dense borderless class="table-input" />
          </div>
        </div>

        <div class="route-row">
          <div class="route-badge start">起</div>
          <div class="route-address">
            <q-input v-model="form.pickup_address" dense borderless class="table-input" placeholder="请输入装货地址" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.pickup_contact" dense borderless class="table-input" placeholder="联系人" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.pickup_phone" dense borderless class="table-input" placeholder="联系电话" />
          </div>
          <div class="route-time">
            <q-input v-model="form.pickup_time" dense borderless class="table-input" placeholder="实际发车时间" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.actual_mileage" dense borderless class="table-input" placeholder="实际里程" />
          </div>
        </div>

        <div class="route-row">
          <div class="route-badge end">终</div>
          <div class="route-address">
            <q-input v-model="form.delivery_address" dense borderless class="table-input" placeholder="请输入卸货地址" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.delivery_contact" dense borderless class="table-input" placeholder="联系人" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.delivery_phone" dense borderless class="table-input" placeholder="联系电话" />
          </div>
          <div class="route-time">
            <q-input v-model="form.delivery_time" dense borderless class="table-input" placeholder="预计到达时间" />
          </div>
          <div class="route-mini">
            <q-input v-model="form.line_mileage" dense borderless class="table-input" placeholder="车线里程" />
          </div>
        </div>

        <div class="line-form line-form-5">
          <div class="field-item"><div class="field-label">派单里程:</div><q-input v-model="form.dispatch_mileage" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label">回单类型:</div><q-input v-model="form.receipt_type" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label">未结运费进度:</div><q-input v-model="form.unfinished_progress" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label">运营增减:</div><q-input v-model="form.transport_delta" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label">配货方式:</div><q-input v-model="form.allocate_mode" dense borderless class="table-input" /></div>
        </div>

        <div class="line-form line-form-5">
          <div class="field-item"><div class="field-label required">部门:</div><q-input v-model="form.department" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label required">组长:</div><q-input v-model="form.team_leader" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label required">配货员:</div><q-input v-model="form.dispatcher" dense borderless class="table-input" /></div>
          <div class="field-item"><div class="field-label">温度要求:</div><q-input v-model="form.temperature_range" dense borderless class="table-input" placeholder="请输入-80~120" /></div>
          <div class="field-item"></div>
        </div>

        <div class="line-form line-form-3 goods-row">
          <div class="field-item">
            <div class="field-label required">货物名称:</div>
            <q-input v-model="form.cargo_name" dense borderless class="table-input" />
          </div>
          <div class="field-item">
            <div class="field-label required">重量(吨):</div>
            <q-input v-model.number="form.weight" dense borderless type="number" class="table-input" />
          </div>
          <div class="field-item">
            <div class="field-label required">体积(方):</div>
            <q-input v-model.number="form.volume" dense borderless type="number" class="table-input" />
          </div>
        </div>
      </div>

      <div class="cost-layout">
        <div class="cost-block">
          <div class="cost-side">收入运费</div>
          <div class="cost-main">
            <div class="line-form line-form-4 compact-cost">
              <div class="field-item"><div class="field-label">到车运费:</div><q-input v-model.number="form.arrival_freight" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">运价:</div><q-input v-model.number="form.price_per_ton" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">项目合计:</div><q-input v-model.number="form.project_total" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">信息费:</div><q-input v-model.number="form.info_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">技术服务费:</div><q-input v-model.number="form.service_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">平台不可退定金:</div><q-input v-model.number="form.platform_refund" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">进仓费:</div><q-input v-model.number="form.storage_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">货运险:</div><q-input v-model.number="form.insurance_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">税费:</div><q-input v-model.number="form.tax_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">久返定金:</div><q-input v-model.number="form.long_return_deposit" dense borderless type="number" class="table-input" /></div>
            </div>
          </div>
          <div class="pay-side">
            <div class="pay-side-title">付款方式</div>
            <div class="line-form line-form-2">
              <div class="field-item"><div class="field-label">到付:</div><q-input v-model.number="form.arrive_pay" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">回付:</div><q-input v-model.number="form.return_pay" dense borderless type="number" class="table-input" /></div>
            </div>
          </div>
        </div>

        <div class="line-form line-form-4 dispatch-row">
          <div class="field-item"><div class="field-label required">派单员:</div><q-input v-model="form.dispatcher" dense borderless class="table-input" /></div>
          <div class="field-item span-3"><div class="field-label">运单备注:</div><q-input v-model="form.remark" dense borderless class="table-input" /></div>
        </div>

        <div class="section-block inner-block">
          <div class="section-caption">运力信息</div>
          <div class="line-form line-form-5">
            <div class="field-item"><div class="field-label">车辆调度员:</div><q-input v-model="form.vehicle_dispatch" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">车牌号:</div><q-input v-model="form.plate_number" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">车辆来源:</div><q-input v-model="form.vehicle_source" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">实际车长:</div><q-input v-model="form.vehicle_length" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label required">主驾司机:</div><q-input v-model="form.main_driver" dense borderless class="table-input" /></div>
          </div>
          <div class="line-form line-form-5">
            <div class="field-item"><div class="field-label">主驾电话:</div><q-input v-model="form.main_driver_phone" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">副驾司机:</div><q-input v-model="form.sub_driver" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">回单地址:</div><q-input v-model="form.receipt_address" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">车辆属性:</div><q-input v-model="form.vehicle_type" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">是否完结:</div><q-input v-model="form.finished_flag" dense borderless class="table-input" /></div>
          </div>
        </div>

        <div class="cost-block">
          <div class="cost-side">支出运费</div>
          <div class="cost-main">
            <div class="line-form line-form-4 compact-cost">
              <div class="field-item"><div class="field-label">运输费:</div><q-input v-model.number="form.transport_cost" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">应付付款方式:</div><q-input v-model="form.cost_pay_mode" dense borderless class="table-input" /></div>
              <div class="field-item"><div class="field-label">油费单价:</div><q-input v-model.number="form.oil_price" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">差异里程:</div><q-input v-model="form.diff_mileage" dense borderless class="table-input" /></div>
              <div class="field-item"><div class="field-label">预计油费:</div><q-input v-model.number="form.estimate_oil_fee" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">实际油耗:</div><q-input v-model.number="form.actual_oil_fee" dense borderless type="number" class="table-input" /></div>
            </div>
          </div>
          <div class="pay-side">
            <div class="pay-side-title">付款方式</div>
            <div class="line-form line-form-2">
              <div class="field-item"><div class="field-label">定金:</div><q-input v-model.number="form.deposit" dense borderless type="number" class="table-input" /></div>
              <div class="field-item"><div class="field-label">车上净得:</div><q-input v-model.number="form.net_income" dense borderless type="number" class="table-input" /></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-tabs">
        <button
          v-for="tab in detailTabs"
          :key="tab.key"
          type="button"
          :class="['bottom-tab', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="tab-body">
        <template v-if="activeTab === 'transit'">
          <div class="line-form line-form-5">
            <div class="field-item"><div class="field-label">司机等待时间:</div><q-input v-model="form.driver_wait_time" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">始发等待时间:</div><q-input v-model="form.depart_wait_time" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">终点到达时间:</div><q-input v-model="form.arrive_time" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">在途时长:</div><q-input v-model="form.transit_duration" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">卸车等待时长:</div><q-input v-model="form.unload_duration" dense borderless class="table-input" /></div>
          </div>
          <div class="line-form line-form-5">
            <div class="field-item"><div class="field-label">到达公里数:</div><q-input v-model="form.start_mileage" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">始发发货备注:</div><q-input v-model="form.start_remark" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">终点到达时间:</div><q-input v-model="form.end_arrive_time" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">卸车等待时长:</div><q-input v-model="form.wait_duration" dense borderless class="table-input" /></div>
            <div class="field-item"><div class="field-label">发车公里数:</div><q-input v-model="form.end_mileage" dense borderless class="table-input" /></div>
          </div>
        </template>
        <div v-else class="tab-placeholder">{{ activeTab === 'customer' ? '客户考核信息暂未录入' : '运力考核信息暂未录入' }}</div>
      </div>

      <div class="action-bar">
        <q-btn outline color="primary" label="光标路径" @click="showCursorTip" />
        <q-btn outline color="primary" label="保存并新增(F4)" @click="submitForm('saveAndCreate')" />
        <q-btn outline color="primary" label="保存并打印(F7)" @click="submitForm('saveAndPrint')" />
        <q-btn color="primary" label="保存(F9)" @click="submitForm('save')" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { LocalStorage } from 'quasar'
import { getauth, patchauth, postauth } from 'boot/axios_request'
import Bus from 'boot/bus.js'

const currentTimeString = () => new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')

const buildInitialForm = () => ({
  id: null,
  dn_code: '',
  project_name: '',
  customer_name: '',
  cargo_name: '',
  quantity: 1,
  weight: 0,
  volume: 0,
  line_name: '',
  plate_number: '',
  organization: '西安莲湖白金昌',
  department: '运输运营部',
  team_leader: '',
  dispatcher: LocalStorage.getItem('login_name') || '',
  main_driver: '',
  main_driver_phone: '',
  sub_driver: '',
  vehicle_type: '高栏车',
  pickup_address: '',
  pickup_contact: '',
  pickup_phone: '',
  pickup_time: currentTimeString(),
  delivery_address: '',
  delivery_contact: '',
  delivery_phone: '',
  delivery_time: '',
  line_mileage: '',
  dispatch_mileage: '',
  actual_mileage: '',
  receipt_type: '',
  unfinished_progress: '',
  transport_delta: '',
  allocate_mode: '',
  temperature_range: '',
  arrival_freight: 0,
  price_per_ton: 0,
  project_total: 0,
  info_fee: 0,
  service_fee: 0,
  platform_refund: 0,
  storage_fee: 0,
  insurance_fee: 0,
  tax_fee: 0,
  long_return_deposit: 0,
  arrive_pay: 0,
  return_pay: 0,
  remark: '',
  audit_status: '待审核',
  audit_remark: '',
  vehicle_dispatch: '',
  vehicle_source: '',
  vehicle_length: '',
  receipt_address: '',
  finished_flag: '',
  transport_cost: 0,
  cost_pay_mode: '',
  oil_price: 0,
  diff_mileage: '',
  estimate_oil_fee: 0,
  actual_oil_fee: 0,
  deposit: 0,
  net_income: 0,
  driver_wait_time: '',
  depart_wait_time: '',
  arrive_time: '',
  transit_duration: '',
  unload_duration: '',
  start_mileage: '',
  start_remark: '',
  end_arrive_time: '',
  wait_duration: '',
  end_mileage: ''
})

export default {
  name: 'CreateWaybillPage',
  data () {
    return {
      loading: false,
      currentTime: currentTimeString(),
      loginName: LocalStorage.getItem('login_name') || '贝权航',
      form: buildInitialForm(),
      flags: {
        transit: false,
        returnCargo: false,
        emptyTask: false
      },
      activeTab: 'transit',
      detailTabs: [
        { key: 'transit', label: '运行情况' },
        { key: 'customer', label: '客户考核' },
        { key: 'carrier', label: '运力考核' }
      ]
    }
  },
  computed: {
    isEditMode () {
      return this.$route.query.mode === 'edit' && Boolean(this.$route.query.id)
    }
  },
  methods: {
    buildPayload () {
      return {
        customer_name: this.form.customer_name,
        cargo_name: this.form.cargo_name,
        quantity: Number(this.form.quantity || 1),
        weight: Number(this.form.weight || 0),
        volume: Number(this.form.volume || 0),
        line_name: this.form.line_name,
        plate_number: this.form.plate_number,
        organization: this.form.organization,
        department: this.form.department,
        dispatcher: this.form.dispatcher,
        arrival_freight: Number(this.form.arrival_freight || 0),
        transport_cost: Number(this.form.transport_cost || 0),
        unload_fee: Number(this.form.actual_oil_fee || 0),
        storage_fee: Number(this.form.storage_fee || 0),
        main_driver: this.form.main_driver,
        vehicle_type: this.form.vehicle_type,
        remark: this.form.remark,
        pickup_address: this.form.pickup_address,
        pickup_contact: this.form.pickup_contact,
        pickup_phone: this.form.pickup_phone,
        delivery_address: this.form.delivery_address,
        delivery_contact: this.form.delivery_contact,
        delivery_phone: this.form.delivery_phone
      }
    },
    buildTransportPatch () {
      return {
        customer: this.form.customer_name,
        total_weight: Number(this.form.weight || 0),
        total_volume: Number(this.form.volume || 0),
        total_cost: Number(this.form.arrival_freight || this.form.transport_cost || 0),
        transportation_fee: {
          line_name: this.form.line_name,
          plate_number: this.form.plate_number,
          driver_name: this.form.main_driver,
          goods_name: this.form.cargo_name,
          vehicle_type: this.form.vehicle_type,
          business_income: Number(this.form.arrival_freight || this.form.transport_cost || 0),
          carrier_cost: Number(this.form.transport_cost || 0),
          extra_fee: Number(this.form.actual_oil_fee || 0),
          storage_fee: Number(this.form.storage_fee || 0),
          organization: this.form.organization,
          department: this.form.department,
          dispatcher: this.form.dispatcher,
          remark: this.form.remark,
          audit_status: this.form.audit_status || '待审核',
          audit_remark: this.form.audit_remark || '',
          pickup_address: this.form.pickup_address,
          pickup_contact: this.form.pickup_contact,
          pickup_phone: this.form.pickup_phone,
          delivery_address: this.form.delivery_address,
          delivery_contact: this.form.delivery_contact,
          delivery_phone: this.form.delivery_phone
        }
      }
    },
    fillFormFromRow (row, detailRow = null) {
      const fee = row.transportation_fee || {}
      this.form = {
        ...buildInitialForm(),
        id: row.id,
        dn_code: row.dn_code || '',
        customer_name: row.customer || '',
        cargo_name: (detailRow && detailRow.goods_desc) || fee.goods_name || '',
        quantity: (detailRow && detailRow.goods_qty) || 1,
        weight: (detailRow && detailRow.goods_weight) || row.total_weight || 0,
        volume: (detailRow && detailRow.goods_volume) || row.total_volume || 0,
        line_name: fee.line_name || '',
        plate_number: fee.plate_number || '',
        organization: fee.organization || '西安莲湖白金昌',
        department: fee.department || '运输运营部',
        dispatcher: fee.dispatcher || row.creater || '',
        main_driver: fee.driver_name || '',
        vehicle_type: fee.vehicle_type || '高栏车',
        pickup_address: fee.pickup_address || '',
        pickup_contact: fee.pickup_contact || '',
        pickup_phone: fee.pickup_phone || '',
        delivery_address: fee.delivery_address || '',
        delivery_contact: fee.delivery_contact || '',
        delivery_phone: fee.delivery_phone || '',
        arrival_freight: Number(fee.business_income || row.total_cost || 0),
        transport_cost: Number(fee.carrier_cost || 0),
        actual_oil_fee: Number(fee.extra_fee || 0),
        storage_fee: Number(fee.storage_fee || 0),
        remark: fee.remark || '',
        audit_status: fee.audit_status || '待审核',
        audit_remark: fee.audit_remark || ''
      }
    },
    resetForm () {
      this.form = buildInitialForm()
      this.currentTime = currentTimeString()
      this.activeTab = 'transit'
    },
    showCursorTip () {
      this.$q.notify({
        type: 'info',
        message: '演示版保留了光标路径按钮位，可继续补真实功能'
      })
    },
    async loadEditData () {
      if (!this.isEditMode) {
        this.resetForm()
        return
      }
      this.loading = true
      try {
        const row = await getauth(`dn/list/${this.$route.query.id}/`)
        let detailRow = null
        try {
          const detailRes = await getauth(`dn/detail/?dn_code=${encodeURIComponent(row.dn_code)}`)
          detailRow = detailRes.results && detailRes.results.length ? detailRes.results[0] : null
        } catch (err) {
          detailRow = null
        }
        this.fillFormFromRow(row, detailRow)
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: err.detail || '运单数据加载失败'
        })
        this.$router.push({ name: 'dn' })
      } finally {
        this.loading = false
      }
    },
    async submitForm (action) {
      if (!this.form.customer_name || !this.form.cargo_name || !this.form.line_name) {
        this.$q.notify({
          type: 'negative',
          message: '请先填写客户名称、货物名称和车线名称'
        })
        return
      }

      try {
        if (this.isEditMode) {
          await patchauth(`dn/list/${this.form.id}/`, this.buildTransportPatch())
          this.$q.notify({
            type: 'positive',
            message: `运单 ${this.form.dn_code} 修改成功`
          })
          Bus.$emit('waybillChanged', { type: 'edit', id: this.form.id })
          return
        }

        const res = await postauth('dn/create_waybill/', this.buildPayload())
        this.$q.notify({
          type: 'positive',
          message: `运单 ${res.dn_code} 保存成功`
        })
        Bus.$emit('waybillChanged', { type: 'create', dnCode: res.dn_code })
        if (action === 'saveAndCreate') {
          this.resetForm()
          return
        }
        if (action === 'saveAndPrint') {
          this.$q.notify({
            type: 'info',
            message: '打印入口已保留，可继续接打印模板'
          })
        }
        this.$router.push({ name: 'dn' })
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: (err && err.detail) || '运单保存失败'
        })
      }
    }
  },
  created () {
    this.loadEditData()
  },
  watch: {
    '$route.fullPath' () {
      this.loadEditData()
    }
  }
}
</script>

<style scoped>
.create-waybill-page {
  padding: 8px;
  background: #f2f3f7;
}

.waybill-shell {
  background: #fff;
  border: 1px solid #c6d8ec;
}

.page-head {
  display: grid;
  grid-template-columns: 1.6fr 0.8fr 1fr;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  padding: 0 10px;
  border-bottom: 1px solid #d8e6f4;
}

.head-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.head-label,
.time-label {
  color: #e53935;
}

.head-code {
  font-size: 14px;
  font-weight: 700;
  color: #ff2e2e;
}

.head-check {
  font-size: 12px;
  color: #516981;
}

.head-title {
  text-align: center;
  font-size: 24px;
  letter-spacing: 10px;
  color: #2f3b4e;
}

.head-right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #5a6f88;
}

.operator {
  color: #2b6cc2;
}

.section-block {
  border-top: 1px solid #c6d8ec;
}

.section-caption {
  height: 30px;
  line-height: 30px;
  padding: 0 10px;
  background: #d9ebfb;
  border-bottom: 1px solid #c6d8ec;
  color: #40688f;
}

.line-form {
  display: grid;
  border-bottom: 1px solid #e5eef7;
}

.line-form-3 {
  grid-template-columns: 1.2fr 1fr 1fr;
}

.line-form-4 {
  grid-template-columns: 1.1fr 1.4fr 1fr 1fr;
}

.line-form-5 {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.field-item {
  display: flex;
  align-items: center;
  min-height: 38px;
  border-right: 1px solid #edf3fa;
}

.field-item:last-child {
  border-right: 0;
}

.field-label {
  width: 106px;
  padding-left: 10px;
  color: #5c7189;
  white-space: nowrap;
}

.field-label.required {
  color: #ef3c33;
}

.table-input {
  flex: 1;
  min-height: 38px;
}

.highlight-input {
  background: #fff6c9;
}

.wide-org {
  min-width: 0;
}

.wide-line {
  min-width: 0;
}

.route-row {
  display: grid;
  grid-template-columns: 44px 1.7fr 0.6fr 0.8fr 0.9fr 0.7fr;
  align-items: center;
  min-height: 38px;
  border-bottom: 1px solid #e5eef7;
}

.route-row > div {
  border-right: 1px solid #edf3fa;
  min-height: 38px;
  display: flex;
  align-items: center;
}

.route-row > div:last-child {
  border-right: 0;
}

.route-badge {
  justify-content: center;
  font-weight: 700;
}

.route-badge.start {
  color: #2cbf76;
}

.route-badge.end {
  color: #ff6c6c;
}

.route-address,
.route-mini,
.route-time {
  padding: 0 6px;
}

.goods-row {
  border-bottom: 1px solid #c6d8ec;
}

.cost-layout {
  border-top: 1px solid #c6d8ec;
}

.cost-block {
  display: grid;
  grid-template-columns: 58px 1fr 360px;
  border-bottom: 1px solid #c6d8ec;
}

.cost-side,
.pay-side-title {
  background: #eef6fe;
  color: #4c6f97;
}

.cost-side {
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #c6d8ec;
}

.cost-main {
  min-width: 0;
}

.compact-cost .field-item {
  min-height: 34px;
}

.pay-side {
  border-left: 1px dashed #c6d8ec;
}

.pay-side-title {
  height: 34px;
  line-height: 34px;
  text-align: center;
  border-bottom: 1px solid #c6d8ec;
}

.dispatch-row .span-3 {
  grid-column: span 3;
}

.inner-block {
  border-top: 0;
}

.bottom-tabs {
  display: flex;
  gap: 0;
  padding-left: 10px;
  margin-top: 6px;
}

.bottom-tab {
  min-width: 96px;
  height: 34px;
  border: 1px solid #c6d8ec;
  border-bottom: 0;
  background: #f4f7fb;
  color: #4f6886;
  cursor: pointer;
}

.bottom-tab.active {
  background: #fff;
  color: #2671bf;
}

.tab-body {
  border-top: 1px solid #c6d8ec;
  border-bottom: 1px solid #c6d8ec;
}

.tab-placeholder {
  padding: 24px 12px;
  color: #8092a8;
}

.action-bar {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 16px 0 20px;
}

@media (max-width: 1300px) {
  .page-head {
    grid-template-columns: 1fr;
  }

  .line-form-4,
  .line-form-5,
  .line-form-3,
  .route-row,
  .cost-block {
    grid-template-columns: 1fr;
  }

  .field-item,
  .route-row > div {
    border-right: 0;
    border-bottom: 1px solid #edf3fa;
  }

  .dispatch-row .span-3 {
    grid-column: span 1;
  }
}
</style>
