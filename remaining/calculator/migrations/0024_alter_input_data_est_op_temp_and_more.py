# Generated by Django 4.0b1 on 2021-11-16 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0023_alter_input_data_est_op_temp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_data',
            name='est_op_temp',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='input_data',
            name='oxide_growth_rate',
            field=models.FloatField(default=0),
        ),
    ]
