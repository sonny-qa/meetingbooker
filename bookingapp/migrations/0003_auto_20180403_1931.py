# Generated by Django 2.0.2 on 2018-04-03 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0002_auto_20180312_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venue',
            options={'permissions': (('can_edit_venue', 'Edit a venue details'),)},
        ),
    ]