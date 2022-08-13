from django.db import models
from datetime import datetime


class UserData(models.Model):
    my_user_id = models.CharField(max_length=124, blank=True, null=True, verbose_name='id from the data')
    first_name = models.CharField(max_length=124, blank=True, null=True, verbose_name='first name')
    last_name = models.CharField(max_length=124, blank=True, null=True, verbose_name='last name')
    births = models.IntegerField(blank=True, null=True, verbose_name='birth seconds')
    user_image_path = models.CharField(max_length=124, blank=True, null=True, verbose_name='path to the image file')


class LastUpdate(models.Model):
    last_update = models.DateTimeField(default=datetime(year=1971, month=1, day=1), verbose_name='last db update')
