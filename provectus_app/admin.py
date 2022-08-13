from django.contrib import admin
from provectus_app.models import *


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    fields = ['my_user_id', 'first_name', 'last_name', 'births', 'user_image_path']


@admin.register(LastUpdate)
class LastUpdateAdmin(admin.ModelAdmin):
    fields = ['last_update']
