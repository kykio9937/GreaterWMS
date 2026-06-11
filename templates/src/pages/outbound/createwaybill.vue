<template>
  <q-page class="create-waybill-page">
    <div class="waybill-board">
      <div class="board-topbar">
        <div class="topbar-left">
          <span class="topbar-label">运单号:</span>
          <span class="topbar-code">{{ form.waybillNo }}</span>
          <q-checkbox v-model="form.transitWaybill" dense label="往返运单" />
          <q-checkbox v-model="form.returnAllocation" dense label="返程配货" />
          <q-checkbox v-model="form.emptyTask" dense label="空驶任务" />
        </div>
        <div class="topbar-title">创建运单</div>
        <div class="topbar-right">
          <span>贝权航</span>
          <span class="divider">|</span>
          <span>开单时间: {{ form.orderTime }}</span>
        </div>
      </div>

      <div class="section-block">
        <div class="section-title">客户信息</div>
        <div class="form-grid customer-grid">
          <div class="field-cell field-cell-highlight">
            <div class="field-label required">所属组织:</div>
            <q-input v-model="form.organization" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label required">车线名称:</div>
            <q-input v-model="form.lineName" dense borderless placeholder="请输入车线名称" />
          </div>
          <div class="field-cell">
            <div class="field-label">项目名称:</div>
            <q-input v-model="form.projectName" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label required">客户名称:</div>
            <q-input v-model="form.customerName" dense borderless placeholder="请输入客户名称" />
          </div>
        </div>

        <div class="route-rows">
          <div class="route-row">
            <div class="route-badge route-start">起</div>
            <div class="route-address">{{ form.pickupAddress || '请输入装货地址' }}</div>
            <q-input v-model="form.pickupContact" dense borderless class="route-mini" placeholder="联系人" />
            <q-input v-model="form.pickupPhone" dense borderless class="route-mini" placeholder="联系电话" />
            <q-input v-model="form.pickupTime" dense borderless class="route-time" placeholder="装货时间" />
            <q-input v-model="form.pickupMileage" dense borderless class="route-mini" placeholder="起始里程" />
          </div>
          <div class="route-row">
            <div class="route-badge route-end">终</div>
            <div class="route-address">{{ form.deliveryAddress || '请输入卸货地址' }}</div>
            <q-input v-model="form.deliveryContact" dense borderless class="route-mini" placeholder="联系人" />
            <q-input v-model="form.deliveryPhone" dense borderless class="route-mini" placeholder="联系电话" />
            <q-input v-model="form.deliveryTime" dense borderless class="route-time" placeholder="到达时间" />
            <q-input v-model="form.deliveryMileage" dense borderless class="route-mini" placeholder="结束里程" />
          </div>
        </div>

        <div class="form-grid meta-grid">
          <div class="field-cell">
            <div class="field-label">派单里程:</div>
            <q-input v-model="form.dispatchMileage" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label">回单类型:</div>
            <q-select v-model="form.receiptType" dense borderless emit-value map-options :options="receiptTypeOptions" />
          </div>
          <div class="field-cell">
            <div class="field-label">运输增减:</div>
            <q-input v-model="form.transportDelta" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label">配货方式:</div>
            <q-select v-model="form.allocateMode" dense borderless emit-value map-options :options="allocateModeOptions" />
          </div>
          <div class="field-cell">
            <div class="field-label required">部门:</div>
            <q-input v-model="form.department" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label required">组长:</div>
            <q-input v-model="form.teamLeader" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label required">配货员:</div>
            <q-input v-model="form.dispatcher" dense borderless />
          </div>
          <div class="field-cell">
            <div class="field-label">温度要求:</div>
            <q-input v-model="form.temperature" dense borderless placeholder="例如 0~8℃" />
          </div>
        </div>

        <div class="goods-grid">
          <div class="field-cell goods-name-cell">
            <div class="field-label required">货物名称:</div>
            <q-input v-model="form.cargoName" dense borderless placeholder="请输入货物名称" />
          </div>
          <div class="field-cell">
            <div class="field-label required">重量(吨):</div>
            <q-input v-model.number="form.weight" dense borderless type="number" />
          </div>
          <div class="field-cell">
            <div class="field-label required">体积(方):</div>
            <q-input v-model.number="form.volume" dense borderless type="number" />
          </div>
          <div class="field-cell">
            <div class="field-label required">件数:</div>
            <q-input v-model.number="form.quantity" dense borderless type="number" />
          </div>
        </div>
      </div>

      <div class="two-column-panel">
        <div class="panel-block">
          <div class="panel-aside">收入运费</div>
          <div class="panel-main">
            <div class="form-grid finance-grid">
              <div class="field-cell"><div class="field-label required">到车运费:</div><q-input v-model.number="form.arrivalFreight" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">运价:</div><q-input v-model.number="form.pricePerTon" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">项目合计:</div><q-input v-model.number="form.projectTotal" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">信息费:</div><q-input v-model.number="form.infoFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">技术服务费:</div><q-input v-model.number="form.serviceFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">平台退定金:</div><q-input v-model.number="form.platformRefund" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">进仓费:</div><q-input v-model.number="form.storageFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">货运险:</div><q-input v-model.number="form.insuranceFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">税费:</div><q-input v-model.number="form.taxFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">久返定金:</div><q-input v-model.number="form.longReturnDeposit" dense borderless type="number" /></div>
              <div class="field-cell">
                <div class="field-label required">派单员:</div>
                <q-input v-model="form.dispatcher" dense borderless />
              </div>
              <div class="field-cell wide-cell">
                <div class="field-label">运单备注:</div>
                <q-input v-model="form.remark" dense borderless />
              </div>
            </div>
          </div>
          <div class="payment-side">
            <div class="payment-title">付款方式</div>
            <div class="payment-grid">
              <div class="field-cell"><div class="field-label">到付:</div><q-input v-model.number="form.arrivePay" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">回付:</div><q-input v-model.number="form.returnPay" dense borderless type="number" /></div>
            </div>
          </div>
        </div>

        <div class="section-block">
          <div class="section-title">运力信息</div>
          <div class="form-grid vehicle-grid">
            <div class="field-cell"><div class="field-label">车辆调度:</div><q-input v-model="form.vehicleDispatch" dense borderless /></div>
            <div class="field-cell"><div class="field-label required">车牌号:</div><q-input v-model="form.plateNumber" dense borderless /></div>
            <div class="field-cell"><div class="field-label">车辆来源:</div><q-input v-model="form.vehicleSource" dense borderless /></div>
            <div class="field-cell"><div class="field-label">实际车长:</div><q-input v-model="form.vehicleLength" dense borderless /></div>
            <div class="field-cell"><div class="field-label required">主驾司机:</div><q-input v-model="form.mainDriver" dense borderless /></div>
            <div class="field-cell"><div class="field-label">主驾电话:</div><q-input v-model="form.mainDriverPhone" dense borderless /></div>
            <div class="field-cell"><div class="field-label">身份证:</div><q-input v-model="form.driverCard" dense borderless /></div>
            <div class="field-cell"><div class="field-label">副驾司机:</div><q-input v-model="form.subDriver" dense borderless /></div>
            <div class="field-cell"><div class="field-label">副驾电话:</div><q-input v-model="form.subDriverPhone" dense borderless /></div>
            <div class="field-cell"><div class="field-label">回单地址:</div><q-input v-model="form.receiptAddress" dense borderless /></div>
            <div class="field-cell"><div class="field-label">车辆属性:</div><q-select v-model="form.vehicleType" dense borderless emit-value map-options :options="vehicleTypeOptions" /></div>
            <div class="field-cell"><div class="field-label">是否完结:</div><q-select v-model="form.finishedFlag" dense borderless emit-value map-options :options="finishOptions" /></div>
          </div>
        </div>

        <div class="panel-block">
          <div class="panel-aside">支出运费</div>
          <div class="panel-main">
            <div class="form-grid finance-grid">
              <div class="field-cell"><div class="field-label required">运输费:</div><q-input v-model.number="form.transportCost" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">应付付款方式:</div><q-select v-model="form.costPayMode" dense borderless emit-value map-options :options="costPayModeOptions" /></div>
              <div class="field-cell"><div class="field-label">油费单价:</div><q-input v-model.number="form.oilPrice" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">差异里程:</div><q-input v-model="form.diffMileage" dense borderless /></div>
              <div class="field-cell"><div class="field-label">预计油费:</div><q-input v-model.number="form.estimateOilFee" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">实际油耗:</div><q-input v-model.number="form.actualOilFee" dense borderless type="number" /></div>
            </div>
          </div>
          <div class="payment-side">
            <div class="payment-title">付款方式</div>
            <div class="payment-grid">
              <div class="field-cell"><div class="field-label">定金:</div><q-input v-model.number="form.deposit" dense borderless type="number" /></div>
              <div class="field-cell"><div class="field-label">车上净得:</div><q-input v-model.number="form.netIncome" dense borderless type="number" /></div>
            </div>
          </div>
        </div>
      </div>

      <div class="section-block">
        <div class="tab-strip">
          <button
            v-for="tab in detailTabs"
            :key="tab.key"
            type="button"
            :class="['detail-tab', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="tab-panel">
          <div v-if="activeTab === 'transit'" class="form-grid transit-grid">
            <div class="field-cell"><div class="field-label">司机等待时间:</div><q-input v-model="form.driverWaitTime" dense borderless /></div>
            <div class="field-cell"><div class="field-label">始发等待时间:</div><q-input v-model="form.departWaitTime" dense borderless /></div>
            <div class="field-cell"><div class="field-label">终点到达时间:</div><q-input v-model="form.arriveTime" dense borderless /></div>
            <div class="field-cell"><div class="field-label">在途时长:</div><q-input v-model="form.transitDuration" dense borderless /></div>
            <div class="field-cell"><div class="field-label">卸货时长:</div><q-input v-model="form.unloadDuration" dense borderless /></div>
            <div class="field-cell"><div class="field-label">发车公里数:</div><q-input v-model="form.startMileage" dense borderless /></div>
            <div class="field-cell"><div class="field-label">到达公里数:</div><q-input v-model="form.endMileage" dense borderless /></div>
            <div class="field-cell"><div class="field-label">实际里程:</div><q-input v-model="form.actualMileage" dense borderless /></div>
          </div>
          <div v-else class="tab-empty">
            {{ activeTab === 'customer' ? '客户考核信息暂未录入' : '运力考核信息暂未录入' }}
          </div>
        </div>
      </div>

      <div class="bottom-actions">
        <q-btn outline color="primary" label="光标路径" @click="showCursorTip" />
        <q-btn outline color="primary" label="保存并新增(F4)" @click="submitForm('saveAndCreate')" />
        <q-btn outline color="primary" label="保存并打印(F7)" @click="submitForm('saveAndPrint')" />
        <q-btn unelevated color="primary" label="保存(F9)" @click="submitForm('save')" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { postauth } from 'boot/axios_request'

