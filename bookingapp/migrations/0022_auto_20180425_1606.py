# Generated by Django 2.0.2 on 2018-04-25 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0021_auto_20180419_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='venue',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingapp.Venue'),
        ),
    ]
