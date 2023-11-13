# Generated by Django 4.1.4 on 2023-11-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_due',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='datetime_cancled',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='datetime_completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_cancled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='user_completed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='projectmemeber',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]
