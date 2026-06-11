<template>
  <q-layout
    view="hHh LpR fFf"
    class="platform-layout"
  >
    <q-header reveal elevated class="platform-header text-white">
      <q-toolbar class="platform-toolbar">
        <q-btn
          v-if="$q.screen.lt.md"
          dense
          flat
          round
          color="white"
          icon="menu"
          class="mobile-menu-btn"
          @click="drawerleft = !drawerleft"
        />
        <div class="brand-block" @click="$router.push({ name: 'web_index' })">
          <img src="statics/icons/logo.png" alt="68卡运联盟" class="brand-logo">
          <div class="brand-copy">
            <div class="brand-title">68 卡运联盟</div>
            <div class="brand-subtitle">物流运输协同平台</div>
          </div>
        </div>
        <div class="top-nav">
          <button
            v-for="item in topNavItems"
            :key="item.key"
            type="button"
            :class="['top-nav-item', { active: topNavActive(item) }]"
            @click="navigateTopMenu(item)"
          >
            {{ item.label }}
          </button>
        </div>
        <q-space />
        <transition appear enter-active-class="animated zoomIn">
          <q-btn
            square
            dense
            flat
            color="white"
            :label="$q.screen.lt.md ? '' : (displayWarehouseName(warehouse_name) || '默认仓库')"
            icon="maps_home_work"
            class="warehouse-switcher"
          >
            <q-menu>
              <q-list style="min-width: 100px">
                <q-item
                  clickable
                  v-close-popup
                  v-for="(warehouse, index) in warehouseOptions"
                  :key="index"
                  @click="warehouseChange(index)"
                >
                  <q-item-section>{{ displayWarehouseName(warehouse.warehouse_name) }}</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </transition>
        <q-separator vertical dark class="header-divider" />
        <template v-if="authin === '1'">
          <transition appear enter-active-class="animated zoomIn">
            <q-btn-dropdown
              stretch
              flat
              color="white-8"
              icon="account_circle"
              :label="$q.screen.lt.md ? '' : login_name"
              class="account-switcher"
            >
              <div class="row no-wrap q-pa-md">
                <div class="column" style="width: 140px">
                  <div class="text-h6 q-mb-md">
                    {{ $t("index.user_center") }}
                  </div>
                  <div class="user-brief-tip">
                    当前账号已登录，可在这里直接退出系统。
                  </div>
                </div>
                <q-separator vertical inset class="q-mx-lg" />
                <div class="column items-center">
                  <q-avatar size="72px"
                    ><q-img src="statics/staff/stafftype.png"></q-img
                  ></q-avatar>
                  <div class="text-subtitle1 q-mt-md q-mb-xs">
                    {{ login_name }}
                  </div>
                  <q-btn
                    color="primary"
                    :label="$t('index.logout')"
                    push
                    size="sm"
                    v-close-popup
                    icon="img:statics/icons/logout.png"
                    @click="Logout()"
                  >
                    <q-tooltip
                      content-class="bg-amber text-black shadow-4"
                      :offset="[10, 10]"
                      content-style="font-size: 12px"
                      >{{ $t("index.logout") }}</q-tooltip
                    >
                  </q-btn>
                </div>
              </div>
            </q-btn-dropdown>
          </transition>
        </template>
        <template v-if="authin === '0'">
          <transition appear enter-active-class="animated zoomIn">
            <q-btn
              :label="$q.screen.lt.md ? '演示' : '演示进入'"
              color="amber-4"
              text-color="dark"
              class="demo-access-btn"
              @click="quickDemoAccess()"
              style="margin-left: 10px"
            />
          </transition>
          <transition appear enter-active-class="animated zoomIn">
            <q-btn
              :label="$q.screen.lt.md ? '登录' : $t('index.login')"
              flat
              color="white"
              class="ghost-access-btn"
              @click="login = true"
              style="margin-left: 10px"
            />
          </transition>
          <transition appear enter-active-class="animated zoomIn">
            <q-btn
              :label="$q.screen.lt.md ? '注册' : '注册并体验'"
              color="primary"
              class="primary-access-btn"
              @click="register = true"
              style="margin-left: 10px"
            />
          </transition>
        </template>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="drawerleft"
      :show-if-above="$q.screen.gt.sm"
      :width="188"
      :breakpoint="1024"
      bordered
      content-class="platform-drawer shadow-24"
    >
      <q-scroll-area class="fit">
        <div class="drawer-user-card">
          <q-avatar size="52px" class="drawer-user-avatar">
            <q-img src="statics/staff/stafftype.png"></q-img>
          </q-avatar>
          <div class="drawer-user-info">
            <div class="drawer-user-name">{{ login_name || '平台用户' }}</div>
            <div class="drawer-user-role">{{ displayWarehouseName(warehouse_name) || '默认仓库' }}</div>
          </div>
        </div>
        <q-list class="drawer-nav-list">
          <q-expansion-item
            v-for="section in filteredNavSections"
            :key="section.key"
            :value="isSectionExpanded(section.key)"
            @input="setSectionExpanded(section.key, $event)"
            dense
            dense-toggle
            switch-toggle-side
            expand-separator
            header-class="nav-section-header"
            :class="{ 'nav-section-active': sectionContainsActive(section) }"
            class="nav-section-tree"
            :icon="section.icon"
            :label="section.title"
          >
            <q-list class="nav-children">
              <template v-for="item in section.items">
                <q-expansion-item
                  v-if="item.children && item.children.length"
                  :key="item.key"
                  dense
                  dense-toggle
                  switch-toggle-side
                  expand-separator
                  :class="['nav-subtree', { 'nav-subtree--finance': section.key === 'financeMenu' }]"
                  :header-class="section.key === 'financeMenu' ? 'nav-subtree-header nav-subtree-header--finance' : 'nav-subtree-header'"
                  :value="isSectionExpanded(item.key)"
                  @input="setSectionExpanded(item.key, $event)"
                  :label="item.label"
                  :icon="section.key === 'financeMenu' ? void 0 : item.icon"
                >
                  <q-list class="nav-grand-children">
                    <q-item
                      v-for="child in item.children"
                      :key="child.key"
                      clickable
                      :to="{ name: child.routeName }"
                      @click="linkChange(child.key)"
                      v-ripple
                      exact
                      :active="link === child.key && link !== ''"
                      active-class="nav-item-active"
                      :class="['nav-item nav-item--child', { 'nav-item--finance-child': section.key === 'financeMenu' }]"
                    >
                      <q-item-section v-if="section.key !== 'financeMenu'" avatar class="nav-item-icon">
                        <q-icon :name="child.icon || 'chevron_right'" />
                      </q-item-section>
                      <q-item-section>
                        <div class="nav-item-label">{{ child.label }}</div>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-expansion-item>
                <q-item
                  v-else
                  :key="item.key"
                  clickable
                  :to="{ name: item.routeName }"
                  @click="linkChange(item.key)"
                  v-ripple
                  exact
                  :active="link === item.key && link !== ''"
                  active-class="nav-item-active"
                  class="nav-item"
                >
                  <q-item-section v-if="section.key !== 'financeMenu'" avatar class="nav-item-icon">
                    <q-icon :name="item.icon" />
                  </q-item-section>
                  <q-item-section>
                    <div class="nav-item-label">{{ item.label }}</div>
                  </q-item-section>
                </q-item>
              </template>
            </q-list>
          </q-expansion-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>
    <q-page-container
      class="main-page platform-page-container"
    >
      <div class="page-shell">
        <div class="page-shell-body">
          <router-view />
        </div>
      </div>
    </q-page-container>
    <q-dialog
      v-model="authid"
      transition-show="jump-down"
      transition-hide="jump-up"
    >
      <q-card style="min-width: 350px">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("index.your_openid") }}</div>
          <q-space></q-space>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip
              content-class="bg-amber text-black shadow-4"
              :offset="[20, 20]"
              content-style="font-size: 12px"
              >{{ $t("index.close") }}</q-tooltip
            >
          </q-btn>
        </q-bar>
        <q-card-section class="q-pt-md"
          ><q-input
            dense
            outlined
            square
            label="OpenID"
            v-model="openid"
            readonly
            disable
        /></q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="login"
      transition-show="jump-down"
      transition-hide="jump-up"
    >
      <q-card class="auth-dialog-card">
        <q-bar
          class="auth-dialog-bar text-white rounded-borders"
        >
          <div class="auth-dialog-title">手机号验证码登录</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip
              content-class="bg-amber text-black shadow-4"
              :offset="[20, 20]"
              content-style="font-size: 12px"
              >{{ $t("index.close") }}</q-tooltip
            >
          </q-btn>
        </q-bar>
        <q-card-section class="auth-dialog-section">
          <div class="auth-dialog-intro">
            使用手机号和验证码登录平台，适合国内物流后台的常见使用方式。
          </div>
          <q-input
            dense
            outlined
            square
            label="手机号"
            v-model="phoneLoginForm.phone"
            maxlength="11"
            autofocus
            @keyup.enter="phoneLogin()"
          />
          <div class="auth-code-row">
            <q-input
              class="auth-code-input"
              dense
              outlined
              square
              label="验证码"
              v-model="phoneLoginForm.code"
              maxlength="6"
              @keyup.enter="phoneLogin()"
            />
            <q-btn
              unelevated
              color="primary"
              class="auth-code-btn"
              :disable="loginCodeCountdown > 0"
              :label="loginCodeCountdown > 0 ? `${loginCodeCountdown}s 后重试` : '获取验证码'"
              @click="sendPhoneCode('login')"
            />
          </div>
          <div v-if="phoneLoginForm.debugCode" class="auth-debug-tip">
            当前开发验证码：{{ phoneLoginForm.debugCode }}
          </div>
        </q-card-section>
        <q-card-actions align="left" class="text-primary auth-dialog-actions">
          <q-btn
            color="primary"
            label="立即登录"
            class="full-width"
            @click="phoneLogin()"
          />
          <div class="q-mx-auto">
            <q-btn
              flat
              class="text-teal-4 q-mt-sm"
              @click="
                login = false;
                register = true;
              "
            >
              {{ $t("index.register_tip") }}
            </q-btn>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="register"
      transition-show="jump-down"
      transition-hide="jump-up"
    >
      <q-card class="auth-dialog-card">
        <q-bar
          class="auth-dialog-bar text-white rounded-borders"
        >
          <div class="auth-dialog-title">手机号注册</div>
          <q-space></q-space>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip
              content-class="bg-amber text-black shadow-4"
              :offset="[20, 20]"
              content-style="font-size: 12px"
              >{{ $t("index.close") }}</q-tooltip
            >
          </q-btn>
        </q-bar>
        <q-card-section class="auth-dialog-section">
          <div class="auth-dialog-intro">
            首次使用请先注册账号，注册完成后自动进入系统并生成演示数据。
          </div>
          <q-input
            dense
            outlined
            square
            label="企业昵称 / 用户名"
            v-model="phoneRegisterForm.name"
            autofocus
            @keyup.enter="phoneRegister()"
          />
          <q-input
            class="q-mt-sm"
            dense
            outlined
            square
            label="手机号"
            v-model="phoneRegisterForm.phone"
            maxlength="11"
            @keyup.enter="phoneRegister()"
          />
          <div class="auth-code-row">
            <q-input
              class="auth-code-input"
              dense
              outlined
              square
              label="验证码"
              v-model="phoneRegisterForm.code"
              maxlength="6"
              @keyup.enter="phoneRegister()"
            />
            <q-btn
              unelevated
              color="primary"
              class="auth-code-btn"
              :disable="registerCodeCountdown > 0"
              :label="registerCodeCountdown > 0 ? `${registerCodeCountdown}s 后重试` : '获取验证码'"
              @click="sendPhoneCode('register')"
            />
          </div>
          <div v-if="phoneRegisterForm.debugCode" class="auth-debug-tip">
            当前开发验证码：{{ phoneRegisterForm.debugCode }}
          </div>
        </q-card-section>
        <q-card-actions align="right" class="text-primary q-mx-sm"
          ><q-btn
            class="full-width"
            color="primary"
            label="注册并进入"
            @click="phoneRegister()"
        /></q-card-actions>
        <q-card-actions align="center" style="margin-top: -8px">
          <q-btn
            class="text-teal-4"
            flat
            :label="$t('index.return_to_login')"
            @click="
              login = true;
              register = false;
            "
          ></q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>
