# Generated by Django 3.0.4 on 2020-03-19 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0002_consumer_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=100, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
    ]
