# Generated by Django 3.2.5 on 2021-07-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_portaluser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='portaluser',
            name='flat2',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