const nowString = () => new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
const waybillNo = () => `XALHBJCYD${new Date().toISOString().slice(0, 10).replace(/-/g, '')}${String(Date.now()).slice(-4)}`

const buildInitialForm = () => ({
  waybillNo: waybillNo(),
  orderTime: nowString(),
  transitWaybill: false,
  returnAllocation: false,
  emptyTask: false,
  organization: '西安莲湖白金昌',
  lineName: '',
  projectName: '',
  customerName: '',
  pickupAddress: '',
  pickupContact: '',
  pickupPhone: '',
  pickupTime: nowString(),
  pickupMileage: '',
  deliveryAddress: '',
  deliveryContact: '',
  deliveryPhone: '',
  deliveryTime: '',
  deliveryMileage: '',
  dispatchMileage: '',
  receiptType: '纸质回单',
  transportDelta: '',
  allocateMode: '平台配货',
  department: '运营部',
  teamLeader: '白金昌',
  dispatcher: '贝权航',
  temperature: '',
  cargoName: '',
  weight: '',
  volume: '',
  quantity: 1,
  arrivalFreight: '',
  pricePerTon: '',
  projectTotal: '',
  infoFee: '',
  serviceFee: '',
  platformRefund: '',
  storageFee: '',
  insuranceFee: '',
  taxFee: '',
  longReturnDeposit: '',
  remark: '',
  arrivePay: '',
  returnPay: '',
  vehicleDispatch: '',
  plateNumber: '',
  vehicleSource: '',
  vehicleLength: '',
  mainDriver: '',
  mainDriverPhone: '',
  driverCard: '',
  subDriver: '',
  subDriverPhone: '',
  receiptAddress: '',
  vehicleType: '高栏车',
  finishedFlag: '未完结',
  transportCost: '',
  costPayMode: '多笔付',
  oilPrice: '',
  diffMileage: '',
  estimateOilFee: '',
  actualOilFee: '',
  deposit: '',
  netIncome: '',
  driverWaitTime: '',
  departWaitTime: '',
  arriveTime: '',
  transitDuration: '',
  unloadDuration: '',
  startMileage: '',
  endMileage: '',
  actualMileage: ''
})

