# Generated by Django 2.1.2 on 2018-12-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='annual_pay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='contractor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='full_time',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='internship',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='job_location',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]