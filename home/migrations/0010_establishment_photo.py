# Generated by Django 4.2.6 on 2023-12-04 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_service_slug_alter_service_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='photo',
            field=models.ImageField(null=True, upload_to='profile'),
        ),
    ]