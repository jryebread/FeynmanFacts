# Generated by Django 3.1.5 on 2021-02-13 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_postlikescount_userpostlikes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpostlikes',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='userpostlikes',
            old_name='user_id',
            new_name='user',
        ),
    ]