# Generated by Django 4.0b1 on 2021-11-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0009_alter_input_data_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='input_data',
            name='oxide_method',
            field=models.CharField(default='Customized growth rate', max_length=100),
        ),
        migrations.AlterField(
            model_name='input_data',
            name='material',
            field=models.CharField(default='T22 2.25Cr-1Mo', max_length=50),
        ),
    ]
