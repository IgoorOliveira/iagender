# Generated by Django 4.2.6 on 2023-11-20 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_closeinterval_interval_close_interval_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interval',
            old_name='close_Interval',
            new_name='close_interval',
        ),
        migrations.RenameField(
            model_name='interval',
            old_name='initial_nterval',
            new_name='initial_interval',
        ),
    ]
