# Generated by Django 4.2.6 on 2023-12-06 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ots_app', '0002_candidate_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='mobile',
        ),
    ]
