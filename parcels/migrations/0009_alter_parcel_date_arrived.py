# Generated by Django 3.2.5 on 2021-09-02 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0008_alter_parcel_date_arrived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='date_arrived',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]