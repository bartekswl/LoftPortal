# Generated by Django 3.2.5 on 2021-09-18 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0010_alter_parcel_date_arrived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='additional_notes',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
