# Generated by Django 3.2.5 on 2021-07-27 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_auto_20210727_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='pin_code',
            field=models.CharField(blank=True, default='SE5931', editable=False, max_length=6),
        ),
    ]