import json
import random
import re
from datetime import timedelta

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from staff.models import ListModel as staff
from userlogin.models import PhoneLoginCode
from userprofile.models import Users
from utils.demo_transport_seed import DEMO_PHONE, ensure_demo_transport_data
from utils.fbmsg import FBMsg


PHONE_PATTERN = re.compile(r'^1\d{10}$')
CODE_EXPIRE_MINUTES = 5


def _json_body(request):
    try:
        return json.loads(request.body.decode() or '{}')
    except json.JSONDecodeError:
        return {}


def _get_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')


def _error(message, code='400'):
    return {'code': code, 'msg': message, 'data': None}


def _normalize_phone(phone):
    return str(phone or '').strip()


def _validate_phone(phone):
    return PHONE_PATTERN.match(phone) is not None


def _consume_phone_code(phone, code, scene):
    code_record = PhoneLoginCode.objects.filter(
        phone=phone,
        code=str(code),
        scene=scene,
        is_used=False,
        expire_time__gte=timezone.now()
    ).order_by('-id').first()
    if code_record is None:
        return None
    code_record.is_used = True
    code_record.save(update_fields=['is_used', 'update_time'])
    return code_record


def _build_login_response(user_detail):
    staff_detail = staff.objects.filter(openid=user_detail.openid, staff_name=str(user_detail.name)).order_by('id').first()
    if staff_detail is None:
        staff_detail = staff.objects.create(
            staff_name=str(user_detail.name),
            staff_type='Admin',
            check_code=random.randint(1000, 9999),
            openid=user_detail.openid
        )
    return {
        'name': user_detail.name,
        'openid': user_detail.openid,
        'user_id': staff_detail.id,
        'phone': user_detail.phone
    }


@csrf_exempt
def send_code(request, *args, **kwargs):
    post_data = _json_body(request)
    phone = _normalize_phone(post_data.get('phone'))
    scene = str(post_data.get('scene') or 'login').strip() or 'login'
    ip = _get_ip(request)

    if not _validate_phone(phone):
        err_ret = _error('请输入正确的11位手机号')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    code = ''.join(random.choice('0123456789') for _ in range(6))
    PhoneLoginCode.objects.filter(phone=phone, scene=scene, is_used=False).update(is_used=True)
    PhoneLoginCode.objects.create(
        phone=phone,
        code=code,
        scene=scene,
        expire_time=timezone.now() + timedelta(minutes=CODE_EXPIRE_MINUTES)
    )

    ret = FBMsg.ret()
    ret['msg'] = '验证码已生成'
    ret['ip'] = ip
    ret['data'] = {
        'phone': phone,
        'scene': scene,
        'debug_code': code,
        'expire_minutes': CODE_EXPIRE_MINUTES
    }
    return JsonResponse(ret)


@csrf_exempt
def login(request, *args, **kwargs):
    post_data = _json_body(request)
    phone = _normalize_phone(post_data.get('phone'))
    code = str(post_data.get('code') or '').strip()
    ip = _get_ip(request)

    if not _validate_phone(phone):
        err_ret = _error('请输入正确的11位手机号')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    if code == '':
        err_ret = _error('请输入验证码')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    if _consume_phone_code(phone, code, 'login') is None:
        err_ret = _error('验证码无效或已过期')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    user_detail = Users.objects.filter(phone=phone, developer=1, is_delete=0).order_by('-id').first()
    if user_detail is None:
        err_ret = _error('该手机号尚未注册，请先完成注册')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    user = User.objects.filter(id=user_detail.user_id).first()
    if user is None:
        user = User.objects.filter(username=phone).first()
    if user is None:
        err_ret = _error('账号不存在，请先注册')
        err_ret['ip'] = ip
        return JsonResponse(err_ret)

    auth.login(request, user)
    if phone == DEMO_PHONE:
        ensure_demo_transport_data(user_detail.openid)
    ret = FBMsg.ret()
    ret['msg'] = '登录成功'
    ret['ip'] = ip
    ret['data'] = _build_login_response(user_detail)
    return JsonResponse(ret)
