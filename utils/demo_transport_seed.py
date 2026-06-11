from django.utils import timezone

from customer.models import ListModel as Customer
from dn.models import DnDetailModel, DnListModel
from driver.models import DispatchListModel, ListModel as Driver
from utils.md5 import Md5


DEMO_PHONE = '13800000000'


def _pick_customer_name(openid, fallback):
    customer = Customer.objects.filter(openid=openid, is_delete=False).order_by('id').first()
    if customer is not None and customer.customer_name:
        return customer.customer_name
    return fallback


def _pick_driver(openid, index):
    driver = Driver.objects.filter(openid=openid, is_delete=False).order_by('id')[index:index + 1].first()
    if driver is not None:
        return driver
    return Driver.objects.create(
        openid=openid,
        driver_name='演示司机{}'.format(index + 1),
        license_plate='陕A{:05d}'.format(1000 + index),
        contact='1380000{:04d}'.format(index + 1),
        creater='DemoData'
    )


def ensure_demo_transport_data(openid, creater='DemoData'):
    if not openid:
        return
    if DnListModel.objects.filter(openid=openid, is_delete=False).exists():
        return

    now = timezone.now()
    demo_rows = [
        {
            'dn_code': 'DNDEMO2026061101',
            'customer': _pick_customer_name(openid, '西安直营客户'),
            'status': 5,
            'line_name': '西安-咸阳干线',
            'driver_name': '王师傅',
            'plate_number': '陕A86521',
            'supplier_name': '西北承运商A',
            'income': 12800,
            'carrier_cost': 10450,
            'reward_fee': 260,
            'other_fee': 120,
            'dispatch_time': now.replace(hour=8, minute=30, second=0, microsecond=0),
            'signed_time': None,
            'customer_reconciled': False,
            'carrier_reconciled': False,
            'goods': [('电子配件', 'G-DEMO-001', 120)]
        },
        {
            'dn_code': 'DNDEMO2026061102',
            'customer': _pick_customer_name(openid, '宝鸡项目客户'),
            'status': 5,
            'line_name': '西安-宝鸡专线',
            'driver_name': '李师傅',
            'plate_number': '陕A90317',
            'supplier_name': '关中承运商B',
            'income': 9650,
            'carrier_cost': 8120,
            'reward_fee': 180,
            'other_fee': 80,
            'dispatch_time': now.replace(hour=10, minute=15, second=0, microsecond=0),
            'signed_time': None,
            'customer_reconciled': False,
            'carrier_reconciled': False,
            'goods': [('快消品', 'G-DEMO-002', 86)]
        },
        {
            'dn_code': 'DNDEMO2026061001',
            'customer': _pick_customer_name(openid, '渭南直营网点'),
            'status': 6,
            'line_name': '西安-渭南干线',
            'driver_name': '张师傅',
            'plate_number': '陕A77204',
            'supplier_name': '东线承运商C',
            'income': 11200,
            'carrier_cost': 9180,
            'reward_fee': 220,
            'other_fee': 60,
            'dispatch_time': now.replace(day=max(1, now.day - 1), hour=7, minute=45, second=0, microsecond=0),
            'signed_time': now.replace(hour=16, minute=20, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S'),
            'customer_reconciled': True,
            'carrier_reconciled': False,
            'goods': [('家电整机', 'G-DEMO-003', 40)]
        },
        {
            'dn_code': 'DNDEMO2026060901',
            'customer': _pick_customer_name(openid, '延安合作客户'),
            'status': 6,
            'line_name': '西安-延安干线',
            'driver_name': '赵师傅',
            'plate_number': '陕A61128',
            'supplier_name': '陕北承运商D',
            'income': 15600,
            'carrier_cost': 12880,
            'reward_fee': 320,
            'other_fee': 150,
            'dispatch_time': now.replace(day=max(1, now.day - 2), hour=9, minute=10, second=0, microsecond=0),
            'signed_time': now.replace(day=max(1, now.day - 1), hour=11, minute=35, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S'),
            'customer_reconciled': True,
            'carrier_reconciled': True,
            'goods': [('工业辅料', 'G-DEMO-004', 64)]
        }
    ]

    for index, row in enumerate(demo_rows):
        driver = _pick_driver(openid, index)
        transport_payload = {
            'line_name': row['line_name'],
            'driver_name': row['driver_name'] or driver.driver_name,
            'plate_number': row['plate_number'] or driver.license_plate,
            'selected_supplier': row['supplier_name'],
            'carrier_cost': row['carrier_cost'],
            'driver_reward': row['reward_fee'],
            'extra_fee': row['other_fee'],
            'dispatch_time': row['dispatch_time'].strftime('%Y-%m-%d %H:%M:%S'),
            'signed_time': row['signed_time'] or '',
            'customer_reconciled': row['customer_reconciled'],
            'carrier_reconciled': row['carrier_reconciled'],
            'business_income': row['income'],
            'detail': [
                {
                    'transportation_supplier': row['supplier_name'],
                    'transportation_cost': row['income']
                }
            ]
        }
        dn_obj = DnListModel.objects.create(
            dn_code=row['dn_code'],
            dn_status=row['status'],
            total_weight=round(sum(item[2] for item in row['goods']) * 0.012, 4),
            total_volume=round(sum(item[2] for item in row['goods']) * 0.003, 4),
            total_cost=row['income'],
            customer=row['customer'],
            creater=creater,
            bar_code=Md5.md5(row['dn_code']),
            openid=openid,
            transportation_fee=transport_payload
        )
        for goods_desc, goods_code, goods_qty in row['goods']:
            DnDetailModel.objects.create(
                dn_code=row['dn_code'],
                dn_status=row['status'],
                customer=row['customer'],
                goods_code=goods_code,
                goods_desc=goods_desc,
                goods_qty=goods_qty,
                pick_qty=goods_qty,
                picked_qty=goods_qty,
                intransit_qty=goods_qty if row['status'] == 5 else 0,
                delivery_actual_qty=goods_qty if row['status'] == 6 else 0,
                goods_weight=round(goods_qty * 0.012, 4),
                goods_volume=round(goods_qty * 0.003, 4),
                goods_cost=row['income'],
                creater=creater,
                openid=openid
            )
        DispatchListModel.objects.get_or_create(
            openid=openid,
            dn_code=row['dn_code'],
            defaults={
                'driver_name': row['driver_name'] or driver.driver_name,
                'contact': int(driver.contact),
                'creater': creater
            }
        )
        DnListModel.objects.filter(id=dn_obj.id).update(
            create_time=row['dispatch_time'],
            update_time=row['dispatch_time']
        )
        DnDetailModel.objects.filter(openid=openid, dn_code=row['dn_code']).update(
            create_time=row['dispatch_time'],
            update_time=row['dispatch_time']
        )
        DispatchListModel.objects.filter(openid=openid, dn_code=row['dn_code']).update(
            create_time=row['dispatch_time'],
            update_time=row['dispatch_time']
        )
