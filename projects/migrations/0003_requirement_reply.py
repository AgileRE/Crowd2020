# Generated by Django 3.0.3 on 2020-04-23 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='projects.Requirement'),
        ),
    ]
