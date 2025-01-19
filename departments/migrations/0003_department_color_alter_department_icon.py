# Generated by Django 5.1.1 on 2025-01-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_department_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='color',
            field=models.CharField(default='#000', max_length=10),
        ),
        migrations.AlterField(
            model_name='department',
            name='icon',
            field=models.FileField(default=1, upload_to='departments/icons/'),
            preserve_default=False,
        ),
    ]
