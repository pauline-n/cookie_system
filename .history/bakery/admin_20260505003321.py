from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Packaging, ProductionBatch, Sale, SaleItem


# ---------------------
# Ingredient
# ---------------------
@admin.register(Ingredient)

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Packaging)
admin.site.register(ProductionBatch)
admin.site.register(Sale)
admin.site.register(SaleItem)