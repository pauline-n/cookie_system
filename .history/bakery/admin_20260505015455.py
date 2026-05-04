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
        return f"UGX {obj.cost_per_cookie():,.2f}"
    cost_per_cookie_display.short_description = "Cost per cookie"
    
# -----------
# productionbatch + packaging inline
# -----------
class PackagingInline(admin.TabularInline):
    model = Packaging
    extra = 1
    readonly_fields = ("total_cookies_used", "total_packaging_cost_display")
    fields = ("package_type", "quantity", "cookies_per_package", "packaging_cost", "total_cookies_used", "total_packaging_cost_display")
    
    def total_packaging_cost_display(self, obj):
        if obj.pk:
            return f"UGX {obj.total_packaging_cost():,.2f}"
        return "-"
    total_packaging_cost_display.short_description = "Total packaging cost"
    
@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = (
        "batch_label", "recipe", "cookies_produced",
        "utilities_cost", "labor_cost", "total_cost_display",
        "cost_per_cookie_display", "produced_at",
    )
    readonly_fields = ("total_cost", "cost_per_cookie_display", "produced_at")
    list_filter = ("recipe",)
    search_fields = ("recipe__cookie_type",)
    ordering = ("-produced_at",)
    inlines = [PackagingInline]
 
    def batch_label(self, obj):
        return str(obj)
    batch_label.short_description = "Batch"
 
    def total_cost_display(self, obj):
        return f"UGX {obj.total_cost:,.2f}"
    total_cost_display.short_description = "Total cost"
 
    def cost_per_cookie_display(self, obj):
        return f"UGX {obj.cost_per_cookie():,.2f}"
    cost_per_cookie_display.short_description = "Cost per cookie"
 
 
# ──────────────────────────────────────────
# Sale + SaleItem (inline)
# ──────────────────────────────────────────
 
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ("total_price_display",)
    fields = ("packaging", "quantity", "price_per_item", "total_price_display")
 
    def total_price_display(self, obj):
        if obj.pk:
            return f"UGX {obj.total_price():,.2f}"
        return "—"
    total_price_display.short_description = "Line total"
 
 
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name", "payment_method", "total_amount_display",
        "amount_paid_display", "balance_display", "payment_status", "created_at",
    )
    readonly_fields = ("total_amount", "balance_display", "created_at")
    list_filter = ("payment_method",)
    search_fields = ("customer_name",)
    ordering = ("-created_at",)
    inlines = [SaleItemInline]
 
    def total_amount_display(self, obj):
        return f"UGX {obj.total_amount:,.2f}"
    total_amount_display.short_description = "Total"
 
    def amount_paid_display(self, obj):
        return f"UGX {obj.amount_paid:,.2f}"
    amount_paid_display.short_description = "Paid"
 
    def balance_display(self, obj):
        bal = obj.balance()
        if bal > 0:
            return format_html('<span style="color:#c0392b;font-weight:500;">UGX {:,.2f}</span>', bal)
        return format_html('<span style="color:#27ae60;font-weight:500;">Settled</span>')
    balance_display.short_description = "Balance"
 
    def payment_status(self, obj):
        bal = obj.balance()
        if bal <= 0:
            return format_html('<span style="color:#27ae60;">&#10003; Paid</span>')
        elif obj.amount_paid > 0:
            return format_html('<span style="color:#e67e22;">&#9679; Partial</span>')
        return format_html('<span style="color:#c0392b;">&#9679; Unpaid</span>')
    payment_status.short_description = "Status"
 
 
# ──────────────────────────────────────────
# Customise the admin site header
# ──────────────────────────────────────────
 
admin.site.site_header = "Cookie Business Admin"
admin.site.site_title = "Cookie Admin"
admin.site.index_title = "Manage your cookie business"
 

# Register your models here.
# admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Packaging)
admin.site.register(ProductionBatch)
admin.site.register(Sale)
admin.site.register(SaleItem)