# Generated by Django 5.1.1 on 2025-01-27 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0004_department_slug'),
        ('reports', '0007_alter_chartaxis_axis'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='width',
            field=models.CharField(choices=[(3, 3), (2, 2), (4, 4), (6, 6)], default=3, max_length=10),
        ),
        migrations.AlterField(
            model_name='chart',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='charts', to='reports.report'),
        ),
        migrations.AlterField(
            model_name='report',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='departments.department'),
        ),
    ]
