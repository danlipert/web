# Generated by Django 2.1.2 on 2018-12-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_auto_20181225_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_location',
        ),
        migrations.AlterField(
            model_name='job',
            name='apply_location',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
