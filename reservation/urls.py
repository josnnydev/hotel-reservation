 
 
from django.urls import path
from .views import HotelApiView, RoomEnable, CreateReservation, ListClientsInfo, Checkout, ReservationClientBus, RegisterView
 


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('hotel/', HotelApiView.as_view()),
    path('room/enable/', RoomEnable.as_view()),
    path('create-reservation/', CreateReservation.as_view()),
    path('list-clients-info/', ListClientsInfo.as_view()),
    path('checkout/', Checkout.as_view()),
    path('reservation-client-bus/', ReservationClientBus.as_view()),
    
]
