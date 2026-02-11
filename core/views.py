from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Order, OrderItem, MenuItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def menu_view(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        item_ids = request.POST.getlist('items')
        
        if item_ids and table_number:
            order = Order.objects.create(table_number=table_number)
            
            for item_id in item_ids:
                from .models import MenuItem
                item = MenuItem.objects.get(id=item_id)
                OrderItem.objects.create(order=order, item=item)

            return render(request, 'core/order_success.html', {'order': order})

    categories = Category.objects.all()
    return render(request, 'core/menu.html', {'categories': categories})

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='login')
def staff_dashboard(request):
    # گرفتن تاریخ امروز
    today = timezone.now().date()
    # فیلتر کردن سفارش‌هایی که امروز ثبت شده‌اند (به ترتیب جدیدترین)
    orders = Order.objects.filter(created_at__date=today).order_by('-created_at')
    
    return render(request, 'core/dashboard.html', {'orders': orders})

def change_status(request, order_id, new_status):
    # تابعی برای تغییر سریع وضعیت سفارش
    order = get_object_or_404(Order, id=order_id)
    order.status = new_status
    order.save()
    return redirect('staff_dashboard')

def submit_order(request):
    if request.method == "POST":
        # ۱. گرفتن شماره میز از مودال
        table_number = request.POST.get('table_number')
        
        # ۲. گرفتن لیست ID محصولاتی که تیک خورده‌اند
        selected_item_ids = request.POST.getlist('items')

        if not selected_item_ids or not table_number:
            return redirect('menu') # اگر چیزی انتخاب نکرده بود برگردد به منو

        # ۳. ساخت رکورد اصلی سفارش (Order)
        new_order = Order.objects.create(
            table_number=table_number,
            status='seen'  # وضعیت اولیه: دریافت شده
        )

        # ۴. ثبت تک‌تک آیتم‌های سفارش در جدول واسط (OrderItem)
        for item_id in selected_item_ids:
            item = get_object_or_404(MenuItem, id=item_id)
            
            # پیدا کردن تعداد انتخاب شده برای این محصول خاص
            quantity = request.POST.get(f'quantity_{item_id}', 1)
            
            if int(quantity) > 0:
                OrderItem.objects.create(
                    order=new_order,
                    item=item,
                    quantity=int(quantity),
                    price=item.price  # ذخیره قیمت لحظه‌ای
                )

        # ۵. نمایش صفحه موفقیت به مشتری
        return render(request, 'core/order_success.html', {'order': new_order})

    return redirect('menu')

