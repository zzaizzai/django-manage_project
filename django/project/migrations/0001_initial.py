# Generated by Django 4.1.4 on 2023-11-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('user_created', models.IntegerField()),
                ('user_completed', models.IntegerField()),
                ('text', models.TextField()),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_completed', models.DateTimeField()),
                ('datetime_updated', models.DateTimeField(auto_now_add=True)),
                ('date_due', models.DateField()),
                ('datetime_cancled', models.DateTimeField()),
                ('is_canceled', models.BooleanField()),
                ('is_completed', models.BooleanField()),
            ],
            options={
                'db_table': 'projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectMemeber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('is_manager', models.BooleanField()),
            ],
            options={
                'db_table': 'project_member',
            },
        ),
    ]
