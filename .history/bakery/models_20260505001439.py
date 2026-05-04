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
            total += item.cost
        self.total_cost = total
        return total
    
    def cost_per_cookie(self):
        if self.cookies_produced > 0:
            return self.total_cost / self.cookies_produced
        return 0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_cost()
        super().save(update_fields = ['total_cost'])
        
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredient", on_delete=models.CASCADE)
    
    quantity_used = models.FloatField()
    
    @property
    def cost(self):
        return self.quantity_used * self.ingredient.cost_per_unit
    
    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity_used}"
    
class ProductionBatch(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    cookies_produced = models.IntegerField()
    
    utilities_cost = models.FloatField(default=0)
    labor_cost = models.FloatField(default=0)
    
    total_cost = models.FloatField(default=0)
    produced_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_total_cost(self):
        self.total_cost = (
            self.recipe.total_cost + self.utilities_cost + self.labor_cost
        )
        return self.total_cost
    
    def cost_per_cookie(self):
        if self.cookies_produced > 0:
            return self.total_cost / self.cookies_produced
        return 0
    
    def save(self, *args, **kwargs):
        self.calculate_total_cost()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.recipe.cookie_type} Batch"
    
    
class Packaging(models.Model):
    PACKAGE_CHOICES = (
        ("zipper", "Zipper Bag"),
        ("tin", "Tin"),
    )
    
    production_batch = models.ForeignKey(
        ProductionBatch, on_delete=models.CASCADE,
        related_name="packages"
    )
    
    package_type = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES
    )
    
    quantity = models.IntegerField()
    cookies_per_package = models.IntegerField()
    packaging_cost = models.FloatField(default=0)
    
    def total_cookies_used(self):
        return self.quantity *  self.cookies_per_package
    
    def total_packaging_cost(self):
        return self.quantity * self.packaging_cost
    
    def __str__(self):
        return f"{self.package_type} - {self.quantity}"
    
class Sale(models.Model):
    PAYMENT_CHOICES = (
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
        ("credit", "Credit")
    )
    
    customer_name = models.CharField(max_length=100)
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
        )
    amount_paid = models.FLoatField(default=0)
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_total(self):
        total=0
        for item in self.items.all():
            total += item.total_price()
        self.total_amount = total
        return total
    
    def balance(self):
        return self.total_amount - self.amount_paid
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total()
        super().save(update_fields=["total_amount"])
        
    def __str__(self):
        return f"{self.customer_name} - {self.total_amount}"
    
class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )
    
    packaging = models.ForeignKey(
        Packaging,
        on_delete=models.CASCADE
    )
    
    quantity = models.IntegerField()
    price_per_item = models.FloatField()
    
    def total_price(self):
        return self.quantity * self.price_per_item
    
    def __str__(self):
        return f"{self.packag}"