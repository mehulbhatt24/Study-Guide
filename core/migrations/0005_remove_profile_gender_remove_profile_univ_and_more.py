# Generated by Django 4.1.4 on 2023-01-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_images_profile_address_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='univ',
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='blank.webp', upload_to='Profile_images'),
        ),
    ]
