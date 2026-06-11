<template>
  <q-layout view="hHh Lpr fFf" class="platform-layout">
    <q-header class="platform-header text-white">
      <q-toolbar class="platform-toolbar">
        <q-btn
          v-if="$q.screen.lt.md"
          dense
          flat
          round
          icon="menu"
          color="white"
          @click="drawerleft = !drawerleft"
        />
        <div class="brand-block" @click="$router.push({ name: 'web_index' })">
          <img src="statics/icons/logo.png" alt="WMS Demo" class="brand-logo">
          <div>
            <div class="brand-title">68 卡运联盟</div>
            <div class="brand-subtitle">物流运输协同平台</div>
          </div>
        </div>

        <q-space />

        <div class="header-actions">
          <q-input
            dense
            standout="bg-white text-dark"
            placeholder="让查单更简单"
            class="header-search"
          >
            <template v-slot:prepend>
              <q-icon name="search" color="grey-6" />
            </template>
          </q-input>
          <q-btn color="primary" class="create-btn" label="创建运单" @click="goRoute('createwaybill')" />
          <q-btn flat dense color="white" label="平台跳转" />
        </div>

        <template v-if="authin === '1'">
          <q-btn-dropdown flat color="white" :label="login_name || '平台用户'">
            <q-list style="min-width: 180px">
              <q-item clickable v-close-popup>
                <q-item-section>当前仓库：{{ displayWarehouseName(warehouse_name) || '默认仓库' }}</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="Logout()">
                <q-item-section>退出登录</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
        <template v-else>
          <q-btn flat color="white" label="登录" @click="openLogin('code')" />
          <q-btn color="primary" label="注册" @click="openRegister()" />
        </template>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawerleft"
      bordered
      :show-if-above="$q.screen.gt.sm"
      :width="186"
      content-class="platform-drawer"
    >
      <q-scroll-area class="fit">
        <div class="drawer-user-card">
          <div class="user-avatar-wrap">
            <img src="statics/staff/stafftype.png" alt="avatar" class="user-avatar">
          </div>
          <div class="drawer-user-info">
            <div class="drawer-user-name">{{ login_name || '平台用户' }}</div>
            <div class="drawer-user-role">{{ displayWarehouseName(warehouse_name) || '西安莲湖白金昌' }}</div>
          </div>
        </div>

        <div class="drawer-search-wrap">
          <q-input dense outlined placeholder="快捷搜索" class="drawer-search">
            <template v-slot:prepend>
              <q-icon name="search" size="16px" color="grey-6" />
            </template>
          </q-input>
        </div>

        <q-list class="nav-list">
          <q-expansion-item
            v-for="section in navSections"
            :key="section.key"
            :value="expandedSections[section.key]"
            @input="setExpanded(section.key, $event)"
            dense
            expand-separator
            switch-toggle-side
            header-class="nav-section-header"
            :icon="section.icon"
            :label="section.title"
          >
            <q-list class="nav-children">
              <template v-for="item in section.items">
                <q-item
                  v-if="!item.children"
                  :key="item.key"
                  clickable
                  :active="isActiveRoute(item.routeName)"
                  active-class="nav-item-active"
                  class="nav-item-child"
                  @click="goRoute(item.routeName)"
                >
                  <q-item-section>{{ item.label }}</q-item-section>
                </q-item>
                <q-expansion-item
                  v-else
                  :key="item.key"
                  :value="expandedSections[item.key]"
                  @input="setExpanded(item.key, $event)"
                  dense
                  switch-toggle-side
                  header-class="nav-subgroup-header"
                  :label="item.label"
                >
                  <q-list class="nav-grand-children">
                    <q-item
                      v-for="child in item.children"
                      :key="child.key"
                      clickable
                      :active="isActiveRoute(child.routeName)"
                      active-class="nav-item-active"
                      class="nav-item-grandchild"
                      @click="goRoute(child.routeName)"
                    >
                      <q-item-section>{{ child.label }}</q-item-section>
                    </q-item>
                  </q-list>
                </q-expansion-item>
              </template>
            </q-list>
          </q-expansion-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container class="platform-page-container">
      <div class="page-tabs">
        <button
          v-for="tab in openTabs"
          :key="tab.key"
          type="button"
          :class="['page-tab', { active: activeTabKey === tab.key }]"
          @click="navigateTab(tab)"
        >
          <span>{{ tab.label }}</span>
          <span v-if="tab.closable" class="page-tab-close" @click.stop="closeTab(tab)">×</span>
        </button>
      </div>
      <div class="page-shell">
        <router-view />
      </div>
    </q-page-container>

    <q-dialog v-model="login">
      <q-card class="auth-dialog-card">
        <q-bar class="auth-dialog-bar text-white">
          <div class="auth-dialog-title">{{ loginMode === 'code' ? '验证码登录' : '密码登录' }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup />
        </q-bar>
        <q-card-section class="auth-dialog-section">
          <div class="auth-mode-switch">
            <q-btn flat :color="loginMode === 'code' ? 'primary' : 'grey-7'" label="验证码登录" @click="loginMode = 'code'" />
            <q-btn flat :color="loginMode === 'password' ? 'primary' : 'grey-7'" label="密码登录" @click="loginMode = 'password'" />
          </div>

          <q-input dense outlined label="手机号" v-model="loginPhoneValue" maxlength="11" />

          <template v-if="loginMode === 'code'">
            <div class="auth-code-row">
              <q-input dense outlined class="auth-code-input" label="验证码" v-model="phoneLoginForm.code" maxlength="6" />
              <q-btn
                color="primary"
                unelevated
                class="auth-code-btn"
                :disable="loginCodeCountdown > 0"
                :label="loginCodeCountdown > 0 ? `${loginCodeCountdown}s 后重试` : '获取验证码'"
                @click="sendPhoneCode('login')"
              />
            </div>
            <div v-if="phoneLoginForm.debugCode" class="auth-debug-tip">当前开发验证码：{{ phoneLoginForm.debugCode }}</div>
          </template>

          <template v-else>
            <q-input dense outlined type="password" label="登录密码" v-model="passwordLoginForm.password" />
          </template>
        </q-card-section>
        <q-card-actions align="right" class="auth-dialog-actions">
          <q-btn flat label="去注册" @click="login = false; openRegister()" />
          <q-btn color="primary" :label="loginMode === 'code' ? '立即登录' : '密码登录'" @click="submitLogin()" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="register">
      <q-card class="auth-dialog-card">
        <q-bar class="auth-dialog-bar text-white">
          <div class="auth-dialog-title">手机号注册</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup />
        </q-bar>
        <q-card-section class="auth-dialog-section">
          <q-input dense outlined label="企业昵称 / 用户名" v-model="phoneRegisterForm.name" />
          <q-input dense outlined label="手机号" v-model="phoneRegisterForm.phone" maxlength="11" />
          <div class="auth-code-row">
            <q-input dense outlined class="auth-code-input" label="验证码" v-model="phoneRegisterForm.code" maxlength="6" />
            <q-btn
              color="primary"
              unelevated
              class="auth-code-btn"
              :disable="registerCodeCountdown > 0"
              :label="registerCodeCountdown > 0 ? `${registerCodeCountdown}s 后重试` : '获取验证码'"
              @click="sendPhoneCode('register')"
            />
          </div>
          <div v-if="phoneRegisterForm.debugCode" class="auth-debug-tip">当前开发验证码：{{ phoneRegisterForm.debugCode }}</div>
          <q-input dense outlined type="password" label="登录密码" v-model="phoneRegisterForm.password" />
          <q-input dense outlined type="password" label="确认密码" v-model="phoneRegisterForm.password_confirm" />
        </q-card-section>
        <q-card-actions align="right" class="auth-dialog-actions">
          <q-btn flat label="返回登录" @click="register = false; openLogin('code')" />
          <q-btn color="primary" label="注册并进入" @click="phoneRegister()" />
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
    icon: 'event_note',
    title: '运单管理',
    items: [
      { key: 'createwaybill', routeName: 'createwaybill', label: '创建运单' },
      { key: 'dn', routeName: 'dn', label: '运单列表' },
      { key: 'freshorder', routeName: 'freshorder', label: '运单审核' },
      { key: 'neworder', routeName: 'neworder', label: '运单修改记录' },
      { key: 'pod', routeName: 'pod', label: '运单回单' }
    ]
  },
  {
    key: 'online',
    icon: 'local_shipping',
    title: '在途管理',
    items: [
      { key: 'driverlist', routeName: 'driverlist', label: '在线跟踪' },
      { key: 'dispatchlist', routeName: 'dispatchlist', label: '在途费用' }
    ]
  },
  {
    key: 'finance',
    icon: 'account_balance_wallet',
    title: '财务管理',
    items: [
      {
        key: 'financeUpstream',
        label: '上游对账',
        children: [
          { key: 'customerdnlist', routeName: 'customerdnlist', label: '客户运单对账' },
          { key: 'customerpod', routeName: 'customerpod', label: '客户订单对账' }
        ]
      },
      {
        key: 'financeDownstream',
        label: '下游对账',
        children: [
          { key: 'supplierasnlist', routeName: 'supplierasnlist', label: '承运商对账' },
          { key: 'driverCheck', routeName: 'driverCheck', label: '司机对账' },
          { key: 'vehicleCheck', routeName: 'vehicleCheck', label: '车辆对账' }
        ]
      },
      { key: 'receiptbill', routeName: 'receiptbill', label: '收款单' },
      { key: 'paybill', routeName: 'paybill', label: '付款单' }
    ]
  },
  {
    key: 'capacity',
    icon: 'hub',
    title: '运力中心',
    items: [
      { key: 'driverCheck2', routeName: 'driverCheck', label: '司机档案' },
      { key: 'vehicleCheck2', routeName: 'vehicleCheck', label: '车辆档案' }
    ]
  },
  {
    key: 'company',
    icon: 'business',
    title: '公司管理',
    items: [
      { key: 'company', routeName: 'company', label: '公司资料' },
      { key: 'supplier', routeName: 'supplier', label: '供应商资料' },
      { key: 'customer', routeName: 'customer', label: '客户资料' }
    ]
  },
  {
    key: 'system',
    icon: 'assignment',
    title: '系统管理',
    items: [
      { key: 'stafflist', routeName: 'stafflist', label: '人员管理' },
      { key: 'uploadlist', routeName: 'uploadlist', label: '导入记录' }
    ]
  }
]