<script>
import { get, getauth, post } from 'boot/axios_request'
import { LocalStorage, SessionStorage } from 'quasar'
import Bus from 'boot/bus.js'

const NAV_SECTIONS = [
  {
    key: 'transport',
    icon: 'local_shipping',
    title: '运单管理',
    caption: '运单创建、审核、修改与回单处理',
    items: [
      { key: 'createwaybill', routeName: 'createwaybill', icon: 'post_add', label: '创建运单', caption: '录入运单、地址、费用与司机车辆信息' },
      { key: 'outbound', routeName: 'dn', icon: 'local_shipping', label: '运单列表', caption: '运单处理、拣货、发车与回单' },
      { key: 'freshorder', routeName: 'freshorder', icon: 'fact_check', label: '运单审核', caption: '计划单据审核与状态确认' },
      { key: 'neworder', routeName: 'neworder', icon: 'history_edu', label: '运单修改记录', caption: '查看运单变更与历史轨迹' },
      { key: 'pod', routeName: 'pod', icon: 'assignment_turned_in', label: '运单回单', caption: '签收回单与完结处理' }
    ]
  },
  {
    key: 'online',
    icon: 'timeline',
    title: '在途管理',
    caption: '在途跟踪、事件监控与费用查看',
    items: [
      { key: 'driver', routeName: 'driverlist', icon: 'person_pin_circle', label: '在线跟踪', caption: '查看在途运单、定位轨迹与实时监控' },
      { key: 'dispatchlist', routeName: 'dispatchlist', icon: 'receipt_long', label: '在途费用', caption: '查看在途费用、奖励与异常成本' }
    ]
  },
  {
    key: 'financeMenu',
    icon: 'account_balance_wallet',
    title: '财务管理',
    caption: '费用结算与客户对账',
    items: [
      {
        key: 'assessmentGroup',
        icon: 'fact_check',
        label: '考核管理',
        children: [
          { key: 'customerAssessment', routeName: 'customerAssessment', icon: 'assignment', label: '客户考核' },
          { key: 'capacityAssessment', routeName: 'capacityAssessment', icon: 'local_shipping', label: '运力考核' }
        ]
      },
      { key: 'directSettlement', routeName: 'directSettlement', icon: 'account_balance', label: '直接结算', caption: '直客费用与在途成本联动' },
      {
        key: 'upstreamGroup',
        icon: 'north',
        label: '上游对账',
        children: [
          { key: 'customerOrderCheck', routeName: 'customerpod', icon: 'receipt', label: '客户订单对账' },
          { key: 'customerdn', routeName: 'customerdnlist', icon: 'receipt_long', label: '客户运单对账' }
        ]
      },
      {
        key: 'downstreamGroup',
        icon: 'south',
        label: '下游对账',
        children: [
          { key: 'supplierasn', routeName: 'supplierasnlist', icon: 'inventory_2', label: '承运商对账' },
          { key: 'driverCheck', routeName: 'driverCheck', icon: 'badge', label: '司机对账' },
          { key: 'vehicleCheck', routeName: 'vehicleCheck', icon: 'directions_car', label: '车辆对账' }
        ]
      },
      { key: 'receiptbill', routeName: 'receiptbill', icon: 'payments', label: '收款单', caption: '客户回款与签收核验' },
      { key: 'paybill', routeName: 'paybill', icon: 'request_quote', label: '付款单', caption: '承运商与司机付款处理' },
      { key: 'driverexpense', routeName: 'driverexpense', icon: 'description', label: '司机报销单', caption: '司机补贴与费用报销' },
      { key: 'borrowmanage', routeName: 'borrowmanage', icon: 'credit_card', label: '借支管理', caption: '借支申请、核销与追踪' },
      { key: 'costmanage', routeName: 'costmanage', icon: 'pie_chart', label: '成本管理', caption: '线路、客户与项目成本分析' },
      { key: 'dailyincome', routeName: 'dailyincome', icon: 'receipt', label: '日常收支', caption: '零星收支与杂项费用登记' },
      { key: 'capitalflow', routeName: 'capitalflow', icon: 'account_tree', label: '资金流水', caption: '账户收支流水与资金去向' },
      { key: 'documentcenter', routeName: 'documentcenter', icon: 'folder_open', label: '单据中心', caption: '财务单据汇总与追踪' }
    ]
  },
  {
    key: 'companyMenu',
    icon: 'apartment',
    title: '公司管理',
    caption: '组织、客户与供应商档案',
    items: [
      { key: 'baseinfo', routeName: 'company', icon: 'business', label: '公司资料', caption: '公司、客户与供应商信息' }
    ]
  },
  {
    key: 'systemMenu',
    icon: 'settings',
    title: '系统管理',
    caption: '岗位权限与导入导出',
    items: [
      { key: 'staff', routeName: 'stafflist', icon: 'supervisor_account', label: '账号权限', caption: '账号、岗位与权限管理' },
      { key: 'uploadcenter', routeName: 'initializeupload', icon: 'cloud_upload', label: '数据导入', caption: '初始化导入与模板上传' },
      { key: 'downloadcenter', routeName: 'downloadinbound', icon: 'cloud_download', label: '数据导出', caption: '单据、库存与报表导出' }
    ]
  }
]

