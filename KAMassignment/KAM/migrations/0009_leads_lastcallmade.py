# Generated by Django 4.2.17 on 2024-12-26 01:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('KAM', '0008_alter_leads_callfrequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='lastCallMade',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
