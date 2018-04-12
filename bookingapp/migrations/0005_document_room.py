# Generated by Django 2.0.2 on 2018-04-06 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0004_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='room',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookingapp.Room'),
            preserve_default=False,
        ),
    ]