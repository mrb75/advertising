# Generated by Django 4.0.6 on 2022-09-18 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_banned_at_user_date_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='negetive_score',
            field=models.IntegerField(default=0),
        ),
    ]
