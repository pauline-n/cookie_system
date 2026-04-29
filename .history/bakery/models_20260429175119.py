from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity = models.FloatField()
    total_cost = models.FloatField()
    cost_per_unit = models.FloatField(blank=True, null= True)
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.cost_per_unit = self.total_cost / self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    cookie_type = models.CharField(max_length=100)
    cookies_produced = models.IntegerField()
    total_cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_cost(self):
        total = 0
        for item in self.ingredients.all():
            total == item.cost
        self.total_cost = total
        return total