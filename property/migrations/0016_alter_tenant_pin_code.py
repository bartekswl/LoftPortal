# Generated by Django 3.2.5 on 2021-07-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0015_alter_tenant_pin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='pin_code',
            field=models.CharField(blank=True, default='se3464', editable=False, max_length=6),
        ),
    ]
