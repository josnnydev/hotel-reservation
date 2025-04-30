from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
 
from .models import Hotel, Room, Reservation, Bus
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
 
 
 


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

            

class HotelApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user = request.user
        hotel = Hotel.objects.filter(user=user).first()
        
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)


class RoomEnable(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        rooms = Room.objects.filter(enable=True, user=user)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

class  CreateReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
         
        room = get_object_or_404(Room, id=data['room_id'], user=user)
        bus = get_object_or_404(Bus, id=data['bus_id'], user=user)

        check_in = data['check_in']
        check_out = data['check_out']
        price =  data['price']
        if not check_in or not check_out:
            return Response({'error': 'check_in and check_out are required'}, status=status.HTTP_400_BAD_REQUEST)

        Reservation.objects.create(  room=room, bus=bus, check_in=check_in, check_out=check_out, price=price, user=user)
         
        room.enable = False
        room.save() 
        return Response({'message': 'Room disabled successfully', 'room': room.type_room, 'bus': bus.name, 'total': price, 'check_in': check_in, 'check_out': check_out}, status=status.HTTP_200_OK)

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
    

class ReservationClientBus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        bus = get_object_or_404(Bus, id=request.data['bus_id'], user=user)
        reservations = Reservation.objects.filter(bus=bus, user=user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)