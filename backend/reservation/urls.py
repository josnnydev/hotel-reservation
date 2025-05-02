 
 
from django.urls import path
from .views import HotelApiView, RoomEnable, CreateReservation, ListClientsInfo, Checkout, ReservationClientBus,  Index, RegisterAndRedirect, getHotelsRoomsBuses
from django.conf import settings
from django.conf.urls.static import static
    


urlpatterns = [
    path('register/', RegisterAndRedirect.as_view(), name='register'),
    path('hotel/', HotelApiView.as_view()),
    path('room/enable/', RoomEnable.as_view()),
    path('create-reservation/', CreateReservation.as_view()),
    path('list-clients-info/', ListClientsInfo.as_view()),
    path('checkout/', Checkout.as_view()),
    path('reservation-client-bus/', ReservationClientBus.as_view()),
    path('get-hotels-rooms-buses/', getHotelsRoomsBuses.as_view()),


    path('', Index, name='index'),
    
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
