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
    cost_per_unit_display.short_description = "Cost Per Unit"

# ---------
# recipe and recipe ingredient
# ---------
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    readonly_fields = ("cost_display",)
    fields = ("ingredient", "quantity_used", "cost_display")
    
    def cost_display(self, obj):
        if obj.pk:
            return f"UGX {obj.cost:,.2f}"
        return "-"
    cost_display.short_description = "Line cost"
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("cookie_type", "cookies_produced", "total_cost_display", "cost_per_cookie_display", "created_at")
    readonly_fields = ("total_cost", "cost_per_cookie_display", "created_at")
    search_fields = ("cookie_type",)
    ordering = ("-created_at",)
    inlines = [RecipeIngredientInline]
    
    def total_cost_display(self, obj):
        return f"UGX {obj.total_cost:,.2f}"
    total_cost_display.short_description = "Ingredient cost"
    
    def cost_per_cookie_display(self, obj):
        

# Register your models here.
# admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Packaging)
admin.site.register(ProductionBatch)
admin.site.register(Sale)
admin.site.register(SaleItem)