const TOP_NAV_ITEMS = [
  { key: 'home', label: '首页', routeName: 'web_index' },
  { key: 'dn', label: '运单列表', routeName: 'dn' },
  { key: 'createwaybill', label: '创建运单', routeName: 'createwaybill' },
  { key: 'freshorder', label: '运单审核', routeName: 'freshorder' },
  { key: 'driverlist', label: '在线跟踪', routeName: 'driverlist' },
  { key: 'dispatchlist', label: '在途费用', routeName: 'dispatchlist' },
  { key: 'customerdnlist', label: '客户运单对账', routeName: 'customerdnlist' },
  { key: 'customerpod', label: '客户订单对账', routeName: 'customerpod' }
]

const WAREHOUSE_NAME_MAP = {
  'Center Warehouse': '中心仓',
  'CENTER WAREHOUSE': '中心仓',
  'center warehouse': '中心仓'
}

const PAGE_META = {
  web_index: { section: '首页', title: '平台首页' },
  outbounddashboard: { section: '工作台', title: '运营总览' },
  inbounddashboard: { section: '工作台', title: '入库报表' },
  inboundAndOutbound: { section: '工作台', title: '出入库分析' },
  asn: { section: '仓储作业', title: '入库中心' },
  predeliverystock: { section: '仓储作业', title: '待到货管理' },
  preloadstock: { section: '仓储作业', title: '待卸货管理' },
  presortstock: { section: '仓储作业', title: '待分拣管理' },
  sortstock: { section: '仓储作业', title: '已分拣管理' },
  shortage: { section: '仓储作业', title: '短少异常' },
  more: { section: '仓储作业', title: '更多处理' },
  asnfinish: { section: '仓储作业', title: '入库完成' },
  createwaybill: { section: '运单管理', title: '创建运单' },
  dn: { section: '运单管理', title: '运单列表' },
  freshorder: { section: '运单管理', title: '新建订单' },
  neworder: { section: '运单管理', title: '新增订单' },
  pickstock: { section: '运单管理', title: '待拣货任务' },
  pickedstock: { section: '运单管理', title: '已拣货任务' },
  shippedstock: { section: '运单管理', title: '已发货订单' },
  backorder: { section: '运单管理', title: '回单管理' },
  pod: { section: '运单管理', title: '签收回单' },
  stocklist: { section: '仓储作业', title: '库存台账' },
  stockbinlist: { section: '仓储作业', title: '库位库存' },
  emptybin: { section: '仓储作业', title: '空库位管理' },
  occupiedbin: { section: '仓储作业', title: '占用库位管理' },
  cyclecount: { section: '仓储作业', title: '动态盘点' },
  cyclecountrecorder: { section: '仓储作业', title: '盘点记录' },
  handcount: { section: '仓储作业', title: '手工盘点' },
  handcountrecorder: { section: '仓储作业', title: '手工盘点记录' },
  goodslist: { section: '主数据', title: '商品资料' },
  goodsunit: { section: '主数据', title: '商品单位' },
  goodsclass: { section: '主数据', title: '商品分类' },
  goodsbrand: { section: '主数据', title: '商品品牌' },
  goodscolor: { section: '主数据', title: '商品颜色' },
  goodsspecs: { section: '主数据', title: '商品规格' },
  goodsshape: { section: '主数据', title: '商品形状' },
  goodsorigin: { section: '主数据', title: '商品产地' },
  company: { section: '主数据', title: '公司资料' },
  supplier: { section: '主数据', title: '供应商资料' },
  customer: { section: '主数据', title: '客户资料' },
  warehouseset: { section: '仓储作业', title: '仓库配置' },
  binset: { section: '仓储作业', title: '库位配置' },
  binsize: { section: '仓储作业', title: '库位尺寸' },
  property: { section: '仓储作业', title: '库位属性' },
  capitallist: { section: '主数据', title: '固定资产' },
  freight: { section: '主数据', title: '运费规则' },
  stafflist: { section: '平台管理', title: '人员管理' },
  stafflist_check_code: { section: '平台管理', title: '校验码管理' },
  stafftype: { section: '平台管理', title: '岗位管理' },
  driverlist: { section: '在途管理', title: '在线跟踪' },
  dispatchlist: { section: '在途管理', title: '在途费用' },
  customerdnlist: { section: '财务管理', title: '客户运单对账' },
  customerpod: { section: '财务管理', title: '客户订单对账' },
  supplierasnlist: { section: '财务管理', title: '承运商对账' },
  supplierasnfinish: { section: '财务管理', title: '承运商明细' },
  customerAssessment: { section: '财务管理', title: '客户考核' },
  capacityAssessment: { section: '财务管理', title: '运力考核' },
  directSettlement: { section: '财务管理', title: '直接结算' },
  driverCheck: { section: '财务管理', title: '司机对账' },
  vehicleCheck: { section: '财务管理', title: '车辆对账' },
  receiptbill: { section: '财务管理', title: '收款单' },
  paybill: { section: '财务管理', title: '付款单' },
  driverexpense: { section: '财务管理', title: '司机报销单' },
  borrowmanage: { section: '财务管理', title: '借支管理' },
  costmanage: { section: '财务管理', title: '成本管理' },
  dailyincome: { section: '财务管理', title: '日常收支' },
  capitalflow: { section: '财务管理', title: '资金流水' },
  documentcenter: { section: '财务管理', title: '单据中心' },
  initializeupload: { section: '平台管理', title: '初始化导入' },
  addupload: { section: '平台管理', title: '新增导入' },
  uploadlist: { section: '平台管理', title: '导入记录' },
  downloadinbound: { section: '平台管理', title: '入库导出' },
  downloadoutbound: { section: '平台管理', title: '出库导出' },
  downloadstocklist: { section: '平台管理', title: '库存导出' },
  downloadgoodslist: { section: '平台管理', title: '商品导出' },
  downloadbinlist: { section: '平台管理', title: '库位导出' }
}

