# Generated by Django 3.2.1 on 2021-08-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gms_admin', '0003_final_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(),
        ),
    ]
