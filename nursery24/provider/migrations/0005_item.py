# Generated by Django 3.0.4 on 2020-03-19 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0004_auto_20200319_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics')),
                ('name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('category', models.CharField(choices=[('P', 'Plants'), ('S', 'Seeds'), ('F', 'Soils and Fertilizers'), ('D', 'Decor'), ('A', 'Accessories')], max_length=1)),
                ('rate', models.FloatField()),
                ('providers', models.ManyToManyField(to='provider.Provider')),
            ],
        ),
    ]
