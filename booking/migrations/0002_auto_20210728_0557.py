# Generated by Django 3.2.5 on 2021-07-28 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_alter_tenant_pin_code'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gymbooking',
            old_name='is_running',
            new_name='no_show',
        ),
        migrations.AddField(
            model_name='gymbooking',
            name='flat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='property.flat'),
        ),
        migrations.AddField(
            model_name='gymbooking',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='property.tenant'),
        ),
    ]