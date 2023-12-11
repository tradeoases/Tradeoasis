from rest_framework import serializers

from database_model.models import ShowRoom


class ShowRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowRoom
        fields = '__all__'
