# Generated by Django 3.2.5 on 2021-07-30 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0022_alter_tenant_pin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='pin_code',
            field=models.CharField(blank=True, default='se5794', editable=False, max_length=6),
        ),
    ]