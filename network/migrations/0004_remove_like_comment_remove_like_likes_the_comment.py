# Generated by Django 4.1.1 on 2022-10-21 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_options_alter_profil_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='like',
            name='likes_the_comment',
        ),
    ]