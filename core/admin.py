from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

# ۱. مدیریت آیتم‌های منو
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    # نمایش ستون‌ها در لیست اصلی
    list_display = ('name', 'subtitle', 'price', 'category')
    # امکان ویرایش سریع قیمت و برچسب کوتاه از داخل لیست
    list_editable = ('subtitle', 'price')
    # قابلیت فیلتر کردن بر اساس دسته‌بندی
    list_filter = ('category',)
    # قابلیت جستجو در نام، برچسب و توضیحات
    search_fields = ('name', 'subtitle', 'description')
    
    # چیدمان فیلدها در صفحه ویرایش محصول
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'category', 'price', 'image')
        }),
        ('جزئیات نمایش', {
            'fields': ('subtitle', 'description'),
            'description': 'این فیلدها در منوی مشتری نمایش داده می‌شوند.'
        }),
    )

# ۲. مدیریت آیتم‌های داخل سفارش (بصورت اینلاین)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item',)

# ۳. مدیریت سفارشات
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'created_at', 'total_price_display')
    list_filter = ('status', 'created_at', 'table_number')
    search_fields = ('id', 'table_number')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    
    def total_price_display(self, obj):
        # محاسبه مجموع قیمت (با فرض اینکه هر آیتم فقط یک عدد است یا ضرب در تعداد شده است)
        total = sum(oi.item.price for oi in obj.order_items.all())
        return f"{total:,} تومان"

    total_price_display.short_description = "مبلغ کل"

# ۴. ثبت دسته‌بندی
admin.site.register(Category)