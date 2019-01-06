# Generated by Django 2.1.4 on 2019-01-06 14:33

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import economy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(db_index=True, default=economy.models.get_time)),
                ('modified_on', models.DateTimeField(default=economy.models.get_time)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None)),
                ('company', models.CharField(max_length=255)),
                ('github_profile', models.CharField(blank=True, default='', max_length=255)),
                ('expiry_date', models.DateTimeField()),
                ('apply_location', models.CharField(max_length=400)),
                ('paid_txid', models.CharField(blank=True, default='', max_length=255)),
                ('owner_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs', to='dashboard.Profile')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('annual_pay', models.IntegerField(blank=True, null=True)),
                ('contractor', models.BooleanField(default=False)),
                ('full_time', models.BooleanField(default=True)),
                ('internship', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
