# Generated by Django 5.1.1 on 2025-02-07 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_connection_name_alter_connection_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='connection_type',
            field=models.CharField(blank=True, choices=[('mysql', 'MYSQL'), ('oracle', 'ORACLE')], default='oracle', max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='ConnectionType',
        ),
    ]
