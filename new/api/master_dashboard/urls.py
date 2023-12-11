from django.urls import path, include

from api.master_dashboard.controllers.showrooms import show_room_list, delete_show_room, update_show_room
from api.user_auth.controllers.authenticate import delete_user_account
from api.vendor.controllers.business_profile import business_profile_list

app_name = 'master_dashboard'

urlpatterns = [
    path('', include('api.shared.urls')),
    path('user_account/delete/<str:pk>/', delete_user_account, name='user_account_delete'),
    path('business_profile_list/', business_profile_list, name='business_profile_list'),
    path('show_room_list/', show_room_list, name='show_room_list'),
    path('show_room/delete/<str:pk>/', delete_show_room, name='delete_show_room'),
    path('show_room/update/<str:pk>/', update_show_room, name='update_show_room'),



]
