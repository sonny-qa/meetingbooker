# Generated by Django 2.0.2 on 2018-04-15 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0014_auto_20180413_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='venue',
        ),
        migrations.RemoveField(
            model_name='room',
            name='venue',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]