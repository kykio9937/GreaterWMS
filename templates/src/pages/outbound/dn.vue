<template>
  <div class="dn-page">
    <div class="status-tabs">
      <button
        v-for="tab in statusTabs"
        :key="tab.key"
        type="button"
        :class="['status-tab', { active: activeStatusTab === tab.key }]"
        @click="setStatusTab(tab.key)"
      >
        <span>{{ tab.label }}</span>
        <em>{{ getStatusTabCount(tab.key) }}</em>
      </button>
    </div>
    <transition appear enter-active-class="animated fadeIn">
      <div class="list-shell shadow-24 platform-table">
        <div class="filter-panel compact-panel">
          <div class="filter-grid compact-grid-bar">
            <div class="toolbar-field">
              <div class="toolbar-label">运单号</div>
              <q-input v-model="filterForm.keyword" dense outlined placeholder="支持批量搜索、多个数据用逗号分隔" class="filter-compact filter-keyword" />
            </div>
            <div class="toolbar-field">
              <div class="toolbar-label">运单状态</div>
              <q-select
                v-model="filterForm.status"
                dense
                outlined
                emit-value
                map-options
                :options="statusFilterOptions"
                class="filter-compact"
              />
            </div>
            <div class="toolbar-field">
              <div class="toolbar-label">客户名称</div>
              <q-input v-model="filterForm.customer" dense outlined placeholder="请输入客户名称" class="filter-compact" />
            </div>
            <div class="toolbar-field">
              <div class="toolbar-label">创建时间</div>
              <q-input v-model="filterForm.dateRange" dense outlined placeholder="开始日期 - 结束日期" class="filter-compact" />
            </div>
          </div>
          <div class="filter-actions table-search-actions compact">
            <q-btn unelevated color="primary" label="查询" icon="search" @click="runSearch()" />
            <q-btn flat color="grey-8" label="重置" @click="resetFilters()" />
            <q-btn flat color="grey-8" label="刷新" icon="refresh" @click="reFresh()" />
          </div>
        </div>

        <div class="toolbar-strip">
          <div class="toolbar-group">
            <q-btn outline dense color="deep-purple-6" label="复制" @click="showFeatureTip('复制')" />
            <q-btn outline dense color="deep-purple-6" label="装车" @click="showFeatureTip('装车')" />
            <q-btn outline dense color="deep-purple-6" label="发车" @click="showFeatureTip('发车')" />
            <q-btn outline dense color="deep-purple-6" label="到达" @click="showFeatureTip('到达')" />
            <q-btn outline dense color="deep-purple-6" label="完成" @click="showFeatureTip('完成')" />
            <q-btn outline dense color="deep-purple-6" label="卸车" @click="showFeatureTip('卸车')" />
            <q-btn outline dense color="deep-purple-6" label="指派" @click="showFeatureTip('指派')" />
            <q-btn outline dense color="deep-purple-6" label="上传电子回单" @click="showFeatureTip('上传电子回单')" />
            <q-btn outline dense color="deep-purple-6" label="重新计算价格" @click="showFeatureTip('重新计算价格')" />
            <q-btn outline dense color="deep-purple-6" label="修改里程" @click="showFeatureTip('修改里程')" />
            <q-btn outline dense color="deep-purple-6" label="重算设备里程" @click="showFeatureTip('重算设备里程')" />
            <q-btn outline dense color="deep-purple-6" label="更多" icon-right="expand_more" @click="showFeatureTip('更多操作')" />
          </div>
          <div class="toolbar-group compact">
            <q-btn outline dense color="grey-8" label="导入" icon="login" @click="showFeatureTip('导入')" />
            <q-btn outline dense color="grey-8" label="导出" icon="edit_square" @click="showFeatureTip('导出')" />
            <q-btn outline dense color="grey-8" label="打印" icon="print" @click="showFeatureTip('打印')" />
          </div>
        </div>

        <div class="manual-table-wrap">
          <table class="manual-table">
            <thead>
              <tr class="dense-header-row">
                <th class="cell-index">筛选</th>
                <th class="cell-select">
                  <q-checkbox v-model="selectAllRows" dense size="xs" />
                </th>
                <th class="cell-action">操作</th>
                <th>到车运费</th>
                <th>审核状态</th>
                <th>业务收入合计</th>
                <th>车线名称</th>
                <th>所属组织</th>
                <th>开单时间</th>
                <th>合作关系</th>
                <th>经办人部门</th>
                <th>派单员</th>
                <th>客户名称</th>
                <th>运单号</th>
                <th>货物名称</th>
                <th>车牌号</th>
                <th>运力奖励</th>
                <th>进仓费</th>
                <th>卸车费</th>
                <th>车辆属性</th>
                <th>运单状态</th>
              </tr>
            </thead>
            <tbody v-if="displayTableList.length">
              <tr v-for="row in displayTableList" :key="row.id" class="dense-body-row">
                <td class="cell-index">{{ row.row_index }}</td>
                <td class="cell-select"><q-checkbox v-model="row.selected" dense size="xs" /></td>
                <td class="cell-action">
                  <div class="action-link-group">
                    <span class="table-link" @click="editData(row)">[修改运单]</span>
                    <span class="table-link danger" @click="deleteData(row)">[删除运单]</span>
                  </div>
                </td>
                <td><span class="amount-dark">{{ row.freight_amount }}</span></td>
                <td>
                  <span :class="['mark-text', 'status-dot', row.audit_status === '待审核' ? 'mark-red' : 'mark-gray']">{{ row.audit_status }}</span>
                </td>
                <td><span class="amount-dark">{{ row.business_income }}</span></td>
                <td>{{ row.line_name }}</td>
                <td>{{ row.organization }}</td>
                <td>{{ row.create_time }}</td>
                <td>{{ row.cooperation }}</td>
                <td>{{ row.department }}</td>
                <td>{{ row.dispatcher }}</td>
                <td>{{ row.customer }}</td>
                <td>
                  <div class="waybill-code-cell compact">
                    <div class="waybill-code">{{ row.dn_code }}</div>
                    <div class="waybill-meta">{{ row.customer_reference }}</div>
                  </div>
                </td>
                <td>{{ row.goods_name }}</td>
                <td>{{ row.plate_number }}</td>
                <td><span class="amount-blue">{{ row.reward_fee }}</span></td>
                <td><span class="amount-blue">{{ row.warehouse_fee }}</span></td>
                <td><span class="amount-blue">{{ row.unload_fee }}</span></td>
                <td><span class="soft-tag">{{ row.vehicle_attr }}</span></td>
                <td>
                  <q-badge rounded :class="statusBadgeClass(row.dn_status)">
                    {{ row.dn_status }}
                  </q-badge>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!displayTableList.length" class="manual-empty">
            暂无数据
          </div>
        </div>
      </div>
    </transition>
      <div v-if="displayTableList.length" class="list-summary-bar">
        <div class="summary-label">合计</div>
        <div class="summary-item">当前页 {{ displayTableList.length }} 批次</div>
        <div class="summary-item">到车运费 {{ visibleFreightTotal }}</div>
        <div class="summary-item">业务收入 {{ visibleBusinessIncomeTotal }}</div>
        <div class="summary-item push-right">{{ displayTableList.length }} 批次</div>
      </div>
      <div v-show="max !== 0" class="pagination-wrap">
        <div class="page-total">共 {{ total }} 条</div>
        <q-pagination
          v-model="current"
          color="black"
          :max="max"
          :max-pages="6"
          boundary-links
          @click="getList()"
        />
        <div class="page-jump">
          <input
            v-model="paginationIpt"
            @blur="changePageEnter"
            @keyup.enter="changePageEnter"
            style="width: 60px; text-align: center"
          />
        </div>
      </div>
      <div v-show="max === 0" class="pagination-wrap empty-state">
        <q-btn flat push color="dark" :label="$t('no_data')"></q-btn>
      </div>
    <q-dialog v-model="newForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ newFormData.dn_code }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            filled
            use-input
            fill-input
            hide-selected
            input-debounce="0"
            dense
            outlined
            square
            v-model="newFormData.customer"
            :options="customer_list"
            @filter="filterFnS"
            @input-value="setModel"
            :label="$t('baseinfo.view_customer.customer_name')"
            style="margin-bottom: 5px"
            :rules="[val => (val && val.length > 0) || error1]"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
                <template v-slot:Sno-option>
                  <q-item>
                    <q-item-section class="text-grey">
                  {{ $t('no_results') }}
                    </q-item-section>
                  </q-item>
                </template>
          </q-select>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData1.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData1.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(1)"
                @input-value="setOptions"
                @filter="filterFn"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">{{ $t('no_results') }}</q-item-section></q-item>
                </template>
                <template v-if="goodsData1.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData1.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData2.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData2.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(2)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData2.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData2.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData3.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData3.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(3)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData3.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData3.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData4.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData4.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(4)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData4.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData4.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData5.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData5.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(5)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData5.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData5.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData6.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData6.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(6)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData6.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData6.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData7.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData7.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(7)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData7.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData7.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData8.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData8.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(8)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData8.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData8.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData9.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData9.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(9)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData9.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData9.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData10.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData10.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(10)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData10.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData10.code = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="isEdit ? editDataCancel() : newDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="isEdit ? editDataSubmit() : newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('delete') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="deleteDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="deleteDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="neworderForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('confirmorder') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="neworderDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="neworderDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="orderreleaseForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('releaseorder') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="orderreleaseDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="orderreleaseDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="viewForm">
      <q-card id="printMe">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ viewdn }}</div>
          <q-space />
          {{ $t('outbound.dn') }}
        </q-bar>
        <q-card-section>
          <div class="row">
            <div class="col-8">
              <div class="text-h6">Sender: {{ warehouse_detail.warehouse_name }}</div>
              <div class="text-subtitle2">Address: {{ warehouse_detail.warehouse_city }}{{ warehouse_detail.warehouse_address }}</div>
              <div class="text-subtitle2">Tel: {{ warehouse_detail.warehouse_contact }}</div>
              <div class="text-h6">Receiver: {{ customer_detail.customer_name }}</div>
              <div class="text-subtitle2">Address: {{ customer_detail.customer_city }}{{ customer_detail.customer_address }}</div>
              <div class="text-subtitle2">Tel: {{ customer_detail.customer_contact }}</div>
            </div>
            <div class="col-4"><img :src="bar_code" style="width: 70%; margin-left: 15%" /></div>
          </div>
        </q-card-section>
        <q-markup-table>
          <thead>
            <tr>
              <th class="text-left">{{ $t('goods.view_goodslist.goods_code') }}</th>
              <th class="text-right">{{ $t('outbound.view_dn.total_weight') }}</th>
              <th class="text-right">{{ $t('outbound.view_dn.total_volume') }}</th>
              <th class="text-right">{{ $t('outbound.view_dn.intransit_qty') }}</th>
              <th class="text-right">Comments</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(view, index) in viewprint_table" :key="index">
              <td class="text-left">{{ view.goods_code }}</td>
              <td class="text-right">{{ view.goods_weight }}</td>
              <td class="text-right">{{ view.goods_volume }}</td>
              <td class="text-right">{{ view.picked_qty }}</td>
              <td class="text-right"></td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card>
      <div style="float: right; padding: 15px 15px 15px 0"><q-btn color="primary" icon="print" v-print="printObj">print</q-btn></div>
    </q-dialog>
    <q-dialog v-model="viewPLForm">
      <q-card id="printPL">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('print') }}</div>
          <q-space />
        </q-bar>
        <div class="col-4" style="margin-top: 5%;"><img :src="bar_code" style="width: 21%;margin-left: 70%" /></div>
        <q-markup-table>
          <thead>
            <tr>
              <th class="text-left">{{ $t('outbound.view_dn.dn_code') }}</th>
              <th class="text-right">{{ $t('warehouse.view_binset.bin_name') }}</th>
              <th class="text-right">{{ $t('goods.view_goodslist.goods_code') }}</th>
              <th class="text-right">{{ $t('outbound.pickstock') }}</th>
              <th class="text-right">{{ $t('outbound.pickedstock') }}</th>
              <th class="text-right">Comments</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(view, index) in pickinglist_print_table" :key="index">
              <td class="text-left">{{ view.dn_code }}</td>
              <td class="text-right">{{ view.bin_name }}</td>
              <td class="text-right">{{ view.goods_code }}</td>
              <td class="text-right">{{ view.pick_qty }}</td>
              <td class="text-right" v-show="picklist_check === 0"></td>
              <td class="text-right" v-show="picklist_check > 0">{{ view.picked_qty }}</td>
              <td class="text-right"></td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card>
      <div style="float: right; padding: 15px 15px 15px 0"><q-btn color="primary" icon="print" v-print="printPL">print</q-btn></div>
    </q-dialog>
    <q-dialog v-model="pickedForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ pickFormData.dn_code }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-input
            dense
            outlined
            square
            debounce="500"
            disable
            readonly
            v-model="pickFormData.customer"
            :label="$t('baseinfo.view_customer.customer_name')"
            style="margin-bottom: 5px"
          />
          <div v-for="(item, index) in pickFormData.goodsData" :key="index">
            <q-input dense outlined square bottom-slots type="number" v-model="item.pick_qty" :label="item.goods_code">
              <template v-slot:append>
                {{ item.bin_name }}
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="pickedDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="pickedDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dispatchForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ dispatchFormData.dn_code }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            dense
            outlined
            square
            use-input
            hide-selected
            fill-input
            v-model="dispatchFormData.driver"
            :label="$t('driver.view_driver.driver_name')"
            :options="driver_options"
            @filter="filterFnDispatch"
            autofocus
            @keyup.enter="dispatchDataSubmit()"
          >
            <template v-slot:no-option>
              <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
            </template>
            <template v-if="dispatchFormData.driver" v-slot:append>
              <q-icon name="cancel" @click.stop="dispatchFormData.driver = ''" class="cursor-pointer" />
            </template>
          </q-select>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="dispatchDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="dispatchDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="podForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('outbound.dn') }}: {{ podFormData.dn_code }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          {{ $t('baseinfo.customer') }}: {{ podFormData.customer }}
          <div v-for="(item, index) in podFormData.goodsData" :key="index">
            <q-input
              dense
              outlined
              square
              debounce="500"
              v-model.number="item.intransit_qty"
              type="number"
              :label="$t('outbound.view_dn.delivery_actual_qty')"
              style="margin-bottom: 5px"
              :error-message="error2"
              :error="isError1"
              :rules="[validate1]"
            >
              <template v-slot:after>
                <q-input
                  dense
                  outlined
                  square
                  debounce="500"
                  v-model.number="item.delivery_damage_qty"
                  type="number"
                  :label="$t('outbound.view_dn.delivery_damage_qty')"
                  style="margin-top: 11%"
                  :error-message="error2"
                  :error="isError2"
                  :rules="[validate2(item.delivery_damage_qty, item.intransit_qty)]"
                ></q-input>
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="PODDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="PODDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { getauth, postauth, putauth, deleteauth, ViewPrintAuth } from 'boot/axios_request'
import { LocalStorage } from 'quasar'

