# Generated by Django 3.2.5 on 2021-08-10 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0004_alter_parcel_pickup_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='pickup_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
