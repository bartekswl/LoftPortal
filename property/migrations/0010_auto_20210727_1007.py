# Generated by Django 3.2.5 on 2021-07-27 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0009_auto_20210727_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='pin_code',
            field=models.CharField(blank=True, default='SE6840', editable=False, max_length=6),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='portal_user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant', to=settings.AUTH_USER_MODEL),
        ),
    ]