export default {
  name: 'CreateWaybillPage',
  data () {
    return {
      form: buildInitialForm(),
      activeTab: 'transit',
      detailTabs: [
        { key: 'transit', label: '运行情况' },
        { key: 'customer', label: '客户考核' },
        { key: 'carrier', label: '运力考核' }
      ],
      receiptTypeOptions: ['纸质回单', '电子回单', '无需回单'].map(label => ({ label, value: label })),
      allocateModeOptions: ['平台配货', '自有客户', '返程拼单'].map(label => ({ label, value: label })),
      vehicleTypeOptions: ['高栏车', '厢式货车', '平板车', '冷藏车'].map(label => ({ label, value: label })),
      finishOptions: ['未完结', '已完结'].map(label => ({ label, value: label })),
      costPayModeOptions: ['多笔付', '现付', '到付', '回付'].map(label => ({ label, value: label }))
    }
  },
  methods: {
    buildWaybillPayload () {
      return {
        customer_name: this.form.customerName,
        cargo_name: this.form.cargoName,
        quantity: Number(this.form.quantity || 1) || 1,
        weight: Number(this.form.weight || 0),
        volume: Number(this.form.volume || 0),
        line_name: this.form.lineName,
        plate_number: this.form.plateNumber,
        organization: this.form.organization,
        department: this.form.department,
        dispatcher: this.form.dispatcher,
        arrival_freight: Number(this.form.arrivalFreight || this.form.projectTotal || 0),
        transport_cost: Number(this.form.transportCost || 0),
        unload_fee: Number(this.form.actualOilFee || 0),
        storage_fee: Number(this.form.storageFee || 0),
        main_driver: this.form.mainDriver,
        vehicle_type: this.form.vehicleType,
        remark: this.form.remark,
        pickup_address: this.form.pickupAddress,
        pickup_contact: this.form.pickupContact,
        pickup_phone: this.form.pickupPhone,
        delivery_address: this.form.deliveryAddress,
        delivery_contact: this.form.deliveryContact,
        delivery_phone: this.form.deliveryPhone
      }
    },
    resetForm () {
      this.form = buildInitialForm()
      this.activeTab = 'transit'
      this.$q.notify({
        type: 'positive',
        message: '已重置为新运单'
      })
    },
    showCursorTip () {
      this.$q.notify({
        type: 'info',
        message: '演示版已保留按钮位，可继续扩展光标路径功能。'
      })
    },
    async submitForm (action) {
      if (!this.form.customerName || !this.form.cargoName) {
        this.$q.notify({
          type: 'negative',
          message: '请先填写客户名称和货物名称'
        })
        return
      }

      try {
        const res = await postauth('dn/create_waybill/', this.buildWaybillPayload())
        this.$q.notify({
          type: 'positive',
          message: `运单 ${res.dn_code} 已保存`
        })
        if (action === 'saveAndCreate') {
          this.resetForm()
          return
        }
        if (action === 'saveAndPrint') {
          this.$q.notify({
            type: 'info',
            message: '打印功能入口已保留，演示版可继续接打印模板。'
          })
        }
        this.$router.push({ name: 'dn' })
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: err.detail || '运单保存失败'
        })
      }
    }
  }
}
</script>

