# Generated by Django 3.2.8 on 2021-11-01 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_alter_input_data_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_data',
            name='material',
            field=models.CharField(choices=[('1', 'T22 2.25Cr-1Mo'), ('2', 'Carbon Steel'), ('3', 'TP347H'), ('4', 'T1 Cr-Mo'), ('5', 'T2 0.5Cr-0.5Mo'), ('6', 'T12 1Cr-0.5Mo'), ('7', 'T11 1.25Cr-0.5Mo'), ('8', 'TP 321H'), ('9', 'TP 316H'), ('10', 'TP 304H'), ('11', 'T91 Cr-Mo-V'), ('12', 'T5 5Cr-0.5Mo')], default='T22 2.25Cr-1Mo', max_length=50),
        ),
    ]