const ROUTE_LINK_MAP = {
  outbounddashboard: 'outbounddashboard',
  inbounddashboard: 'outbounddashboard',
  inboundAndOutbound: 'outbounddashboard',
  asn: 'inbound',
  predeliverystock: 'inbound',
  preloadstock: 'inbound',
  presortstock: 'inbound',
  sortstock: 'inbound',
  shortage: 'inbound',
  more: 'inbound',
  asnfinish: 'inbound',
  createwaybill: 'createwaybill',
  dn: 'outbound',
  freshorder: 'freshorder',
  neworder: 'neworder',
  pickstock: 'outbound',
  pickedstock: 'outbound',
  pickinglist: 'outbound',
  shippedstock: 'outbound',
  backorder: 'outbound',
  pod: 'pod',
  stocklist: 'stock',
  stockbinlist: 'stock',
  emptybin: 'stock',
  occupiedbin: 'stock',
  cyclecount: 'stock',
  cyclecountrecorder: 'stock',
  handcount: 'stock',
  handcountrecorder: 'stock',
  goodslist: 'goods',
  goodsunit: 'goods',
  goodsclass: 'goods',
  goodsbrand: 'goods',
  goodscolor: 'goods',
  goodsspecs: 'goods',
  goodsshape: 'goods',
  goodsorigin: 'goods',
  company: 'baseinfo',
  supplier: 'baseinfo',
  customer: 'baseinfo',
  warehouseset: 'warehouse',
  binset: 'warehouse',
  binsize: 'warehouse',
  property: 'warehouse',
  capitallist: 'finance',
  freight: 'finance',
  stafflist: 'staff',
  stafflist_check_code: 'staff',
  stafftype: 'staff',
  driverlist: 'driver',
  dispatchlist: 'driver',
  customerdnlist: 'customerdn',
  customerpod: 'customerOrderCheck',
  supplierasnlist: 'supplierasn',
  supplierasnfinish: 'supplierasn',
  customerAssessment: 'customerAssessment',
  capacityAssessment: 'capacityAssessment',
  directSettlement: 'directSettlement',
  driverCheck: 'driverCheck',
  vehicleCheck: 'vehicleCheck',
  receiptbill: 'receiptbill',
  paybill: 'paybill',
  driverexpense: 'driverexpense',
  borrowmanage: 'borrowmanage',
  costmanage: 'costmanage',
  dailyincome: 'dailyincome',
  capitalflow: 'capitalflow',
  documentcenter: 'documentcenter',
  supplierasnfinish: 'supplierasn',
  initializeupload: 'uploadcenter',
  addupload: 'uploadcenter',
  uploadlist: 'uploadcenter',
  downloadinbound: 'downloadcenter',
  downloadoutbound: 'downloadcenter',
  downloadstocklist: 'downloadcenter',
  downloadgoodslist: 'downloadcenter',
  downloadbinlist: 'downloadcenter'
}

