from django.db import models


class PhoneLoginCode(models.Model):
    phone = models.CharField(max_length=20, db_index=True, verbose_name='Phone')
    code = models.CharField(max_length=6, verbose_name='Code')
    scene = models.CharField(max_length=20, default='login', verbose_name='Scene')
    is_used = models.BooleanField(default=False, verbose_name='Used')
    expire_time = models.DateTimeField(verbose_name='Expire Time')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create Time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update Time')

    class Meta:
        db_table = 'phone_login_code'
        verbose_name = 'Phone Login Code'
        verbose_name_plural = 'Phone Login Code'
        ordering = ['-id']
