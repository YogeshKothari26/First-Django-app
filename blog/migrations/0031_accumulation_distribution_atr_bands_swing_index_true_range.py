# Generated by Django 2.1.5 on 2019-03-19 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_strategy_group_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accumulation_Distribution',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('interval', models.CharField(default='minute', max_length=100)),
                ('use_volume', models.CharField(default='Yes', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='ATR_bands',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('period', models.CharField(default='5', max_length=100)),
                ('interval', models.CharField(default='minute', max_length=100)),
                ('shift', models.CharField(default='3', max_length=100)),
                ('field', models.CharField(default='close', max_length=100)),
                ('band_type', models.CharField(default='upper', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='Swing_Index',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('interval', models.CharField(default='day', max_length=100)),
                ('limit_move_value', models.CharField(default='0.5', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
        migrations.CreateModel(
            name='True_Range',
            fields=[
                ('indicator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Indicator')),
                ('interval', models.CharField(default='minute', max_length=100)),
            ],
            bases=('blog.indicator',),
        ),
    ]
