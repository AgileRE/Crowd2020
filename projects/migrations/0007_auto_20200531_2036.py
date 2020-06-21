# Generated by Django 3.0.3 on 2020-05-31 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200531_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='category',
            field=models.CharField(blank=True, choices=[('System Functional', 'System Functional'), ('System Non-functional', 'System Non-functional'), ('User Requirement', 'User Requirement')], max_length=30),
        ),
    ]