export default {
  computed: {
    navSections () {
      return NAV_SECTIONS
    },
    topNavItems () {
      return TOP_NAV_ITEMS
    },
    currentPageMeta () {
      return PAGE_META[this.$route.name] || { section: '业务中心', title: '物流平台' }
    },
    filteredNavSections () {
      return this.navSections
    }
  },
  data () {
    return {
      device: LocalStorage.getItem('device'),
      device_name: LocalStorage.getItem('device_name'),
      lang: this.$i18n.locale,
      warehouse_name: '',
      warehouseOptions: [],
      title: this.$t('index.webtitle'),
      openid: '',
      authin: '0',
      authid: false,
      left: false,
      drawerleft: false,
      tab: '',
      login: false,
      link: '',
      login_name: '',
      login_id: 0,
      register: false,
      phoneLoginForm: {
        phone: '',
        code: '',
        debugCode: ''
      },
      phoneRegisterForm: {
        name: '',
        phone: '',
        code: '',
        debugCode: ''
      },
      loginCodeCountdown: 0,
      registerCodeCountdown: 0,
      loginCodeTimer: null,
      registerCodeTimer: null,
      needLogin: '',
      expandedSections: {
        transport: true,
        online: false,
        financeMenu: false,
        assessmentGroup: true,
        upstreamGroup: true,
        downstreamGroup: false,
        companyMenu: false,
        systemMenu: false
      }
    }
  },
  methods: {
    displayWarehouseName (name) {
      const rawName = (name || '').trim()
      if (!rawName) {
        return ''
      }
      if (WAREHOUSE_NAME_MAP[rawName]) {
        return WAREHOUSE_NAME_MAP[rawName]
      }
      const normalizedName = rawName.toLowerCase()
      if (normalizedName === 'center warehouse') {
        return '中心仓'
      }
      return rawName
    },
    navigateTopMenu (item) {
      if (!item || !item.routeName || item.routeName === this.$route.name) {
        return
      }
      this.$router.push({ name: item.routeName })
    },
    topNavActive (item) {
      return item && item.routeName === this.$route.name
    },
    linkChange (e) {
      localStorage.removeItem('menulink')
      localStorage.setItem('menulink', e)
      this.link = e
      this.ensureCurrentSectionExpanded()
    },
    isSectionExpanded (key) {
      return this.expandedSections[key] === true
    },
    setSectionExpanded (key, value) {
      this.$set(this.expandedSections, key, value)
    },
    sectionContainsActive (section) {
      return section.items.some(item => {
        if (item.key === this.link) {
          return true
        }
        return Array.isArray(item.children) && item.children.some(child => child.key === this.link)
      })
    },
    ensureCurrentSectionExpanded () {
      this.navSections.forEach(section => {
        if (section.items.some(item => item.key === this.link || (Array.isArray(item.children) && item.children.some(child => child.key === this.link)))) {
          this.$set(this.expandedSections, section.key, true)
        }
        section.items.forEach(item => {
          if (Array.isArray(item.children) && item.children.some(child => child.key === this.link)) {
            this.$set(this.expandedSections, item.key, true)
          }
        })
      })
    },
    drawerClick (e) {
      if (this.miniState) {
        this.miniState = false
        e.stopPropagation()
      }
    },
    showNotify (message, color = 'negative', icon = 'close') {
      this.$q.notify({ message, color, icon })
    },
    validPhone (phone) {
      return /^1\d{10}$/.test((phone || '').trim())
    },
    startCodeCountdown (scene) {
      const countdownKey = scene === 'register' ? 'registerCodeCountdown' : 'loginCodeCountdown'
      const timerKey = scene === 'register' ? 'registerCodeTimer' : 'loginCodeTimer'
      if (this[timerKey]) {
        clearInterval(this[timerKey])
      }
      this[countdownKey] = 60
      this[timerKey] = window.setInterval(() => {
        if (this[countdownKey] <= 1) {
          clearInterval(this[timerKey])
          this[timerKey] = null
          this[countdownKey] = 0
          return
        }
        this[countdownKey] -= 1
      }, 1000)
    },
    sendPhoneCode (scene) {
      const form = scene === 'register' ? this.phoneRegisterForm : this.phoneLoginForm
      const phone = (form.phone || '').trim()
      if (!this.validPhone(phone)) {
        this.showNotify('请输入正确的11位手机号')
        return
      }
      SessionStorage.set('axios_check', 'false')
      post('login/send_code/', { phone, scene })
        .then((res) => {
          if (res.code === '200') {
            form.debugCode = res.data.debug_code || ''
            this.startCodeCountdown(scene)
            this.showNotify(`验证码已生成，当前开发验证码：${form.debugCode}`, 'green', 'check')
          } else {
            this.showNotify(res.msg || '验证码发送失败')
          }
        })
        .catch((err) => {
          this.showNotify(err.detail || '验证码发送失败')
        })
    },
    applyPhoneAuth (data, mode = 'phone') {
      this.authin = '1'
      this.login = false
      this.register = false
      this.openid = data.openid
      this.login_name = data.name
      this.login_id = data.user_id
      LocalStorage.set('auth', '1')
      LocalStorage.set('openid', data.openid)
      LocalStorage.set('login_name', data.name)
      LocalStorage.set('login_id', data.user_id)
      LocalStorage.set('login_mode', mode)
      this.showNotify('登录成功', 'green', 'check')
      this.staffType()
      localStorage.removeItem('menulink')
      this.link = ''
      this.$router.push({ name: 'web_index' })
      window.setTimeout(() => {
        location.reload()
      }, 1)
    },
    phoneLogin () {
      const payload = {
        phone: (this.phoneLoginForm.phone || '').trim(),
        code: (this.phoneLoginForm.code || '').trim()
      }
      if (!this.validPhone(payload.phone)) {
        this.showNotify('请输入正确的11位手机号')
        return
      }
      if (!payload.code) {
        this.showNotify('请输入验证码')
        return
      }
      SessionStorage.set('axios_check', 'false')
      post('login/', payload)
        .then((res) => {
          if (res.code === '200') {
            this.applyPhoneAuth(res.data, 'phone')
          } else {
            this.showNotify(res.msg || '登录失败')
          }
        })
        .catch((err) => {
          this.showNotify(err.detail || '登录失败')
        })
    },
    Logout () {
      this.authin = '0'
      this.login_name = ''
      LocalStorage.remove('auth')
      SessionStorage.remove('axios_check')
      LocalStorage.set('login_name', '')
      LocalStorage.set('login_id', '')
      this.showNotify('已退出登录', 'negative', 'check')
      localStorage.removeItem('menulink')
      this.link = ''
      this.$router.push({ name: 'web_index' })
      window.setTimeout(() => {
        location.reload()
      }, 1)
    },
    phoneRegister () {
      const payload = {
        name: (this.phoneRegisterForm.name || '').trim(),
        phone: (this.phoneRegisterForm.phone || '').trim(),
        code: (this.phoneRegisterForm.code || '').trim()
      }
      if (!this.validPhone(payload.phone)) {
        this.showNotify('请输入正确的11位手机号')
        return
      }
      if (!payload.code) {
        this.showNotify('请输入验证码')
        return
      }
      SessionStorage.set('axios_check', 'false')
      post('register/', payload)
        .then((res) => {
          if (res.code === '200') {
            this.phoneRegisterForm = { name: '', phone: '', code: '', debugCode: '' }
            this.applyPhoneAuth(res.data, 'phone')
          } else {
            this.showNotify(res.msg || '注册失败')
          }
        })
        .catch((err) => {
          this.showNotify(err.detail || '注册失败')
        })
    },
    staffType () {
      getauth('staff/?staff_name=' + this.login_name).then((res) => {
        if (res.results && res.results.length > 0) {
          LocalStorage.set('staff_type', res.results[0].staff_type)
        }
      })
    },
    warehouseOptionsGet () {
      get('warehouse/multiple/?max_page=30')
        .then((res) => {
          if (res.count === 1) {
            this.openid = res.results[0].openid
            this.warehouse_name = res.results[0].warehouse_name
            LocalStorage.set('openid', this.openid)
          } else {
            this.warehouseOptions = res.results
            if (LocalStorage.has('openid')) {
              this.warehouseOptions.forEach((item) => {
                if (item.openid === LocalStorage.getItem('openid')) {
                  this.warehouse_name = item.warehouse_name
                }
              })
            }
          }
        })
        .catch((err) => {
          console.log(err)
          this.showNotify(err.detail || '仓库加载失败')
        })
    },
    warehouseChange (e) {
      this.warehouse_name = this.warehouseOptions[e].warehouse_name
      this.openid = this.warehouseOptions[e].openid
      LocalStorage.set('openid', this.openid)
      LocalStorage.set('staff_type', 'Admin')
      this.login_name = ''
      LocalStorage.set('login_name', '')
      this.authin = '0'
      this.isLoggedIn()
      LocalStorage.remove('auth')
      SessionStorage.remove('axios_check')
    },
    langChange (e) {
      this.lang = e
      window.setTimeout(() => {
        location.reload()
      }, 1)
    },
    syncLinkFromRoute () {
      const currentLink = ROUTE_LINK_MAP[this.$route.name] || localStorage.getItem('menulink') || 'outbounddashboard'
      this.link = currentLink
      localStorage.setItem('menulink', currentLink)
    },
    isLoggedIn () {
      this.register = false
      this.login = true
    }
  },
  created () {
    if (LocalStorage.has('openid')) {
      this.openid = LocalStorage.getItem('openid')
    } else {
      this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      this.login_name = LocalStorage.getItem('login_name')
    } else {
      this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
      this.authin = '1'
      this.staffType()
    } else {
      LocalStorage.set('staff_type', 'Admin')
      this.authin = '0'
      this.isLoggedIn()
    }
  },
  mounted () {
    this.warehouseOptionsGet()
    this.syncLinkFromRoute()
    this.ensureCurrentSectionExpanded()
    Bus.$on('needLogin', () => {
      this.isLoggedIn()
    })
    Bus.$on('openLoginDialog', () => {
      this.login = true
      this.register = false
    })
    Bus.$on('openRegisterDialog', () => {
      this.register = true
      this.login = false
    })
  },
  beforeDestroy () {
    Bus.$off('needLogin')
    Bus.$off('openLoginDialog')
    Bus.$off('openRegisterDialog')
    if (this.loginCodeTimer) {
      clearInterval(this.loginCodeTimer)
    }
    if (this.registerCodeTimer) {
      clearInterval(this.registerCodeTimer)
    }
  },
  watch: {
    '$route.name' () {
      this.syncLinkFromRoute()
      this.ensureCurrentSectionExpanded()
    },
    lang (lang) {
      LocalStorage.set('lang', lang)
      this.$i18n.locale = lang
    }
  }
}
</script>
<style>
html,
body,
#q-app,
.q-layout,
.q-page-container,
.q-page {
  min-height: 100%;
}

