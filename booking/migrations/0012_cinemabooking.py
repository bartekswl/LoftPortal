# Generated by Django 3.2.5 on 2021-08-01 04:24

import booking.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0027_alter_tenant_pin_code'),
        ('booking', '0011_rename_block_length_gymbookingblock_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, validators=[booking.models.validate_date])),
                ('time', models.CharField(choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21')], max_length=2, null=True)),
                ('duration', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1, null=True)),
                ('pax', models.IntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('additional_notes', models.TextField(blank=True, max_length=50)),
                ('flat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='property.flat')),
                ('made_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.concierge')),
                ('tenant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='property.tenant')),
            ],
        ),
    ]