<style scoped>
.create-waybill-page {
  background: #f3f7fc;
  padding: 6px;
}

.waybill-board {
  background: #fff;
  border: 1px solid #b8d0ea;
  box-shadow: inset 0 0 0 1px #eef5fc;
}

.board-topbar {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr 1fr;
  align-items: center;
  gap: 12px;
  min-height: 54px;
  padding: 0 12px;
  border-bottom: 1px solid #c5d9ef;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  color: #41566f;
  font-size: 13px;
}

.topbar-label {
  color: #f14545;
  font-weight: 700;
}

.topbar-code {
  color: #ff3b30;
  font-size: 15px;
  font-weight: 700;
}

.topbar-title {
  text-align: center;
  font-size: 28px;
  letter-spacing: 10px;
  color: #26384f;
}

.topbar-right {
  justify-self: end;
  color: #4e79a5;
  font-size: 13px;
}

.divider {
  margin: 0 8px;
  color: #d0d8e2;
}

.section-block {
  border-top: 1px solid #c5d9ef;
}

.section-title {
  height: 30px;
  display: flex;
  align-items: center;
  padding: 0 10px;
  font-size: 13px;
  color: #355070;
  background: #cfe4f8;
  border-bottom: 1px solid #b8d0ea;
}

.form-grid {
  display: grid;
}

.customer-grid {
  grid-template-columns: 1.3fr 1fr 0.9fr 1fr;
}

