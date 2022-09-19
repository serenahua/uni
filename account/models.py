from django.db import models
from django.utils import timezone


class ExpenseItem(models.Model):
    name = models.CharField(max_length=128)
    chicken = models.BooleanField()
    hot_pot = models.BooleanField()
    home = models.BooleanField()


class ChickenIncome(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    volume = models.PositiveSmallIntegerField()
    value = models.PositiveSmallIntegerField()
    remark = models.TextField(blank=True)


class ChickenExpense(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(ExpenseItem, on_delete=models.SET_NULL, null=True)
    value = models.PositiveSmallIntegerField()
    remark = models.TextField(blank=True)


class HotPotIncome(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    value = models.PositiveSmallIntegerField()
    remark = models.TextField(blank=True)


class HotPotExpense(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(ExpenseItem, on_delete=models.SET_NULL, null=True)
    value = models.PositiveSmallIntegerField()
    remark = models.TextField(blank=True)


class HomeExpense(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(ExpenseItem, on_delete=models.SET_NULL, null=True)
    value = models.PositiveSmallIntegerField()
    remark = models.TextField(blank=True)

