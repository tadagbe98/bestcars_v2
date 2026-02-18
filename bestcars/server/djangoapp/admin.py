from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'state', 'st')
    list_filter = ('state',)
    search_fields = ('full_name', 'city')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealer', 'sentiment', 'purchase', 'created_at')
    list_filter = ('sentiment', 'purchase')

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'car_type', 'year')
    list_filter = ('car_type', 'car_make')
