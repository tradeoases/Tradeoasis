import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from api.user_auth.controllers.serializers import UserSerializerWithToken, UserSerializer
from database_model.models import User, AuditTrail


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        # data['id'] = self.user.id
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# GET USER PROFILE
@api_view(['GET'])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user_account(request, pk):
    try:
        user = User.objects.get(id=pk)

        AuditTrail.objects.create(
            user=user,
            action=user.last_name + ' - ' + user.last_name +
                   ' with email ' + user.email + 'has deleted account permanently'
                   + 'at ' + str(
                datetime.datetime.now())
        )
        user.delete()
        return Response('Account permanently deleted successfully', status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)
