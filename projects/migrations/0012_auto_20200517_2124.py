# Generated by Django 3.0.3 on 2020-05-17 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_requirementview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.Requirement'),
        ),
    ]
