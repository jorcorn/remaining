# Generated by Django 4.0b1 on 2021-11-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0015_remove_rate_input_data_estimated_operating_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='eot_input_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_op_temp', models.FloatField()),
            ],
        ),
    ]