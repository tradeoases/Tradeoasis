import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

# GET BUSINESS PROFILE
from api.vendor.controllers.serializers import BusinessProfileSerializer
from database_model.models import BusinessProfile, User, AuditTrail


# GET PROFILE
@api_view(['GET'])
def get_business_profile(request, pk):
    try:
        user = User.objects.get(id=pk)
        profile = BusinessProfile.objects.get(user=user.id)
        serializer = BusinessProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)


# GET ALL BUSINESS PROFILES ADMIN TASK
@api_view(['GET'])
def business_profile_list(request):
    try:
        profiles = BusinessProfile.objects.all()
        serializer = BusinessProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)


# UPDATE BUSINESS PROFILES
@api_view(['PUT'])
def update_business_profile(request, pk):
    try:
        user = User.objects.get(id=pk)
        profile_data = BusinessProfile.objects.filter(user=user.id).update()
        serializer = BusinessProfileSerializer(instance=profile_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = {'detail': 'Some thing went wrong please contact admin'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)


# DELETE BUSINESS PROFILE
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_business_profile(request, pk):
    try:
        user = User.objects.get(id=pk)
        profile = BusinessProfile.objects.get(user=user.id)
        AuditTrail.objects.create(
            user=user,
            action=user.last_name + ' - ' + user.last_name +
                   ' with email ' + user.email + 'has deleted business profile of '
                   + profile.business_name + 'at ' + str(
                datetime.datetime.now())
        )
        profile.delete()
        return Response('Business profile deleted successfully', status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)
