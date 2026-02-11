from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # تغییر این خط: چون price در OrderItem وجود ندارد، آن را از readonly_fields حذف می‌کنیم
    readonly_fields = ('item',) 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'created_at', 'total_price_display')
    list_filter = ('status', 'created_at', 'table_number')
    search_fields = ('id', 'table_number')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    
    def total_price_display(self, obj):
        # محاسبه مجموع قیمت آیتم‌ها از طریق مدل MenuItem
        total = sum(oi.item.price for oi in obj.order_items.all())
        return f"{total:,} تومان"

    total_price_display.short_description = "مبلغ کل"

admin.site.register(MenuItem)
admin.site.register(Category)