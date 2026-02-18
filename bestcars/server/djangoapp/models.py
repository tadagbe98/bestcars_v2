from django.db import models
from django.contrib.auth.models import User


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'), ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'), ('VAN', 'Van'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(default=2023)

    def __str__(self):
        return f"{self.car_make.name} {self.name} {self.year}"


class Dealer(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=5)
    zip_code = models.CharField(max_length=20)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def __str__(self):
        return self.full_name

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "st": self.st,
            "zip": self.zip_code,
            "lat": self.lat,
            "long": self.lng,
        }


class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} for {self.dealer.full_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "dealership": self.dealer.id,
            "name": self.name,
            "review": self.review,
            "purchase": self.purchase,
            "purchase_date": str(self.purchase_date) if self.purchase_date else "",
            "car_make": self.car_make,
            "car_model": self.car_model,
            "car_year": self.car_year,
            "sentiment": self.sentiment,
        }
