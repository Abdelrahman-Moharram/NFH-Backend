# Generated by Django 5.1.1 on 2025-01-17 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_schema_created_by_remove_schema_deleted_by_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Status',
        ),
    ]
