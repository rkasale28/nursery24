# Generated by Django 3.0.5 on 2020-04-29 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider', '0004_auto_20200428_1808'),
        ('courier', '0003_auto_20200428_1808'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('profile_pic', models.ImageField(default='dps/profile.png', upload_to='dps/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('secondary_id', models.CharField(max_length=8)),
                ('date_placed', models.DateField(null=True)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('consumer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='provider.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('D', 'Delivered'), ('S', 'Shipped'), ('P', 'Placed'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('expected_delivery_date', models.DateField(null=True)),
                ('date_delivered', models.DateField(null=True)),
                ('date_last_tracked', models.DateField(null=True)),
                ('last_tracked_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='courier.Courier')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Order')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='provider.Product')),
                ('provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='provider.Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.TextField(max_length=100, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
    ]
