# Generated by Django 3.2.5 on 2021-09-18 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0011_alter_parcel_additional_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='turnover',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
