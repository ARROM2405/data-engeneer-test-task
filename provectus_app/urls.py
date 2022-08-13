from django.urls import path
from .views import *


urlpatterns = [
    path('data/', DataListView.as_view(), name='data'),
    path('stats/', AverageAgeView.as_view(), kwargs={'is_image_exists': None, 'min_age': None, 'max_age': None},
         name='stats')
]