body {
  overflow-x: hidden;
  overflow-y: auto;
}

.platform-layout {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(24, 119, 242, 0.12), transparent 28%),
    linear-gradient(180deg, #eef4fb 0%, #f6f8fc 100%);
}

.platform-header {
  background: linear-gradient(90deg, #26136d 0%, #2f167c 40%, #2a1468 100%);
}

.platform-toolbar {
  min-height: 46px;
  padding: 0 10px 0 0;
  gap: 6px;
}

.mobile-menu-btn {
  flex: 0 0 auto;
  margin-left: 6px;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 176px;
  height: 46px;
  padding: 0 12px 0 8px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.06);
}

.brand-logo {
  width: 42px;
  height: 42px;
  object-fit: contain;
}

.brand-copy {
  min-width: 0;
}

.brand-title {
  font-size: 15px;
  line-height: 1.1;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.brand-subtitle {
  margin-top: 2px;
  font-size: 9px;
  color: rgba(255, 255, 255, 0.72);
  letter-spacing: 0.12em;
}

.top-nav {
  display: flex;
  align-items: center;
  height: 46px;
  overflow-x: auto;
  max-width: 620px;
  scrollbar-width: none;
}

.top-nav::-webkit-scrollbar {
  display: none;
}

.top-nav-item {
  height: 46px;
  padding: 0 16px;
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.82);
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
}

