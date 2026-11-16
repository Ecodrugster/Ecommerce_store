from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'phone_number', 'delivery_method', 'status')
    list_filter = ('delivery_method',)
    search_fields = ('user_name', 'phone_number')
    inlines = (OrderItemInline,)
