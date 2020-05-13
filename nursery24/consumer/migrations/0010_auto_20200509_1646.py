# Generated by Django 3.0.5 on 2020-05-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0009_auto_20200504_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_placed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='date_delivered',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='expected_delivery_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='last_tracked_on',
            field=models.DateTimeField(null=True),
        ),
    ]
