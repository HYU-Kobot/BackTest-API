# Generated by Django 4.2 on 2023-04-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candle',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('acc_trade_price', models.DecimalField(decimal_places=10, max_digits=30)),
                ('acc_trade_volume', models.DecimalField(decimal_places=10, max_digits=30)),
                ('date_time_kst', models.DateTimeField()),
                ('exchange', models.CharField(max_length=255)),
                ('high_price', models.DecimalField(decimal_places=10, max_digits=30)),
                ('low_price', models.DecimalField(decimal_places=10, max_digits=30)),
                ('market', models.CharField(max_length=255)),
                ('opening_price', models.DecimalField(decimal_places=10, max_digits=30)),
                ('time_unit', models.CharField(max_length=255)),
                ('trade_price', models.DecimalField(decimal_places=10, max_digits=30)),
            ],
            options={
                'db_table': 'candle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HibernateSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_val', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hibernate_sequence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'member',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TradingKey',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('access_key', models.CharField(max_length=255)),
                ('market', models.CharField(max_length=255)),
                ('other', models.CharField(blank=True, max_length=255, null=True)),
                ('secret_key', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'trading_key',
                'managed': False,
            },
        ),
    ]
