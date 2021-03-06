# Generated by Django 2.1.5 on 2019-03-12 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_bollinger_band'),
    ]

    operations = [
        migrations.CreateModel(
            name='ATR',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('period', models.CharField(default='10', max_length=100)),
                ('interval', models.CharField(default='minute', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='Momentum_Indicator',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('period', models.CharField(default='14', max_length=100)),
                ('interval', models.CharField(default='minute', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='Money_Flow_Index',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('period', models.CharField(default='10', max_length=100)),
                ('interval', models.CharField(default='minute', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='Standard_Deviation',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('period', models.CharField(default='10', max_length=100)),
                ('interval', models.CharField(default='minute', max_length=100)),
                ('field', models.CharField(default='close', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='VWAP',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('interval', models.CharField(default='minute', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.RenameField(
            model_name='bollinger_band',
            old_name='standard_deviation',
            new_name='std',
        ),
        migrations.AlterField(
            model_name='bollinger_band',
            name='band_type',
            field=models.CharField(default='middle', max_length=100),
        ),
    ]
