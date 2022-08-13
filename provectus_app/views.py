from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .serializers import *
from .models import *
from .csv_processor import update_data
from django.db.models import Avg


class DataListView(ListAPIView):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        return UserData.objects.all().exclude(my_user_id='')

    def post(self, request, *args, **kwargs):
        update_data()
        return HttpResponse('updated')


class AverageAgeView(APIView):
    def get(self, request, *args, **kwargs):
        image_filter = self.request.GET.get('is_image_exists')
        min_age_filter = self.request.GET.get('min_age')
        max_age_filter = self.request.GET.get('max_age')
        queryset = UserData.objects.all().exclude(my_user_id='')
        if image_filter is not None:
            if image_filter == 'True':
                queryset = queryset.filter(user_image_path__isnull=False)
            elif image_filter == 'False':
                queryset = queryset.filter(user_image_path__isnull=True)
        if min_age_filter is not None:
            queryset = queryset.filter(births__gte=int(min_age_filter))
        if max_age_filter is not None:
            queryset = queryset.filter(births__lte=int(max_age_filter))
        if queryset:
            avg_age = queryset.aggregate(Avg('births')).get('births__avg')
            return HttpResponse(f'{avg_age}, queryset length: {len(queryset)}, '
                                f'FILTERS: '
                                f'is_image_exists: {image_filter}, '
                                f'min_age: {min_age_filter}, '
                                f'max_age: {max_age_filter}')
        else:
            return HttpResponse('Filter returned no objects')
