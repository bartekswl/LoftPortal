# Generated by Django 3.2.5 on 2021-07-26 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_auto_20210726_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialunit',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
