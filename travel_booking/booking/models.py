from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    available_seats = models.IntegerField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"
class TravelSystem(models.Model):
    MODE_CHOICES = [
        ('Flight', 'Flight'),
        ('Bus', 'Bus'),
        ('Train', 'Train'),
        ('Cab', 'Cab'),
    ]

    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=0)
    image = models.ImageField(upload_to='travel_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.mode}: {self.source} → {self.destination}"
class Travel(models.Model):
    name = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)  # e.g. Flight, Bus, Train, Cab
    price = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seats = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.mode})"