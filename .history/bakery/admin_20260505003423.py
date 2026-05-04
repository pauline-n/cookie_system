from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Packaging, ProductionBatch, Sale, SaleItem


# ---------------------
# Ingredient
# ---------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "unit", "total_cost", "cost_per_unit")

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Packaging)
admin.site.register(ProductionBatch)
admin.site.register(Sale)
admin.site.register(SaleItem)