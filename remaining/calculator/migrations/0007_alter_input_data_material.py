# Generated by Django 3.2.8 on 2021-11-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0006_auto_20211101_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_data',
            name='material',
            field=models.CharField(max_length=50),
        ),
    ]
