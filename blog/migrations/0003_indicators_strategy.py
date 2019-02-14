# Generated by Django 2.1.5 on 2019-02-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190201_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comparator', models.CharField(max_length=100)),
                ('indicator1', models.CharField(max_length=100)),
                ('indicator2', models.CharField(max_length=100)),
                ('instrument', models.CharField(max_length=100)),
            ],
        ),
    ]