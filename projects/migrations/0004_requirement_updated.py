# Generated by Django 3.0.3 on 2020-04-23 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20200423_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
