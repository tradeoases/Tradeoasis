from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.master_dashboard.controllers.serializers import ShowRoomSerializer
from database_model.models import ShowRoom, AuditTrail


@api_view(['GET'])
def show_room_list(request):
    try:
        profiles = ShowRoom.objects.all()
        serializer = ShowRoomSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)



# DELETE SHOW ROOM
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_show_room(request, pk):
    try:
        user  = request.user
        show_room_detail = ShowRoom.objects.get(id=pk)
        AuditTrail.objects.create(
            user=user,
            action=user.last_name + ' - ' + user.last_name +' deleted show room' + 'at ' + str(
                datetime.datetime.now())
        )
        show_room_detail.delete()
        return Response('show room has been deleted deleted successfully', status=status.HTTP_200_OK)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)


# UPDATE SHOW ROOM
@api_view(['PUT'])
def update_show_room(request, pk):
    try:
        user = request.user
        show_room_data = ShowRoom.objects.filter(id=pk).update()
        serializer = ShowRoomSerializer(instance=show_room_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = {'detail': 'Some thing went wrong please contact admin'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as p:
        print(str(p))
        return Response('Not found 404', status=status.HTTP_404_NOT_FOUND)