.meta-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.goods-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 0.8fr;
}

.vehicle-grid {
  grid-template-columns: repeat(6, minmax(0, 1fr));
}

.finance-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.transit-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.field-cell {
  min-width: 0;
  min-height: 42px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 10px;
  border-right: 1px solid #e4eef8;
  border-bottom: 1px solid #e4eef8;
}

.field-cell-highlight {
  background: #fff5d5;
}

.field-label {
  flex-shrink: 0;
  color: #4a5f79;
  font-size: 12px;
}

.field-label.required {
  color: #ff4040;
  font-weight: 700;
}

.field-cell :deep(.q-field__control) {
  min-height: 30px;
}

.field-cell :deep(.q-field__native),
.field-cell :deep(.q-field__input),
.field-cell :deep(input) {
  font-size: 12px;
  color: #23415e;
}

.route-rows {
  display: grid;
  grid-template-columns: 1fr;
}

.route-row {
  display: grid;
  grid-template-columns: 34px 1.6fr 0.6fr 0.8fr 0.8fr 0.6fr;
  align-items: center;
  min-height: 42px;
  border-bottom: 1px solid #e4eef8;
}

.route-badge {
  margin-left: 10px;
  width: 22px;
  height: 22px;
  line-height: 22px;
  text-align: center;
  border-radius: 5px;
  font-size: 12px;
  font-weight: 700;
}

.route-start {
  color: #31b36a;
  border: 1px solid #98ddb6;
  background: #f2fff7;
}

.route-end {
  color: #ff6a59;
  border: 1px solid #f4b2ac;
  background: #fff5f4;
}

.route-address,
.route-mini,
.route-time {
  min-width: 0;
  padding: 0 10px;
  border-right: 1px solid #e4eef8;
  color: #7a8ca1;
  font-size: 12px;
}

.route-address {
  color: #5d77a2;
}

.route-mini :deep(.q-field__control),
.route-time :deep(.q-field__control) {
  min-height: 30px;
}

.goods-name-cell {
  border-left: 1px solid #e4eef8;
}

.two-column-panel {
  display: grid;
  grid-template-columns: 1fr;
}

.panel-block {
  display: grid;
  grid-template-columns: 66px 1fr 300px;
  border-top: 1px solid #c5d9ef;
}

.panel-aside {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: #6780a0;
  background: #edf5fc;
  border-right: 1px solid #c5d9ef;
}

.panel-main {
  min-width: 0;
}

.payment-side {
  border-left: 1px dashed #d7e5f3;
}

.payment-title {
  height: 100%;
  min-height: 84px;
  float: left;
  width: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6780a0;
  background: #edf5fc;
  border-right: 1px solid #d7e5f3;
  font-size: 13px;
}

.payment-grid {
  margin-left: 64px;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.wide-cell {
  grid-column: span 2;
}

.tab-strip {
  display: flex;
  gap: 0;
  padding: 6px 10px 0;
  border-bottom: 1px solid #b8d0ea;
}

.detail-tab {
  min-width: 98px;
  height: 34px;
  border: 1px solid #c5d9ef;
  border-bottom: 0;
  background: #f5f9fd;
  color: #355070;
  font-size: 13px;
  cursor: pointer;
}

.detail-tab.active {
  background: #fff;
  color: #2a85dd;
}

.tab-panel {
  min-height: 84px;
}

.tab-empty {
  padding: 20px;
  color: #7a8ca1;
  font-size: 12px;
}

.bottom-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 12px 0 16px;
}

@media (max-width: 1600px) {
  .customer-grid,
  .meta-grid,
  .vehicle-grid,
  .finance-grid,
  .transit-grid,
  .goods-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .route-row {
    grid-template-columns: 34px 1fr 1fr 1fr;
  }
}

@media (max-width: 960px) {
  .board-topbar {
    grid-template-columns: 1fr;
    text-align: left;
  }

  .topbar-right {
    justify-self: start;
  }

  .customer-grid,
  .meta-grid,
  .vehicle-grid,
  .finance-grid,
  .transit-grid,
  .goods-grid,
  .payment-grid {
    grid-template-columns: 1fr;
  }

  .panel-block {
    grid-template-columns: 1fr;
  }

  .panel-aside,
  .payment-title {
    width: auto;
    min-height: 36px;
    float: none;
  }

  .payment-grid {
    margin-left: 0;
  }

  .route-row {
    grid-template-columns: 34px 1fr;
  }
}
</style>
