import json
import random
import re
from datetime import timedelta

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from staff.models import ListModel as Staff
from userlogin.models import PhoneLoginCode
from userprofile.models import Users
from utils.demo_transport_seed import DEMO_PHONE, ensure_demo_transport_data
from utils.fbmsg import FBMsg


PHONE_PATTERN = re.compile(r'^1\d{10}$')
CODE_EXPIRE_MINUTES = 5


def _json_body(request):
    try:
        return json.loads(request.body.decode() or '{}')
    except Exception:
        return {}


def _client_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')


def _error(message, code='400', data=None):
    return {'code': code, 'msg': message, 'data': data}


def _normalize_phone(phone):
    return str(phone or '').strip()


def _valid_phone(phone):
    return PHONE_PATTERN.match(phone) is not None


def _consume_phone_code(phone, code, scene):
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


def _ensure_staff(user_profile):
    staff_detail = Staff.objects.filter(
        openid=user_profile.openid,
        staff_name=str(user_profile.name)
    ).order_by('id').first()
    if staff_detail is None:
        staff_detail = Staff.objects.create(
            staff_name=str(user_profile.name),
            staff_type='Admin',
            check_code=random.randint(1000, 9999),
            openid=user_profile.openid
        )
    return staff_detail


def _build_login_response(user_profile):
    staff_detail = _ensure_staff(user_profile)
    return {
        'name': user_profile.name,
        'openid': user_profile.openid,
        'user_id': staff_detail.id,
        'phone': user_profile.phone
    }


@csrf_exempt
def send_code(request, *args, **kwargs):
    post_data = _json_body(request)
    phone = _normalize_phone(post_data.get('phone'))
    scene = str(post_data.get('scene') or 'login').strip() or 'login'
    ip = _client_ip(request)

    if not _valid_phone(phone):
        ret = _error('请输入正确的11位手机号')
        ret['ip'] = ip
        return JsonResponse(ret)

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
    mode = str(post_data.get('mode') or 'code').strip() or 'code'
    phone = _normalize_phone(post_data.get('phone'))
    code = str(post_data.get('code') or '').strip()
    password = str(post_data.get('password') or '')
    ip = _client_ip(request)

    if not _valid_phone(phone):
        ret = _error('请输入正确的11位手机号')
        ret['ip'] = ip
        return JsonResponse(ret)

    user_profile = Users.objects.filter(phone=phone, developer=1, is_delete=0).order_by('-id').first()
    if user_profile is None:
        ret = _error('该手机号尚未注册，请先完成注册')
        ret['ip'] = ip
        return JsonResponse(ret)

    user = User.objects.filter(id=user_profile.user_id).first() or User.objects.filter(username=phone).first()
    if user is None:
        ret = _error('账号不存在，请重新注册')
        ret['ip'] = ip
        return JsonResponse(ret)

    if mode == 'password':
        if password == '':
            ret = _error('请输入登录密码')
            ret['ip'] = ip
            return JsonResponse(ret)
        if not user.check_password(password):
            ret = _error('手机号或密码不正确')
            ret['ip'] = ip
            return JsonResponse(ret)
    else:
        if code == '':
            ret = _error('请输入验证码')
            ret['ip'] = ip
            return JsonResponse(ret)
        if _consume_phone_code(phone, code, 'login') is None:
            ret = _error('验证码无效或已过期')
            ret['ip'] = ip
            return JsonResponse(ret)

    auth.login(request, user)
    if phone == DEMO_PHONE:
        ensure_demo_transport_data(user_profile.openid)

    ret = FBMsg.ret()
    ret['msg'] = '登录成功'
    ret['ip'] = ip
    ret['data'] = _build_login_response(user_profile)
    return JsonResponse(ret)
