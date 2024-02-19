from rest_framework import serializers
from .models import Stuff

class StuffSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ("id","owner","name","description","created_at")
    model = Stuff