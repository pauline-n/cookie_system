from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity = models.FloatField()
    total_cost = models.FloatField()
    cost_per_unit = models.FloatField(blank=True, null= True)
    
    def save()