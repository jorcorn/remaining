# Generated by Django 4.0b1 on 2021-11-11 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0013_rename_rate_rate_input_data_oxide_growth_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate_input_data',
            name='estimated_operating_temperature',
            field=models.FloatField(default=1000),
        ),
    ]
