# Generated by Django 4.0.5 on 2022-07-21 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='published',
            new_name='publish',
        ),
    ]