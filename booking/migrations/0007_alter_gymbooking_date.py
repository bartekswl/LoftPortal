# Generated by Django 3.2.5 on 2021-07-29 10:24

import booking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_gymbookingblock_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymbooking',
            name='date',
            field=models.DateField(null=True, validators=[booking.models.validate_date]),
        ),
    ]
