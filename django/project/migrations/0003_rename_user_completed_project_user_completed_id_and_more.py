# Generated by Django 4.1.4 on 2023-11-13 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_project_date_due_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user_completed',
            new_name='user_completed_id',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='user_created',
            new_name='user_created_id',
        ),
    ]