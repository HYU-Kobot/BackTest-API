# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Candle(models.Model):
    id = models.BigAutoField(primary_key=True)
    acc_trade_price = models.DecimalField(max_digits=30, decimal_places=10)
    acc_trade_volume = models.DecimalField(max_digits=30, decimal_places=10)
    date_time_kst = models.DateTimeField()
    exchange = models.CharField(max_length=255)
    high_price = models.DecimalField(max_digits=30, decimal_places=10)
    low_price = models.DecimalField(max_digits=30, decimal_places=10)
    market = models.CharField(max_length=255)
    opening_price = models.DecimalField(max_digits=30, decimal_places=10)
    time_unit = models.CharField(max_length=255)
    trade_price = models.DecimalField(max_digits=30, decimal_places=10)

    class Meta:
        managed = False
        db_table = 'candle'


class HibernateSequence(models.Model):
    next_val = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hibernate_sequence'


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'member'


class TradingKey(models.Model):
    id = models.BigAutoField(primary_key=True)
    access_key = models.CharField(max_length=255)
    market = models.CharField(max_length=255)
    other = models.CharField(max_length=255, blank=True, null=True)
    secret_key = models.CharField(max_length=255)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trading_key'
