# Generated by Django 5.1.1 on 2025-01-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_department_color_alter_department_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
