# Generated by Django 3.0.4 on 2020-03-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='verification_status',
            field=models.BooleanField(default=False),
        ),
    ]
