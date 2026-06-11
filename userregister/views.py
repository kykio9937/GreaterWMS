import json
import os
import random
import re

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from scanner.models import ListModel as Scanner
from staff.models import ListModel as Staff
from userlogin.models import PhoneLoginCode
from userprofile.models import Users
from utils.demo_transport_seed import DEMO_PHONE, ensure_demo_transport_data
from utils.fbmsg import FBMsg
from utils.md5 import Md5


PHONE_PATTERN = re.compile(r'^1\d{10}$')
COMMON_PASSWORDS = {
    '12345678', '123456789', '1234567890', '11111111', '88888888',
    'password', 'qwerty123', '00000000'
}


def _json_body(request):
    try:
        return json.loads(request.body.decode() or '{}')
    except Exception:
        return {}


def _client_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')


def _error(message, code='400', data=None):
    return {'code': code, 'msg': message, 'data': data}


def _consume_phone_code(phone, code, scene='register'):
    record = PhoneLoginCode.objects.filter(
        phone=phone,
        code=str(code),
        scene=scene,
        is_used=False,
        expire_time__gte=timezone.now()
    ).order_by('-id').first()
    if record is None:
        return None
    record.is_used = True
    record.save(update_fields=['is_used', 'update_time'])
    return record


def _validate_password(password, phone, display_name):
    password = str(password or '')
    if password == '':
        return '请输入登录密码'
    if len(password) < 8:
        return '密码长度不能少于8位'
    if password.isdigit():
        return '密码不能设置得过于简单，不能全部为数字'
    lowered = password.lower()
    if lowered in COMMON_PASSWORDS:
        return '密码过于常见，请更换一个更安全的密码'
    if phone and phone[-6:] in password:
        return '密码不能包含手机号中的连续数字'
    if display_name and str(display_name).strip() and str(display_name).strip().lower() in lowered:
        return '密码不能与用户名过于相似'
    return ''


def _seed_basic_demo_data(transaction_code):
    from company.models import ListModel as Company
    from warehouse.models import ListModel as Warehouse
    from customer.models import ListModel as Customer
    from driver.models import ListModel as Driver

    if not Company.objects.filter(openid=transaction_code, is_delete=False).exists():
        Company.objects.create(
            openid=transaction_code,
            company_name='WMS Demo',
            company_city='西安',
            company_address='西安市演示办公区',
            company_contact='13800000000',
            company_manager='演示管理员',
            creater='DemoData'
        )

    if not Warehouse.objects.filter(openid=transaction_code, is_delete=False).exists():
        Warehouse.objects.create(
            openid=transaction_code,
            warehouse_name='Center Warehouse',
            warehouse_city='西安',
            warehouse_address='西安市演示仓库',
            warehouse_contact='13800000000',
            warehouse_manager='演示管理员',
            creater='DemoData'
        )

    if not Customer.objects.filter(openid=transaction_code, is_delete=False).exists():
        for index in range(1, 6):
            Customer.objects.create(
                openid=transaction_code,
                customer_name=f'演示客户{index}',
                customer_city='西安',
                customer_address=f'西安市客户地址{index}',
                customer_contact=f'1380000000{index}',
                customer_manager=f'客户联系人{index}',
                creater='DemoData'
            )

    if not Driver.objects.filter(openid=transaction_code, is_delete=False).exists():
        for index in range(1, 6):
            Driver.objects.create(
                openid=transaction_code,
                driver_name=f'演示司机{index}',
                license_plate=f'陕A88{index:03d}',
                contact=f'1390000000{index}',
                creater='DemoData'
            )


@csrf_exempt
def register(request, *args, **kwargs):
    post_data = _json_body(request)
    display_name = str(post_data.get('name') or '').strip()
    phone = str(post_data.get('phone') or '').strip()
    code = str(post_data.get('code') or '').strip()
    password = str(post_data.get('password') or '')
    password_confirm = str(post_data.get('password_confirm') or '')
    ip = _client_ip(request)

    if not PHONE_PATTERN.match(phone):
        ret = _error('请输入正确的11位手机号')
        ret['ip'] = ip
        return JsonResponse(ret)

    if code == '':
        ret = _error('请输入验证码')
        ret['ip'] = ip
        return JsonResponse(ret)

    if _consume_phone_code(phone, code) is None:
        ret = _error('验证码无效或已过期')
        ret['ip'] = ip
        return JsonResponse(ret)

    if password_confirm == '':
        ret = _error('请再次输入确认密码')
        ret['ip'] = ip
        return JsonResponse(ret)

    password_error = _validate_password(password, phone, display_name)
    if password_error:
        ret = _error(password_error)
        ret['ip'] = ip
        return JsonResponse(ret)

    if password != password_confirm:
        ret = _error('两次输入的密码不一致')
        ret['ip'] = ip
        return JsonResponse(ret)

    if Users.objects.filter(phone=phone, developer=1, is_delete=0).exists():
        ret = _error('该手机号已注册，请直接登录')
        ret['ip'] = ip
        return JsonResponse(ret)

    if display_name == '':
        display_name = f'用户{phone[-4:]}'
    if Users.objects.filter(name=display_name, developer=1, is_delete=0).exists():
        display_name = f'{display_name}{random.randint(10, 99)}'

    transaction_code = Md5.md5(phone)
    user = User.objects.create_user(username=phone, password=password)
    Users.objects.create(
        user_id=user.id,
        name=display_name,
        phone=phone,
        openid=transaction_code,
        appid=Md5.md5(phone + '1'),
        t_code=Md5.md5(str(timezone.now())),
        developer=1,
        ip=ip
    )

    auth.login(request, user)
    staff_detail = Staff.objects.create(
        staff_name=display_name,
        staff_type='Admin',
        check_code=random.randint(1000, 9999),
        openid=transaction_code
    )

    folder = os.path.join(settings.BASE_DIR, 'media', transaction_code)
    for sub_path in ['', 'win32', 'linux', 'darwin']:
        os.makedirs(os.path.join(folder, sub_path), exist_ok=True)

    Scanner.objects.get_or_create(
        openid=transaction_code,
        mode='USER',
        code=phone,
        bar_code=Md5.md5(phone)
    )

    _seed_basic_demo_data(transaction_code)
    if phone == DEMO_PHONE:
        ensure_demo_transport_data(transaction_code)

    ret = FBMsg.ret()
    ret['msg'] = '注册成功'
    ret['ip'] = ip
    ret['data'] = {
        'openid': transaction_code,
        'name': display_name,
        'user_id': staff_detail.id,
        'phone': phone
    }
    return JsonResponse(ret)
