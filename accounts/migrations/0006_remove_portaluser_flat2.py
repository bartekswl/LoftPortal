# Generated by Django 3.2.5 on 2021-07-27 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_portaluser_flat2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portaluser',
            name='flat2',
        ),
    ]
