# Generated by Django 4.1.4 on 2023-11-16 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_masterdepartment_customuser_department_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MasterDepartment',
        ),
    ]
