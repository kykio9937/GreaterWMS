from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.CharField(blank=True, db_index=True, default='', max_length=20, verbose_name='Phone'),
        ),
    ]