export default {
  name: 'Pagednlist',
  data () {
    return {
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'dn/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      viewprint_table: [],
      bar_code: '',
      pickinglist_print_table: [],
      pickinglist_check: 0,
      warehouse_detail: {},
      customer_list: [],
      customer_list1: [],
      driver_list: [],
      customer_detail: {},
      columns: [
        { name: 'row_index', label: '序号', align: 'center', style: 'min-width: 56px' },
        { name: 'row_select', label: '', align: 'center', style: 'min-width: 44px' },
        { name: 'action', label: '操作', align: 'left', style: 'min-width: 138px' },
        { name: 'freight_amount', label: '到车运费', field: 'freight_amount', align: 'right', style: 'min-width: 84px' },
        { name: 'audit_status', label: '审核状态', align: 'center', field: 'audit_status', style: 'min-width: 88px' },
        { name: 'business_income', label: '业务收入合计', field: 'business_income', align: 'right', style: 'min-width: 108px' },
        { name: 'line_name', label: '车线名称', field: 'line_name', align: 'left', style: 'min-width: 138px' },
        { name: 'organization', label: '所属组织', field: 'organization', align: 'left', style: 'min-width: 128px' },
        { name: 'create_time', label: '开单时间', field: 'create_time', align: 'center', style: 'min-width: 138px' },
        { name: 'cooperation', label: '合作关系', field: 'cooperation', align: 'left', style: 'min-width: 128px' },
        { name: 'department', label: '经办人部门', field: 'department', align: 'left', style: 'min-width: 108px' },
        { name: 'dispatcher', label: '派单员', field: 'dispatcher', align: 'center', style: 'min-width: 82px' },
        { name: 'customer', label: '客户名称', field: 'customer', align: 'left', style: 'min-width: 98px' },
        { name: 'dn_code', required: true, label: '运单号', align: 'left', field: 'dn_code', style: 'min-width: 178px' },
        { name: 'goods_name', label: '货物名称', field: 'goods_name', align: 'left', style: 'min-width: 98px' },
        { name: 'plate_number', label: '车牌号', field: 'plate_number', align: 'center', style: 'min-width: 88px' },
        { name: 'reward_fee', label: '运力奖励', field: 'reward_fee', align: 'right', style: 'min-width: 86px' },
        { name: 'warehouse_fee', label: '进仓费', field: 'warehouse_fee', align: 'right', style: 'min-width: 82px' },
        { name: 'fee_status', label: '费用对账状态', field: 'fee_status', align: 'center', style: 'min-width: 112px' },
        { name: 'audit_result', label: '审核意见', field: 'audit_result', align: 'left', style: 'min-width: 92px' },
        { name: 'audit_remark', label: '审核备注', field: 'audit_remark', align: 'left', style: 'min-width: 118px' },
        { name: 'vehicle_attr', label: '车辆属性', field: 'vehicle_attr', align: 'left', style: 'min-width: 98px' },
        { name: 'unload_fee', label: '卸车费', field: 'unload_fee', align: 'right', style: 'min-width: 82px' },
        { name: 'dn_status', label: '运单状态', field: 'dn_status', align: 'center', style: 'min-width: 92px' }
      ],
      filter: '',
      activeStatusTab: 'all',
      statusTabs: [
        { key: 'all', label: '全部' },
        { key: 'plan', label: '计划运单' },
        { key: 'accept', label: '待受理' },
        { key: 'picking', label: '已受理' },
        { key: 'transit', label: '运输中' },
        { key: 'done', label: '已完成' },
        { key: 'void', label: '作废记录' }
      ],
      filterForm: {
        keyword: '',
        customer: '',
        status: 'all',
        dateRange: ''
      },
      statusFilterOptions: [
        { label: '全部', value: 'all' },
        { label: '待审核', value: '待审核' },
        { label: '待受理', value: '待受理' },
        { label: '已受理', value: '已受理' },
        { label: '运输中', value: '运输中' },
        { label: '已完成', value: '已完成' },
        { label: '作废', value: '作废' }
      ],
      pagination: {
        page: 1,
        rowsPerPage: '30'
      },
      newForm: false,
      options1: [],
      isEdit: false,
      listNumber: '',
      options: LocalStorage.getItem('goods_code_list'),
      driver_options: LocalStorage.getItem('driver_name_list'),
      newdn: { creater: '' },
      newFormData: {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      pickFormData: {
        dn_code: '',
        customer: '',
        goodsData: [],
        creater: ''
      },
      goodsData1: { bin: '', code: '', qty: '' },
      goodsData2: { bin: '', code: '', qty: '' },
      goodsData3: { bin: '', code: '', qty: '' },
      goodsData4: { bin: '', code: '', qty: '' },
      goodsData5: { bin: '', code: '', qty: '' },
      goodsData6: { bin: '', code: '', qty: '' },
      goodsData7: { bin: '', code: '', qty: '' },
      goodsData8: { bin: '', code: '', qty: '' },
      goodsData9: { bin: '', code: '', qty: '' },
      goodsData10: { bin: '', code: '', qty: '' },
      editid: 0,
      editFormData: {},
      pickedForm: false,
      pickedid: 0,
      deleteForm: false,
      deleteid: 0,
      neworderForm: false,
      neworderid: 0,
      orderreleaseForm: false,
      orderreleaseid: 0,
      viewForm: false,
      viewPLForm: false,
      viewdn: '',
      viewid: 0,
      dispatchid: 0,
      dispatchForm: false,
      dispatchFormData: {
        dn_code: '',
        driver: ''
      },
      podid: 0,
      podForm: false,
      podFormData: {
        dn_code: '',
        customer: '',
        goodsData: []
      },
      printObj: {
        id: 'printMe',
        popTitle: this.$t('outbound.dn')
      },
      printPL: {
        id: 'printPL',
        popTitle: this.$t('outbound.pickinglist')
      },
      error1: this.$t('baseinfo.view_customer.error1'),
      error2: this.$t('notice.valerror'),
      isError1: false,
      isError2: false,
      current: 1,
      max: 0,
      total: 0,
      paginationIpt: 1,
      selectAllRows: false
    }
  },
  computed: {
    enhancedTableList () {
      return this.table_list.map((item, index) => this.buildDisplayRow(item, index))
    },
    displayTableList () {
      return this.enhancedTableList.filter(item => {
        const matchTab = this.isStatusInTab(item, this.activeStatusTab)
        const matchStatus = this.filterForm.status === 'all' || item.audit_status === this.filterForm.status || item.dn_status === this.filterForm.status
        const matchCustomer = !this.filterForm.customer || String(item.customer || '').includes(this.filterForm.customer)
        const matchDate = !this.filterForm.dateRange || String(item.create_time || '').includes(this.filterForm.dateRange)
        return matchTab && matchStatus && matchCustomer && matchDate
      })
    },
    freshOrderCount () {
      return this.enhancedTableList.filter(item => this.isStatusInTab(item, 'plan')).length
    },
    pickPendingCount () {
      return this.enhancedTableList.filter(item => this.isStatusInTab(item, 'picking')).length
    },
    receiptPendingCount () {
      return this.enhancedTableList.filter(item => this.isStatusInTab(item, 'transit')).length
    },
    inTransitCount () {
      return this.receiptPendingCount
    },
    completedCount () {
      return this.enhancedTableList.filter(item => this.isStatusInTab(item, 'done')).length
    },
    visibleFreightTotal () {
      return this.displayTableList.reduce((sum, item) => sum + Number(item.freight_amount || 0), 0).toFixed(2)
    },
    visibleBusinessIncomeTotal () {
      return this.displayTableList.reduce((sum, item) => sum + Number(item.business_income || 0), 0).toFixed(2)
    },
    totalWeightDisplay () {
      const totalWeight = this.table_list.reduce((sum, item) => sum + Number(item.total_weight || 0), 0)
      return totalWeight.toFixed(2)
    }
  },
  methods: {
    normalizeStatus (status) {
      if (status === 1 || status === '1') {
        return this.$t('outbound.freshorder')
      } else if (status === 2 || status === '2') {
        return this.$t('outbound.neworder')
      } else if (status === 3 || status === '3') {
        return this.$t('outbound.pickstock')
      } else if (status === 4 || status === '4') {
        return this.$t('outbound.pickedstock')
      } else if (status === 5 || status === '5') {
        return this.$t('outbound.shippedstock')
      } else if (status === 6 || status === '6') {
        return this.$t('outbound.received')
      }
      return status || 'N/A'
    },
    buildDisplayRow (row, index) {
      const feeMeta = row.transportation_fee || {}
      const weight = Number(row.total_weight || 0)
      const volume = Number(row.total_volume || 0)
      const income = row.business_income || feeMeta.business_income || ((weight * 0.46) + (volume * 58)).toFixed(2)
      const reward = row.reward_fee || feeMeta.reward_fee || (weight > 0 ? (weight * 0.03).toFixed(2) : '0.00')
      const status = this.normalizeStatus(row.dn_status)
      const auditStatus = row.audit_status || ([this.$t('outbound.freshorder'), this.$t('outbound.neworder')].includes(status) ? '待审核' : '已审核')
      return {
        ...row,
        dn_status: status,
        audit_status: auditStatus,
        goods_name: row.goods_name || feeMeta.goods_name || row.goods_code || '标准普货',
        plate_number: row.plate_number || feeMeta.plate_number || row.vehicle_no || '待分配',
        line_name: row.line_name || feeMeta.line_name || `${row.customer || '默认客户'}干线`,
        organization: row.organization || feeMeta.organization || '西安莲湖白桦',
        cooperation: row.cooperation || '68卡运区块链',
        department: row.department || feeMeta.department || '莲湖运营部',
        freight_amount: row.freight_amount || feeMeta.carrier_cost || income,
        business_income: income,
        fee_status: row.fee_status || '正常',
        audit_result: row.audit_result || '正常',
        audit_remark: row.audit_remark || feeMeta.remark || '系统默认',
        vehicle_attr: row.vehicle_attr || feeMeta.vehicle_type || '高栏车',
        reward_fee: reward,
        warehouse_fee: row.warehouse_fee || feeMeta.storage_fee || '0.00',
        unload_fee: row.unload_fee || feeMeta.extra_fee || '0.00',
        create_time: row.create_time || row.create_dt || '--',
        dispatcher: row.dispatcher || feeMeta.dispatcher || row.creater || '--',
        customer_reference: row.customer_reference || `KH${String(index + 1).padStart(4, '0')}`,
        row_index: row.row_index || index + 1,
        selected: Boolean(row.selected)
      }
    },
    isStatusInTab (item, tabKey) {
      const status = item.dn_status
      if (tabKey === 'all') {
        return true
      }
      if (tabKey === 'plan') {
        return [this.$t('outbound.freshorder'), this.$t('outbound.neworder')].includes(status)
      }
      if (tabKey === 'accept') {
        return status === this.$t('outbound.neworder') || status === '待受理'
      }
      if (tabKey === 'picking') {
        return [this.$t('outbound.pickstock'), this.$t('outbound.pickedstock'), '已受理'].includes(status)
      }
      if (tabKey === 'transit') {
        return status === this.$t('outbound.shippedstock') || status === '运输中'
      }
      if (tabKey === 'done') {
        return status === this.$t('outbound.received') || status === '已完成'
      }
      if (tabKey === 'void') {
        return status === '作废'
      }
      return true
    },
    getStatusTabCount (tabKey) {
      return this.enhancedTableList.filter(item => this.isStatusInTab(item, tabKey)).length
    },
    setStatusTab (tabKey) {
      this.activeStatusTab = tabKey
    },
    focusLatestWaybill () {
      this.current = 1
      this.paginationIpt = 1
      this.filter = ''
      this.filterForm = {
        keyword: '',
        customer: '',
        status: 'all',
        dateRange: ''
      }
      this.activeStatusTab = 'all'
    },
    runSearch () {
      this.filter = this.filterForm.keyword
      if (this.filterForm.keyword) {
        this.getSearchList()
      } else {
        this.getList()
      }
    },
    resetFilters () {
      this.filter = ''
      this.filterForm = {
        keyword: '',
        customer: '',
        status: 'all',
        dateRange: ''
      }
      this.activeStatusTab = 'all'
      this.getList()
    },
    goCreateWaybill () {
      this.$router.push('/outbound/createwaybill')
    },
    showFeatureTip (label) {
      this.$q.notify({
        message: `${label} 功能已预留，可继续按国内物流平台流程扩展。`,
        icon: 'check_circle',
        color: 'primary'
      })
    },
    statusBadgeClass (status) {
      if ([this.$t('outbound.freshorder'), this.$t('outbound.neworder'), '待受理'].includes(status)) {
        return 'status-badge status-fresh'
      }
      if ([this.$t('outbound.pickstock'), this.$t('outbound.pickedstock'), '已受理'].includes(status)) {
        return 'status-badge status-picking'
      }
      if (status === this.$t('outbound.shippedstock') || status === '运输中') {
        return 'status-badge status-shipped'
      }
      if (status === this.$t('outbound.received') || status === '已完成') {
        return 'status-badge status-finished'
      }
      if (status === '作废') {
        return 'status-badge status-void'
      }
      return 'status-badge status-default'
    },
    validate1 (val) {
      const reg = /^[1-9]\d*$/g
      const check = reg.test(val)
      if (check) {
        this.isError1 = false
      } else {
        this.isError1 = true
      }
    },
    validate2 (val1, val2) {
      const reg = /^[0-9]\d*$/g
      const check = reg.test(val1)
      if (check && val1 <= val2) {
        this.isError2 = false
      } else {
        this.isError2 = true
      }
    },
    getList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + 'list/' + '?page=' + '' + _this.current, {})
          .then(res => {
            _this.table_list = []
            _this.total = res.count
            if (res.count === 0) {
              _this.max = 0
            } else {
              if (Math.ceil(res.count / 30) === 1) {
                _this.max = 0
              } else {
                _this.max = Math.ceil(res.count / 30)
              }
            }
            res.results.forEach(item => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            res.results.forEach(item => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t()
              }
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    changePageEnter (e) {
      if (Number(this.paginationIpt) < 1) {
        this.current = 1
        this.paginationIpt = 1
      } else if (Number(this.paginationIpt) > this.max) {
        this.current = this.max
        this.paginationIpt = this.max
      } else {
        this.current = Number(this.paginationIpt)
      }
      this.getList()
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        _this.current = 1
        _this.paginationIpt = 1
        getauth(_this.pathname + 'list/?dn_code__icontains=' + _this.filter + '&page=' + '' + _this.current, {})
          .then(res => {
            _this.table_list = []
            _this.total = res.count
            if (res.count === 0) {
              _this.max = 0
            } else {
              if (Math.ceil(res.count / 30) === 1) {
                _this.max = 0
              } else {
                _this.max = Math.ceil(res.count / 30)
              }
            }
            res.results.forEach(item => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_previous, {})
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_next, {})
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    reFresh () {
      var _this = this
      _this.table_list = []
      _this.getList()
    },
    newFormOpen () {
      var _this = this
      _this.isEdit = false
      _this.goodsDataClear()
      _this.newForm = true
      _this.newdn.creater = _this.login_name
      postauth(_this.pathname + 'list/', _this.newdn)
        .then(res => {
          if (!res.detail) {
            _this.newFormData.dn_code = res.dn_code
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    newDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.customer !== '') {
        _this.newFormData.goods_code = []
        _this.newFormData.goods_qty = []
        let goodsDataCheck = 0
        for (let i = 0; i < 10; i++) {
          const goodsData = `goodsData${i + 1}`
          if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
            if (_this[goodsData].qty < 1) {
              cancelRequest = true
              _this.$q.notify({
                message: 'Total Quantity Must Be > 0',
                icon: 'close',
                color: 'negative'
              })
            } else {
              _this.newFormData.goods_code.push(_this[goodsData].code)
              _this.newFormData.goods_qty.push(_this[goodsData].qty)
            }
            goodsDataCheck += 1
          }
        }
        if (goodsDataCheck === 0) {
          cancelRequest = true
          _this.$q.notify({
            message: 'Please Enter The Goods & Qty',
            icon: 'close',
            color: 'negative'
          })
        }
      } else {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Customer',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        postauth(_this.pathname + 'detail/', _this.newFormData)
          .then(res => {
            _this.table_list = []
            _this.focusLatestWaybill()
            _this.getList()
            _this.newDataCancel()
            if (res.detail === 'success') {
              _this.$q.notify({
                message: 'Success Create',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    newDataCancel () {
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    goodsDataClear () {
      var _this = this
      for (let i = 1; i <= 10; i++) {
        _this[`goodsData${i}`] = { code: '', qty: '' }
      }
    },
    editData (e) {
      var _this = this
      _this.isEdit = true
      _this.goodsDataClear()
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.newFormData.dn_code = e.dn_code
        _this.newFormData.customer = e.customer
        getauth(_this.pathname + 'detail/?dn_code=' + e.dn_code).then(res => {
          _this.newForm = true
          _this.editid = e.id
          res.results.forEach((detail, index) => {
            _this[`goodsData${index + 1}`] = { code: detail.goods_code, qty: detail.goods_qty }
          })
        })
      }
    },
    editDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.customer !== '') {
        _this.newFormData.goods_code = []
        _this.newFormData.goods_qty = []
        let goodsDataCheck = 0
        for (let i = 0; i < 10; i++) {
          const goodsData = `goodsData${i + 1}`
          if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
            if (_this[goodsData].qty < 1) {
              cancelRequest = true
              _this.$q.notify({
                message: 'Total Quantity Must Be > 0',
                icon: 'close',
                color: 'negative'
              })
            } else {
              _this.newFormData.goods_code.push(_this[goodsData].code)
              _this.newFormData.goods_qty.push(_this[goodsData].qty)
            }
            goodsDataCheck += 1
          }
        }
        if (goodsDataCheck === 0) {
          cancelRequest = true
          _this.$q.notify({
            message: 'Please Enter The Goods & Qty',
            icon: 'close',
            color: 'negative'
          })
        }
      } else {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Customer',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        putauth(_this.pathname + 'detail/', _this.newFormData)
          .then(res => {
            _this.table_list = []
            _this.editDataCancel()
            _this.getList()
            if (!res.detail) {
              _this.$q.notify({
                message: 'Success Edit DN',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    editDataCancel () {
      var _this = this
      _this.newForm = false
      _this.editid = 0
      _this.newFormData = {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    deleteData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.deleteForm = true
        _this.deleteid = e.id
      }
    },
    deleteDataSubmit () {
      var _this = this
      deleteauth(_this.pathname + 'list/' + _this.deleteid + '/')
        .then(res => {
          _this.table_list = []
          _this.deleteDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Delete DN',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    deleteDataCancel () {
      var _this = this
      _this.deleteForm = false
      _this.deleteid = 0
    },
    neworderData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.neworderForm = true
        _this.neworderid = e.id
      }
    },
    neworderDataSubmit () {
      var _this = this
      postauth(_this.pathname + 'neworder/' + _this.neworderid + '/', {})
        .then(res => {
          _this.table_list = []
          _this.neworderDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm DN Delivery',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    neworderDataCancel () {
      var _this = this
      _this.neworderForm = false
      _this.neworderid = 0
    },
    orderreleaseData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.neworder')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.neworder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.orderreleaseForm = true
        _this.orderreleaseid = e.id
      }
    },
    orderreleaseAllData () {
      var _this = this
      postauth(_this.pathname + 'orderrelease/', {})
        .then(res => {
          _this.table_list = []
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Release All Order',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    orderreleaseDataSubmit () {
      var _this = this
      putauth(_this.pathname + 'orderrelease/' + _this.orderreleaseid + '/', {})
        .then(res => {
          _this.table_list = []
          _this.orderreleaseDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Release DN Code',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    orderreleaseDataCancel () {
      var _this = this
      _this.orderreleaseForm = false
      _this.orderreleaseid = 0
    },
    getFocus (number) {
      this.listNumber = number
    },
    setOptions (val) {
      const _this = this
      if (!val) {
        _this[`goodsData${_this.listNumber}`].code = ''
      }
      const needle = val.toLowerCase()
      getauth('goods/?goods_code__icontains=' + needle).then(res => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
          if (_this.listNumber) {
            if (res.results[i].goods_code === val) {
              _this[`goodsData${_this.listNumber}`].code = val
            }
          }
        }
        _this.options1 = goodscodelist
      })
    },
    filterFn (val, update, abort) {
      if (val.length < 1) {
        abort()
        return
      }
      update(() => {
        this.options = this.options1
      })
    },
    setModel (val) {
      const _this = this
      _this.newFormData.customer = val
    },
    filterFnS (val, update, abort) {
      var _this = this
      update(() => {
        const needle = val.toLocaleLowerCase()
        const data_filter = _this.customer_list1
        _this.customer_list = data_filter.filter(v => v.toLocaleLowerCase().indexOf(needle) > -1)
      })
    },
    PrintPickingList (e) {
      var _this = this
      var QRCode = require('qrcode')
      QRCode.toDataURL(e.bar_code, [
        {
          errorCorrectionLevel: 'H',
          mode: 'byte',
          version: '2',
          type: 'image/jpeg'
        }
      ])
        .then(url => {
          _this.bar_code = url
        })
        .catch(err => {
          console.error(err)
        })
      _this.viewPLForm = true
      getauth(_this.pathname + 'pickinglist/' + e.id + '/')
        .then(res => {
          _this.pickinglist_print_table = []
          _this.picklist_check = 0
          res.forEach(item => {
            if (item.picked_qty > 0) {
              _this.picklist_check += 1
            } else {
            }
          })
          _this.pickinglist_print_table = res
          _this.viewPLForm = true
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    pickedData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.pickstock')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.pickstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.pickFormData.dn_code = e.dn_code
        _this.pickFormData.customer = e.customer
        getauth(_this.pathname + 'pickinglist/' + e.id + '/').then(res => {
          _this.pickedForm = true
          _this.pickedid = e.id
          _this.pickFormData.goodsData = res
        })
      }
    },
    pickedDataSubmit () {
      var _this = this
      _this.pickFormData.creater = _this.login_name
      postauth(_this.pathname + 'picked/' + _this.pickedid + '/', _this.pickFormData)
        .then(res => {
          _this.table_list = []
          _this.pickedDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm Picking List',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    pickedDataCancel () {
      var _this = this
      _this.pickedForm = false
      _this.pickedid = 0
      _this.pickFormData = {
        dn_code: '',
        customer: '',
        goodsData: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    viewData (e) {
      var _this = this
      ViewPrintAuth(_this.pathname + 'viewprint/' + e.id + '/').then(res => {
        _this.viewprint_table = res.dn_detail
        _this.warehouse_detail = res.warehouse_detail
        _this.customer_detail = res.customer_detail
        _this.viewdn = e.dn_code
        var QRCode = require('qrcode')
        QRCode.toDataURL(e.bar_code, [
          {
            errorCorrectionLevel: 'H',
            mode: 'byte',
            version: '2',
            type: 'image/jpeg'
          }
        ])
          .then(url => {
            _this.bar_code = url
          })
          .catch(err => {
            console.error(err)
          })
        _this.viewForm = true
      })
    },
    filterFnDispatch (val, update, abort) {
      var _this = this
      if (val.length < 1) {
        abort()
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        getauth('driver/?driver_name__icontains=' + needle)
          .then(res => {
            const drivernamelist = []
            for (let i = 0; i < res.results.length; i++) {
              drivernamelist.push(res.results[i].driver_name)
            }
            LocalStorage.set('driver_name_list', drivernamelist)
            _this.driver_options = LocalStorage.getItem('driver_name_list')
            _this.$forceUpdate()
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      })
    },
    DispatchDN (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.pickedstock')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.pickedstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.dispatchFormData.dn_code = e.dn_code
        _this.dispatchid = e.id
        _this.dispatchForm = true
      }
    },
    dispatchDataCancel () {
      var _this = this
      _this.dispatchFormData = { dn_code: '', driver: '' }
      _this.dispatchForm = false
    },
    dispatchDataSubmit () {
      var _this = this
      postauth(_this.pathname + 'dispatch/' + _this.dispatchid + '/', _this.dispatchFormData)
        .then(res => {
          _this.table_list = []
          _this.dispatchDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Dispatch',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    PODData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.shippedstock')) {
        _this.$q.notify({
          message: e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.shippedstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.podFormData.dn_code = e.dn_code
        _this.podFormData.customer = e.customer
        getauth(_this.pathname + 'detail/?dn_code=' + e.dn_code).then(res => {
          _this.podForm = true
          _this.podid = e.id
          _this.podFormData.goodsData = res.results
        })
      }
    },
    PODDataCancel () {
      var _this = this
      _this.podForm = false
      _this.podid = 0
      _this.podFormData = {
        dn_code: '',
        customer: '',
        goodsData: []
      }
    },
    PODDataSubmit () {
      var _this = this
      if (!(_this.isError1 || _this.isError2)) {
        postauth(_this.pathname + 'pod/' + _this.podid + '/', _this.podFormData)
          .then(res => {
            _this.table_list = []
            _this.PODDataCancel()
            _this.getList()
            if (!res.detail) {
              _this.$q.notify({
                message: 'Success Dispatch',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    }
  },
  created () {
    var _this = this
    if (LocalStorage.has('openid')) {
      _this.openid = LocalStorage.getItem('openid')
    } else {
      _this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      _this.login_name = LocalStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
      _this.authin = '1'
      _this.table_list = []
      _this.getList()
    } else {
      _this.authin = '0'
    }
    if (LocalStorage.has('goods_code_list')) {
    } else {
      LocalStorage.set('goods_code_list', [])
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  updated () {},
  destroyed () {}
}
</script>

<style scoped>
.dn-page {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.metric-strip {
  display: none;
}

.status-tabs {
  display: flex;
  gap: 0;
  overflow-x: auto;
  padding: 0 0 0 2px;
  border-bottom: 1px solid #cfc8ff;
  background: #fff;
}

.status-tab {
  border: 1px solid #d8dff0;
  border-bottom: 0;
  background: #fff;
  color: #44556d;
  border-radius: 0;
  padding: 9px 22px;
  min-width: 96px;
  margin-right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.status-tab em {
  font-style: normal;
  color: #7b8ba2;
  margin-left: 8px;
}

.status-tab.active {
  border-color: #7d6bff;
  background: #fff;
  color: #5a43f2;
  box-shadow: inset 0 2px 0 #7d6bff;
}

.platform-table {
  border: 1px solid #dde3ee;
  border-radius: 8px;
  overflow-x: auto;
  overflow-y: hidden;
  background: #fff;
  box-shadow: none;
}

.list-shell {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.table-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.table-title-row.compact {
  min-height: 34px;
}

.list-caption {
  font-size: 14px;
  font-weight: 700;
  color: #293859;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-panel {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid #e4e9f2;
  border-radius: 6px;
  background: #fff;
}

.compact-panel {
  padding: 14px 12px 10px;
  border: 0;
  border-bottom: 1px solid #ece7ff;
  border-radius: 0;
}

.filter-grid {
  align-items: start;
  flex: 1;
  min-width: 760px;
  display: grid;
  grid-template-columns: 1.2fr 1fr 0.9fr 1fr;
  gap: 10px;
}

.compact-grid-bar {
  min-width: 0;
  grid-template-columns: 1.4fr 0.8fr 0.9fr 1fr;
}

.toolbar-field {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-label {
  flex-shrink: 0;
  font-size: 13px;
  color: #3f4d66;
  font-weight: 600;
}

.filter-actions {
  padding-top: 2px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-actions.compact {
  padding-top: 0;
}

.toolbar-strip {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 12px 0 10px;
  border-bottom: 1px solid #edf1f6;
}

.toolbar-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.toolbar-group.compact {
  justify-content: flex-end;
}

.manual-table-wrap {
  width: 100%;
  overflow: auto;
  background: #fff;
}

.manual-table {
  width: 100%;
  min-width: 2200px;
  border-collapse: collapse;
  table-layout: fixed;
}

.manual-table th,
.manual-table td {
  border-right: 1px solid #edf1f6;
  border-bottom: 1px solid #edf1f6;
  padding: 7px 6px;
  white-space: nowrap;
  font-size: 12px;
  color: #22324a;
  background: #fff;
  vertical-align: middle;
}

.manual-table th {
  background: #f7f9fc;
  color: #5d6c82;
  font-weight: 700;
}

.manual-empty {
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5f6f86;
  font-size: 14px;
  border-top: 1px solid #edf1f6;
}

.cell-index {
  width: 54px;
  text-align: center;
}

.cell-select {
  width: 42px;
  text-align: center;
}

.cell-action {
  width: 128px;
}

.status-tab em {
  display: none;
}

.dense-header-row {
  background: #f5f7fb;
}

.dense-header-row .q-th {
  background: #f7f9fc;
  border-right: 1px solid #e6ebf2;
  white-space: nowrap;
  font-size: 12px;
  font-weight: 700;
  color: #5d6c82;
  padding: 7px 6px;
}

.dense-body-row .q-td {
  white-space: nowrap;
  background: #fff;
  border-right: 1px solid #edf1f6;
  padding: 7px 6px;
  font-size: 12px;
  color: #22324a;
  vertical-align: middle;
  border-color: #edf1f6;
}

.sub-filter-row {
  background: #fff;
}

.sub-filter-cell {
  height: 34px;
  padding: 4px 6px;
  border-right: 1px solid #edf1f6;
  border-bottom: 1px solid #edf1f6;
  font-size: 12px;
  color: #5f6f86;
  background: #fff;
}

.mini-filter {
  width: 100%;
  height: 24px;
  border: 1px solid #d9e1ef;
  border-radius: 3px;
  padding: 0 6px;
  font-size: 12px;
}

.mini-select {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 24px;
  min-width: 48px;
  padding: 0 8px;
  border: 1px solid #d9e1ef;
  border-radius: 3px;
  background: #fafbfd;
}

.row-index-cell,
.row-select-cell {
  text-align: center !important;
}

.waybill-code-cell {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.waybill-code {
  font-size: 13px;
  font-weight: 700;
  color: #1b5fc9;
}

.waybill-meta {
  font-size: 12px;
  color: #8a96ab;
}

.mark-text {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 700;
}

.mark-gray {
  color: #8f96a3;
}

.mark-blue {
  color: #1565d8;
}

.mark-red {
  color: #ff8a00;
}

.amount-dark {
  font-weight: 700;
  color: #4c586a;
}

.soft-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 52px;
  height: 22px;
  padding: 0 8px;
  border-radius: 11px;
  background: #eef3ff;
  color: #51627d;
}

.soft-tag {
  display: inline-flex;
  align-items: center;
  padding: 0 8px;
  height: 22px;
  border-radius: 4px;
  background: #f5f7fb;
  color: #51627d;
}

.muted-text {
  color: #7e8aa1;
}

.mark-soft {
  color: #5d6c82;
}

.amount-blue {
  font-weight: 700;
  color: #1565d8;
}

.amount-red {
  font-weight: 700;
  color: #ff8a00;
}

.waybill-code-cell.compact {
  gap: 1px;
}

.filter-compact :deep(.q-field__control) {
  min-height: 34px;
}

.filter-keyword :deep(.q-field__native),
.filter-keyword :deep(input) {
  font-size: 12px;
}

.table-search-actions .q-btn {
  min-height: 34px;
}

.action-link-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2px;
}

.table-link {
  line-height: 16px;
  color: #2fa4ff;
  cursor: pointer;
  white-space: nowrap;
  font-size: 12px;
}

.table-link.danger {
  color: #2fa4ff;
}

.status-dot::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.action-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2px;
}

.status-badge {
  white-space: nowrap;
  padding: 2px 8px;
  font-size: 12px;
  line-height: 18px;
  border-radius: 10px;
  font-weight: 600;
}

.status-fresh {
  background: #e8f1ff;
  color: #195fc7;
}

.status-picking {
  background: #fff3dc;
  color: #b96b08;
}

.status-shipped {
  background: #e7f8ef;
  color: #168651;
}

.status-finished {
  background: #ebeef3;
  color: #43546d;
}

.status-void {
  background: #fbeaea;
  color: #c53d3d;
}

.status-default {
  background: #f1f4f8;
  color: #69788f;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  padding: 14px 8px 8px;
}

.list-summary-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #dfe6f0;
  border-top: 0;
  background: linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%);
  color: #3d4c63;
  font-size: 12px;
  font-weight: 600;
}

.push-right {
  margin-left: auto;
}

.summary-label {
  min-width: 48px;
  color: #1f2d44;
  font-weight: 700;
}

.summary-item {
  white-space: nowrap;
}

.page-total {
  color: #5f6f86;
  font-size: 13px;
}

.page-jump input {
  height: 30px;
  border: 1px solid #d7deea;
  border-radius: 6px;
  background: #fff;
}

.empty-state {
  justify-content: center;
}

@media (max-width: 1200px) {
  .metric-strip {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .metric-strip {
    grid-template-columns: 1fr;
  }

  .table-title-row,
  .filter-panel,
  .toolbar-strip {
  align-items: center;
  padding: 10px 0 8px;
  border-top: 1px solid #eef2f7;
    flex-direction: column;
    align-items: stretch;
  }

  .filter-grid {
    align-items: start;
    min-width: 0;
    grid-template-columns: 1fr;
  }

  .toolbar-field {
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
  }

  .toolbar-group.compact {
    justify-content: flex-start;
  }

  .status-tab {
    width: 100%;
  }
}
</style>













