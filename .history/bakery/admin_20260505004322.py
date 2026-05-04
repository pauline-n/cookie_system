from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Packaging, ProductionBatch, Sale, SaleItem


# ---------------------
# Ingredient
# ---------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "unit", "total_cost", "cost_per_unit_display")
    list_filter = ("unit",)
    search_fields = ("name",)
    readonly_fields = ("cost_per_unit",)
    ordering = ("name",)
    
    def cost_per_unit_display(self, obj):
        if obj.cost_per_unit is not None:
            return f"Ugx {obj.cost_per_unit:,.2f}"
        return "-"
    cost_per_unit_display

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Packaging)
admin.site.register(ProductionBatch)
admin.site.register(Sale)
admin.site.register(SaleItem)