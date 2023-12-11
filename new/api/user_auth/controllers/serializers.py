from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from database_model.models import User


# serializer with no token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'is_staff', 'account_type',
                  'is_email_activated',]


# user serializer with token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'is_staff', 'account_type',
                  'is_email_activated', 'token', ]

        def get_token(self, obj):
            token = RefreshToken.for_user(obj)
            return str(token)
