from rest_framework.serializers import Serializer, ModelSerializer
from .models import *


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = UserData
        fields = ['my_user_id', 'first_name', 'last_name', 'births', 'user_image_path']
