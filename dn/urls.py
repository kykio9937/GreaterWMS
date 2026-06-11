from django.urls import path, re_path
from . import views

urlpatterns = [
path(r'list/', views.DnListViewSet.as_view({"get": "list", "post": "create"}), name="dnlist"),
re_path(r'^list/(?P<pk>\d+)/$', views.DnListViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}), name="dnlist_1"),
path(r'detail/', views.DnDetailViewSet.as_view({"get": "list", "post": "create", 'put': 'update'}), name="dndetail"),
re_path(r'^detail/(?P<pk>\d+)/$', views.DnDetailViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
}), name="dndetail_1"),
re_path(r'^viewprint/(?P<pk>\d+)/$', views.DnViewPrintViewSet.as_view({
    'get': 'retrieve',
}), name="dnviewprint_1"),
re_path(r'^neworder/(?P<pk>\d+)/$', views.DnNewOrderViewSet.as_view({
    'post': 'create',
}), name="preloadid_1"),
path(r'orderrelease/', views.DnOrderReleaseViewSet.as_view({"post": "create"}), name="orderrelease"),
re_path(r'^orderrelease/(?P<pk>\d+)/$', views.DnOrderReleaseViewSet.as_view({
    'put': 'update',
}), name="orderrelease_1"),
path(r'pickinglistfilter/', views.DnPickingListFilterViewSet.as_view({"get": "list"}), name="pickinglistfilter"),
re_path(r'^pickinglist/(?P<pk>\d+)/$', views.DnPickingListViewSet.as_view({
    'get': 'retrieve',
}), name="pickinglist_1"),
path(r'picked/', views.DnPickedViewSet.as_view({'put': 'update'}), name="picked"),
re_path(r'^picked/(?P<pk>\d+)/$', views.DnPickedViewSet.as_view({
    'post': 'create',
    'put': 'update'
}), name="picked_1"),
re_path(r'^dispatch/(?P<pk>\d+)/$', views.DnDispatchViewSet.as_view({
    'post': 'create',
}), name="dispatch_1"),
re_path(r'^pod/(?P<pk>\d+)/$', views.DnPODViewSet.as_view({
    'post': 'create',
}), name="pod_1"),
path(r'create_waybill/', views.DnCreateWaybillViewSet.as_view({"post": "create"}), name="dn_create_waybill"),
path(r'transit/', views.DnTransitViewSet.as_view({"get": "list"}), name="dn_transit"),
path(r'reconcile/customer/summary/', views.DnCustomerReconcileSummaryViewSet.as_view({"get": "list"}), name="dn_customer_reconcile_summary"),
path(r'reconcile/customer/detail/', views.DnCustomerReconcileDetailViewSet.as_view({"get": "list"}), name="dn_customer_reconcile_detail"),
re_path(r'^reconcile/customer/(?P<pk>\d+)/$', views.DnCustomerReconcileConfirmViewSet.as_view({
    'post': 'create',
}), name="dn_customer_reconcile_confirm"),
path(r'reconcile/carrier/summary/', views.DnCarrierReconcileSummaryViewSet.as_view({"get": "list"}), name="dn_carrier_reconcile_summary"),
path(r'reconcile/carrier/detail/', views.DnCarrierReconcileDetailViewSet.as_view({"get": "list"}), name="dn_carrier_reconcile_detail"),
re_path(r'^reconcile/carrier/(?P<pk>\d+)/$', views.DnCarrierReconcileConfirmViewSet.as_view({
    'post': 'create',
}), name="dn_carrier_reconcile_confirm"),
path(r'filelist/', views.FileListDownloadView.as_view({"get": "list"}), name="dnfilelistdownload"),
path(r'filedetail/', views.FileDetailDownloadView.as_view({"get": "list"}), name="dnfiledetaildownload"),

]
