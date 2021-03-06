# Generated by Django 3.2.5 on 2021-07-29 09:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0015_alter_tenant_pin_code'),
        ('booking', '0003_alter_gymbooking_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymbooking',
            name='made_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.concierge'),
        ),
        migrations.AlterField(
            model_name='gymbooking',
            name='time',
            field=models.CharField(choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('xxx', 'xxx'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21')], max_length=3, null=True),
        ),
        migrations.CreateModel(
            name='GymBookingBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('all_day', models.BooleanField(default=False, null=True)),
                ('time', models.CharField(blank=True, choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('xxx', 'xxx'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21')], max_length=3, null=True)),
                ('block_length', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)])),
                ('block_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.concierge')),
            ],
        ),
    ]
