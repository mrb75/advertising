# Generated by Django 4.0.6 on 2022-09-18 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_banned_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='banned_at',
            new_name='date_banned',
        ),
    ]