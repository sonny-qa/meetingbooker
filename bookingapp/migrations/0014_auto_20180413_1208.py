# Generated by Django 2.0.2 on 2018-04-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0013_auto_20180413_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(help_text='Enter the address', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(help_text='Enter a venue name', max_length=200, null=True),
        ),
    ]