from django.urls import path, include

from api.front_shop.controllers import main_shop
from api.master_dashboard.controllers.showrooms import show_room_list

app_name = 'front_shop'

urlpatterns = [
    path('', include('api.shared.urls')),
    path('show_room_list/', show_room_list, name='show_room_list'),

]
