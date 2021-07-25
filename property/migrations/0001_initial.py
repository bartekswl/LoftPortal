# Generated by Django 3.2.5 on 2021-07-25 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('flat_number', models.CharField(choices=[('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3')], max_length=4)),
            ],
        ),
    ]