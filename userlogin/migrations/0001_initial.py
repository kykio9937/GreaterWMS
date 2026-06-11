from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneLoginCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(db_index=True, max_length=20, verbose_name='Phone')),
                ('code', models.CharField(max_length=6, verbose_name='Code')),
                ('scene', models.CharField(default='login', max_length=20, verbose_name='Scene')),
                ('is_used', models.BooleanField(default=False, verbose_name='Used')),
                ('expire_time', models.DateTimeField(verbose_name='Expire Time')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
            ],
            options={
                'verbose_name': 'Phone Login Code',
                'verbose_name_plural': 'Phone Login Code',
                'db_table': 'phone_login_code',
                'ordering': ['-id'],
            },
        ),
    ]
