from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=30)

    # Create a toString method for object string representation
    def __str__(self):
        return self.name + ": " + self.description

class CarModel(models.Model):
    car_models = [      # ↓ Displayed on Django Admin
        ('SEDAN', 'Sedan'),
        ('SUV', 'Sports Utility Vehicle'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealerId = models.IntegerField()
    carType = models.CharField(null=False, choices=car_models, max_length=30)
    year = models.DateField()

    # Create a toString method for object string representation
    def __str__(self):
        return self.year + " " + self.make + " "+ self.name + " " + self.carType

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
