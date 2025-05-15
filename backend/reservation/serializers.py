from rest_framework import serializers
from .models import Hotel, Room, Reservation, Bus
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Serializeer para el registro de usuarios
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key


#serializer para el hotel
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

#serializer para la habitación
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


#serializer para la reserva
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'hotel', 'room', 'bus', 'check_in', 'check_out', 'price']


 

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'        