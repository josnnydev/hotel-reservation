from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room, Reservation, Bus
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer, BusSerializer
from django.shortcuts import get_object_or_404 
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import render 
from rest_framework.authtoken.models import Token



 
    

    
 
#api get que hace llamada a la base de datos y devuelve los hoteles, habitaciones y buses
class getHotelsRoomsBuses(APIView):
    
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        hotels = Hotel.objects.all()
        rooms = Room.objects.all()
        buses = Bus.objects.all()

        return Response({
            "hotels": HotelSerializer(hotels, many=True).data,
            "rooms": RoomSerializer(rooms, many=True).data,
            "buses": BusSerializer(buses, many=True).data,
        })


#api post que recibe los datos del registro de un nuevo usuario y devuelve un token
class RegisterAndRedirect(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#api get que devuelve la información del hotel
class HotelApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        hotel = Hotel.objects.first()
        
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

#api get que devuelve la información de las habitaciones habilitadas
class RoomEnable(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.filter(enable=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
#api post que recibe los datos de la reserva y crea una nueva reserva
class CreateReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        
        room = get_object_or_404(Room, id=data['type_room'])   
        bus = get_object_or_404(Bus, id=data['name'])   
        hotel = get_object_or_404(Hotel, id=data['hotel'])   

        check_in = data['check_in']
        check_out = data['check_out']
        price = room.price_room + bus.price_bus
        
        if not check_in or not check_out:
            return Response({'error': 'check_in and check_out are required'}, status=status.HTTP_400_BAD_REQUEST)

        reservation = Reservation.objects.create(
            hotel=hotel,
            room=room,
            bus=bus,
            check_in=check_in,
            check_out=check_out,
            price=price,
            user=user
        )
        
        room.enable = False
        room.save() 
        
        return Response({
            'message': 'Room disabled successfully',
            'hotel': hotel.name,
            'room': room.type_room,
            'bus': bus.name,
            'total': price,
            'check_in': check_in,
            'check_out': check_out
        }, status=status.HTTP_200_OK)

#api get que devuelve la información de las reservas del usuario
class ListClientsInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reservations = Reservation.objects.select_related('room', 'user', 'bus').filter(user=user)
        data = [
           {
            'user': r.user.username,
            'room': r.room.type_room,
            'bus': r.bus.name,
            'check_in': r.check_in,
            'check_out': r.check_out
           } 
           for r in reservations
        ]
        return Response(data)

#api post que recibe los datos de la reserva y elimina la reserva
class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        reservation = get_object_or_404(Reservation, id=data['reservation_id'], user=user)
        reservation.room.enable = True
        reservation.room.save()
        reservation.delete()
        return Response({'message': 'Room enabled successfully'}, status=status.HTTP_200_OK)        
    
#api post que recibe los datos de la reserva y devuelve la información de las reservas del usuario
class ReservationClientBus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        bus = get_object_or_404(Bus, id=request.data['bus_id'], user=user)
        reservations = Reservation.objects.filter(bus=bus, user=user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)