.top-nav-item.active {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-weight: 700;
}

.warehouse-switcher {
  margin: 0 6px 0 0;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.08);
}

.ghost-access-btn {
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.24);
  background: rgba(255, 255, 255, 0.06);
}

.primary-access-btn {
  border-radius: 999px;
  background: linear-gradient(135deg, #2c7df0 0%, #43a1ff 100%);
  box-shadow: 0 12px 28px rgba(45, 125, 240, 0.3);
}

.header-divider {
  margin-right: 8px;
}

.platform-drawer {
  overflow: hidden;
  background: linear-gradient(180deg, #ffffff 0%, #fbfcff 100%);
  color: #2b3550;
}

.drawer-user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 8px 10px;
  padding: 10px 8px;
  border-bottom: 1px solid #edf0f6;
}

.drawer-user-avatar {
  background: #eff3ff;
}

.drawer-user-info {
  flex: 1;
  min-width: 0;
}

.drawer-user-name {
  font-size: 14px;
  font-weight: 700;
  color: #27324a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drawer-user-role {
  margin-top: 4px;
  font-size: 11px;
  color: #7e8aa3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drawer-nav-list {
  padding: 8px 6px 20px;
}

.nav-section-tree {
  margin-bottom: 6px;
  border-radius: 12px;
  overflow: hidden;
}

.nav-section-header {
  min-height: 42px;
  padding: 0 6px;
  border-radius: 12px;
  color: #33415c;
  font-size: 13px;
  font-weight: 600;
}

.nav-section-tree:hover .nav-section-header {
  background: #f5f7fc;
}

.nav-section-active .nav-section-header {
  color: #5b33d6;
  background: #f4f0ff;
}

.nav-children {
  padding: 4px 0 8px;
}

.nav-subtree {
  margin: 2px 0;
}

.nav-subtree-header {
  min-height: 38px;
  margin: 2px 6px 2px 14px;
  border-radius: 10px;
  color: #607089;
}

.nav-subtree-header--finance {
  min-height: 72px;
  margin: 8px 2px 2px 6px;
  padding-left: 2px;
  padding-right: 2px;
  border-top: 1px solid #dde3ef;
  border-radius: 0;
}

.nav-subtree:hover .nav-subtree-header {
  background: #f5f7fc;
}

.nav-subtree--finance:hover .nav-subtree-header--finance {
  background: transparent;
}

.nav-subtree--finance :deep(.q-item__label) {
  writing-mode: vertical-rl;
  text-orientation: upright;
  letter-spacing: 1px;
  line-height: 1.1;
  font-size: 11px;
  font-weight: 600;
  color: #5f6f89;
}

.nav-subtree--finance :deep(.q-item__section--main) {
  align-items: center;
  justify-content: center;
  min-width: 18px;
}

.nav-subtree--finance :deep(.q-item) {
  justify-content: space-between;
}

.nav-subtree--finance :deep(.q-item__section--side) {
  min-width: 16px;
  padding-right: 0;
  padding-left: 0;
  color: #7a7f88;
}

.nav-subtree--finance :deep(.q-expansion-item__toggle-icon) {
  font-size: 34px;
  font-weight: 700;
}

.nav-grand-children {
  position: relative;
  padding: 2px 0 4px;
}

.nav-grand-children::before {
  content: '';
  position: absolute;
  left: 23px;
  top: 0;
  bottom: 6px;
  width: 1px;
  background: #d4dbe8;
}

.nav-item {
  position: relative;
  min-height: 38px;
  margin: 2px 6px 2px 14px;
  padding-left: 2px;
  border-radius: 10px;
  color: #56657f;
}

.nav-item:hover {
  background: #f5f7fc;
}

.nav-item--child {
  margin-left: 28px;
}

.nav-item--finance-child {
  margin: -1px 2px 0 14px;
  min-height: 28px;
  padding-left: 0;
  border-radius: 0;
  background: transparent;
}

.nav-item--finance-child .nav-item-label {
  font-size: 11px;
  color: #5a6780;
  line-height: 1.05;
}

.nav-item--finance-child:hover {
  background: transparent;
}

.nav-item--finance-child.nav-item-active {
  background: transparent;
}

.nav-item--finance-child.nav-item-active::before {
  left: -8px;
  top: 4px;
  bottom: 4px;
  width: 2px;
}

.nav-item--finance-child .nav-item-label {
  white-space: nowrap;
}

.nav-item--finance-child::after {
  content: '';
  position: absolute;
  left: -10px;
  top: 14px;
  width: 6px;
  height: 1px;
  background: #d4dbe8;
}

.nav-item--child::after {
  content: '';
  position: absolute;
  left: -16px;
  top: 18px;
  width: 12px;
  height: 1px;
  background: #d8deeb;
}

.nav-item-active {
  color: #5b33d6;
  background: #f2ecff;
}

.nav-item-active::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6b45f6 0%, #8b63ff 100%);
}

