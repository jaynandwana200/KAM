# Generated by Django 4.2.17 on 2024-12-28 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KAM', '0002_alter_kammail_kamid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kammail',
            name='KAMID',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
