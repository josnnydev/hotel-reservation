from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type_room = models.CharField(max_length=100)
    price_room = models.DecimalField(max_digits=10, decimal_places=2)
    enable = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type_room} - {self.price_room} - {self.enable}'

class Bus(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price_bus = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


 
     

          

class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel} - {self.room.type_room} - {self.bus.name} - {self.price} - {self.check_in} - {self.check_out}'

    def save(self, *args, **kwargs):
        self.price = self.room.price_room + self.bus.price_bus
        super().save(*args, **kwargs)