.nav-item-icon {
  min-width: 28px;
  color: #8e99b1;
}

.nav-item-label {
  font-size: 13px;
  font-weight: 500;
}

.nav-item-active .nav-item-icon,
.nav-item-active .nav-item-label {
  color: #5b33d6;
}

.nav-section-tree :deep(.q-item__section--avatar) {
  min-width: 30px;
}

.nav-section-tree :deep(.q-expansion-item__toggle-icon) {
  color: #98a3b9;
}

.nav-section-tree :deep(.q-expansion-item__content) {
  background: transparent;
}

.platform-page-container {
  padding: 8px;
  min-height: calc(100vh - 62px);
  overflow: auto;
}

.page-shell {
  min-height: calc(100vh - 62px);
  width: 100%;
}

.page-shell-body {
  padding: 0;
  min-width: 0;
  overflow-x: auto;
  overflow-y: auto;
}

.page-shell-body > * {
  width: 100%;
  min-width: 0;
}

.auth-dialog-card {
  min-width: 420px;
  width: min(92vw, 420px);
  border-radius: 20px;
  overflow: hidden;
}
.auth-dialog-bar {
  height: 56px;
  padding: 0 16px;
  background: linear-gradient(90deg, #17355f 0%, #24528f 100%);
}
.auth-dialog-title {
  font-size: 16px;
  font-weight: 700;
}
.auth-dialog-section {
  padding: 18px 20px 12px;
}
.auth-dialog-intro {
  margin-bottom: 14px;
  font-size: 13px;
  line-height: 1.6;
  color: #60708f;
}

.user-brief-tip {
  font-size: 12px;
  line-height: 1.6;
  color: #6d7991;
}
.auth-code-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.auth-code-input {
  flex: 1;
}
.auth-code-btn {
  min-width: 128px;
}
.auth-debug-tip {
  margin-top: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  background: #eef5ff;
  color: #24528f;
  font-size: 12px;
}
.auth-dialog-actions {
  padding: 0 20px 18px;
}

.tabs .q-tab__indicator {
  width: 25%;
  height: 1.5px;
  margin: auto;
  color: #d6d7d7;
}
.tabs .absolute-bottom {
  bottom: 8px;
}

@media (max-width: 1024px) {
  .brand-block {
    min-width: 0;
    flex: 1;
    padding-right: 8px;
  }

  .top-nav {
    max-width: 34vw;
  }

  .platform-page-container {
    padding: 6px;
  }

  .page-shell {
    min-height: calc(100vh - 56px);
  }
}

@media (max-width: 768px) {
  .platform-toolbar {
    min-height: 52px;
    padding-right: 6px;
    flex-wrap: wrap;
    align-content: center;
  }

  .top-nav {
    order: 3;
    flex: 1 0 100%;
    max-width: 100%;
    height: 40px;
    padding: 0 4px 6px;
  }

  .top-nav-item {
    height: 36px;
    padding: 0 12px;
  }

  .brand-block {
    gap: 8px;
    min-width: 0;
    height: 42px;
    padding-left: 6px;
  }

  .brand-logo {
    width: 34px;
    height: 34px;
  }

  .brand-title {
    font-size: 13px;
  }

  .brand-subtitle {
    font-size: 8px;
    letter-spacing: 0.08em;
  }

  .warehouse-switcher,
  .account-switcher,
  .demo-access-btn,
  .ghost-access-btn,
  .primary-access-btn {
    margin-left: 0 !important;
  }

  .header-divider {
    display: none;
  }

  .platform-page-container {
    padding: 4px;
  }

  .auth-code-row {
    flex-direction: column;
  }

  .auth-code-btn {
    width: 100%;
    min-width: 0;
  }
}

@media (max-width: 480px) {
  .brand-subtitle {
    display: none;
  }

  .top-nav {
    padding-bottom: 4px;
  }

  .auth-dialog-card {
    width: 94vw;
    min-width: 0;
  }
}
</style>