const WAREHOUSE_NAME_MAP = {
  'Center Warehouse': '中心仓',
  'CENTER WAREHOUSE': '中心仓',
  'center warehouse': '中心仓'
}

const TAB_TITLE_MAP = {
  web_index: '首页',
  createwaybill: '创建运单',
  dn: '运单列表',
  freshorder: '运单审核',
  neworder: '运单修改记录',
  pod: '运单回单',
  driverlist: '在线跟踪',
  dispatchlist: '在途费用',
  customerdnlist: '客户运单对账',
  customerpod: '客户订单对账',
  supplierasnlist: '承运商对账',
  driverCheck: '司机对账',
  vehicleCheck: '车辆对账',
  receiptbill: '收款单',
  paybill: '付款单',
  company: '公司资料',
  supplier: '供应商资料',
  customer: '客户资料',
  stafflist: '人员管理',
  uploadlist: '导入记录'
}

export default {
  name: 'MainLayout',
  data () {
    return {
      drawerleft: false,
      warehouse_name: '',
      warehouseOptions: [],
      authin: '0',
      login_name: '',
      login_id: 0,
      openid: '',
      login: false,
      register: false,
      loginMode: 'code',
      openTabs: [],
      activeTabKey: 'web_index',
      expandedSections: {
        transport: true,
        online: false,
        finance: false,
        financeUpstream: true,
        financeDownstream: false,
        capacity: false,
        company: false,
        system: false
      },
      phoneLoginForm: {
        phone: '',
        code: '',
        debugCode: ''
      },
      passwordLoginForm: {
        phone: '',
        password: ''
      },
      phoneRegisterForm: {
        name: '',
        phone: '',
        code: '',
        debugCode: '',
        password: '',
        password_confirm: ''
      },
      loginCodeCountdown: 0,
      registerCodeCountdown: 0,
      loginCodeTimer: null,
      registerCodeTimer: null
    }
  },
  computed: {
    navSections () {
      return NAV_SECTIONS
    },
    loginPhoneValue: {
      get () {
        return this.loginMode === 'password'
          ? this.passwordLoginForm.phone
          : this.phoneLoginForm.phone
      },
      set (value) {
        if (this.loginMode === 'password') {
          this.passwordLoginForm.phone = value
        } else {
          this.phoneLoginForm.phone = value
        }
      }
    }
  },
  methods: {
    displayWarehouseName (name) {
      const rawName = (name || '').trim()
      if (!rawName) {
        return ''
      }
      return WAREHOUSE_NAME_MAP[rawName] || rawName
    },
    isActiveRoute (routeName) {
      return this.$route.name === routeName
    },
    goRoute (routeName) {
      if (routeName && routeName !== this.$route.name) {
        this.$router.push({ name: routeName })
      }
      if (this.$q.screen.lt.md) {
        this.drawerleft = false
      }
    },
    setExpanded (key, value) {
      this.$set(this.expandedSections, key, value)
    },
    showNotify (message, color = 'negative', icon = 'close') {
      this.$q.notify({ message, color, icon })
    },
    validPhone (phone) {
      return /^1\d{10}$/.test((phone || '').trim())
    },
    routeToTab (route) {
      if (!route || !route.name) {
        return null
      }
      if (route.name === 'createwaybill' && route.query && route.query.mode === 'edit' && route.query.id) {
        return {
          key: `edit-${route.query.id}`,
          label: '修改运单',
          route: {
            name: 'createwaybill',
            query: { mode: 'edit', id: route.query.id }
          },
          closable: true
        }
      }
      return {
        key: route.name,
        label: TAB_TITLE_MAP[route.name] || '业务页面',
        route: { name: route.name, query: route.query || {} },
        closable: route.name !== 'web_index'
      }
    },
    ensureTabForRoute (route = this.$route) {
      const tab = this.routeToTab(route)
      if (!tab) {
        return
      }
      const exists = this.openTabs.find(item => item.key === tab.key)
      if (!exists) {
        this.openTabs.push(tab)
      } else {
        exists.route = tab.route
        exists.label = tab.label
      }
      this.activeTabKey = tab.key
    },
    navigateTab (tab) {
      if (!tab) {
        return
      }
      this.activeTabKey = tab.key
      this.$router.push(tab.route)
    },
    closeTab (tab) {
      const index = this.openTabs.findIndex(item => item.key === tab.key)
      if (index === -1 || !tab.closable) {
        return
      }
      const isCurrent = this.activeTabKey === tab.key
      this.openTabs.splice(index, 1)
      if (isCurrent) {
        const fallback = this.openTabs[index - 1] || this.openTabs[index] || this.openTabs[0]
        if (fallback) {
          this.navigateTab(fallback)
        } else {
          this.$router.push({ name: 'web_index' })
        }
      }
    },
    openLogin (mode = 'code') {
      this.loginMode = mode
      this.login = true
      this.register = false
    },
    openRegister () {
      this.register = true
      this.login = false
    },
    quickDemoAccess () {
      this.openLogin('code')
      this.showNotify('请先登录或注册后再使用完整业务功能', 'info', 'info')
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
        } else {
          this[countdownKey] -= 1
        }
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
            this.showNotify(`验证码已生成：${form.debugCode}`, 'positive', 'check')
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
      this.showNotify('登录成功', 'positive', 'check')
      this.staffType()
      this.$router.push({ name: 'web_index' })
    },
    submitLogin () {
      if (this.loginMode === 'password') {
        this.passwordLogin()
      } else {
        this.phoneLogin()
      }
    },
    phoneLogin () {
      const payload = {
        mode: 'code',
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
    passwordLogin () {
      const payload = {
        mode: 'password',
        phone: (this.passwordLoginForm.phone || '').trim(),
        password: this.passwordLoginForm.password || ''
      }
      if (!this.validPhone(payload.phone)) {
        this.showNotify('请输入正确的11位手机号')
        return
      }
      if (!payload.password) {
        this.showNotify('请输入登录密码')
        return
      }
      SessionStorage.set('axios_check', 'false')
      post('login/', payload)
        .then((res) => {
          if (res.code === '200') {
            this.applyPhoneAuth(res.data, 'password')
          } else {
            this.showNotify(res.msg || '登录失败')
          }
        })
        .catch((err) => {
          this.showNotify(err.detail || '登录失败')
        })
    },
    phoneRegister () {
      const payload = {
        name: (this.phoneRegisterForm.name || '').trim(),
        phone: (this.phoneRegisterForm.phone || '').trim(),
        code: (this.phoneRegisterForm.code || '').trim(),
        password: this.phoneRegisterForm.password || '',
        password_confirm: this.phoneRegisterForm.password_confirm || ''
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
            this.applyPhoneAuth(res.data, 'password')
          } else {
            this.showNotify(res.msg || '注册失败')
          }
        })
        .catch((err) => {
          this.showNotify(err.detail || '注册失败')
        })
    },
    Logout () {
      this.authin = '0'
      this.login_name = ''
      this.login_id = 0
      this.openid = ''
      LocalStorage.remove('auth')
      LocalStorage.set('login_name', '')
      LocalStorage.set('login_id', '')
      LocalStorage.set('openid', '')
      SessionStorage.remove('axios_check')
      this.showNotify('已退出登录', 'info', 'check')
      this.$router.push({ name: 'web_index' })
    },
    staffType () {
      getauth(`staff/?staff_name=${this.login_name}`).then((res) => {
        if (res.results && res.results.length > 0) {
          LocalStorage.set('staff_type', res.results[0].staff_type)
        }
      }).catch(() => {})
    },
    warehouseOptionsGet () {
      get('warehouse/multiple/?max_page=30')
        .then((res) => {
          this.warehouseOptions = res.results || []
          if (this.warehouseOptions.length) {
            if (LocalStorage.has('openid')) {
              const found = this.warehouseOptions.find(item => item.openid === LocalStorage.getItem('openid'))
              this.warehouse_name = found ? found.warehouse_name : this.warehouseOptions[0].warehouse_name
            } else {
              this.warehouse_name = this.warehouseOptions[0].warehouse_name
            }
          }
        })
        .catch(() => {})
    }
  },
  created () {
    this.openTabs = [
      {
        key: 'web_index',
        label: '首页',
        route: { name: 'web_index' },
        closable: false
      }
    ]
    this.openid = LocalStorage.getItem('openid') || ''
    this.login_name = LocalStorage.getItem('login_name') || ''
    this.login_id = LocalStorage.getItem('login_id') || 0
    if (LocalStorage.has('auth')) {
      this.authin = '1'
      this.staffType()
    }
    this.ensureTabForRoute()
  },
  mounted () {
    this.warehouseOptionsGet()
    Bus.$on('needLogin', () => {
      this.openLogin('code')
    })
    Bus.$on('openLoginDialog', () => {
      this.openLogin('code')
    })
    Bus.$on('openRegisterDialog', () => {
      this.openRegister()
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
    '$route.fullPath' () {
      this.ensureTabForRoute()
    }
  }
}
</script>

<style scoped>
.platform-layout {
  background: #f3f4f7;
}

.platform-header {
  background: #2d1979;
}

.platform-toolbar {
  min-height: 48px;
  padding: 0 10px;
  gap: 10px;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 190px;
  cursor: pointer;
}

.brand-logo {
  width: 110px;
  height: 30px;
  object-fit: contain;
}

.brand-title {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.1;
}

.brand-subtitle {
  font-size: 11px;
  opacity: 0.8;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-search {
  width: 172px;
}

.create-btn {
  min-width: 92px;
}

.platform-drawer {
  background: #fbfbfd;
}

.drawer-user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 10px 10px;
  border-bottom: 1px solid #eceef4;
}

.user-avatar-wrap {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  background: #eef1f7;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.drawer-user-name {
  font-size: 14px;
  font-weight: 700;
  color: #2d3c55;
}

.drawer-user-role {
  margin-top: 3px;
  font-size: 12px;
  color: #7f8ca3;
}

.drawer-search-wrap {
  padding: 10px;
}

.drawer-search :deep(.q-field__control) {
  min-height: 34px;
}

.nav-list {
  padding: 4px 8px 14px;
}

.nav-section-header {
  min-height: 40px;
  border-radius: 6px;
  color: #5c4cf4;
  font-weight: 700;
}

.nav-children {
  padding-left: 6px;
}

.nav-item-child,
.nav-item-grandchild {
  min-height: 34px;
  padding-left: 18px;
  color: #36465f;
  border-radius: 6px;
}

.nav-subgroup-header {
  min-height: 34px;
  padding-left: 10px;
  color: #4d5d76;
}

.nav-grand-children {
  padding-left: 10px;
}

.nav-item-active {
  background: #efedff;
  color: #5c4cf4;
  font-weight: 700;
}

.platform-page-container {
  padding: 0;
}

.page-tabs {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding: 6px 10px 0;
  background: #f0f2f6;
}

.page-tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #ced7e5;
  border-bottom: 0;
  border-radius: 8px 8px 0 0;
  background: #fff;
  color: #465a77;
  padding: 8px 12px;
  white-space: nowrap;
  cursor: pointer;
}

.page-tab.active {
  color: #2d1979;
  font-weight: 700;
}

.page-tab-close {
  font-size: 16px;
  line-height: 1;
}

.page-shell {
  padding: 0 10px 10px;
}

.auth-dialog-card {
  width: 460px;
  max-width: calc(100vw - 24px);
}

.auth-dialog-bar {
  background: #2d1979;
  min-height: 44px;
}

.auth-dialog-title {
  font-size: 15px;
  font-weight: 700;
}

.auth-dialog-section {
  display: grid;
  gap: 12px;
  padding: 18px;
}

.auth-mode-switch {
  display: flex;
  gap: 8px;
}

.auth-code-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}

.auth-code-btn {
  min-width: 120px;
}

.auth-debug-tip {
  font-size: 12px;
  color: #5d7193;
}

.auth-dialog-actions {
  padding: 0 18px 18px;
}

@media (max-width: 1100px) {
  .header-actions {
    display: none;
  }
}
</style>
