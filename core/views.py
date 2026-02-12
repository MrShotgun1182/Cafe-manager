from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Order, OrderItem, MenuItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

# --- منوی مشتری ---
def menu_view(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        item_ids = request.POST.getlist('items')
        
        if item_ids and table_number:
            order = Order.objects.create(table_number=table_number)
            for item_id in item_ids:
                item = get_object_or_404(MenuItem, id=item_id)
                OrderItem.objects.create(order=order, item=item)
            return render(request, 'core/order_success.html', {'order': order})

    categories = Category.objects.all()
    return render(request, 'core/menu.html', {'categories': categories})

# --- ثبت سفارش حرفه‌ای (همراه با کوانتیتی و قیمت لحظه‌ای) ---
def submit_order(request):
    if request.method == "POST":
        table_number = request.POST.get('table_number')
        selected_item_ids = request.POST.getlist('items')

        if not selected_item_ids or not table_number:
            return redirect('menu')

        new_order = Order.objects.create(
            table_number=table_number,
            status='seen' # وضعیت پیش‌فرض
        )

        for item_id in selected_item_ids:
            item = get_object_or_404(MenuItem, id=item_id)
            quantity = request.POST.get(f'quantity_{item_id}', 1)
            
            if int(quantity) > 0:
                OrderItem.objects.create(
                    order=new_order,
                    item=item,
                    quantity=int(quantity),
                    price=item.price
                )

        return render(request, 'core/order_success.html', {'order': new_order})
    return redirect('menu')

# --- بخش مدیریت (Staff) ---
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='login')
def staff_dashboard(request):
    # این همون ویوی اصلی هست که کارمند اول بار باز می‌کنه
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'orders': orders})

# --- ویوی مخصوص HTMX (بدون رفرش صفحه) ---
@user_passes_test(is_staff, login_url='login')
def order_list_ajax(request):
    # دقیقاً همان منطق فیلتر داشبورد رو اینجا داریم
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today).order_by('-created_at')
    # فقط بخش لیست رو رندر می‌کنیم
    return render(request, 'core/includes/order_list_fragment.html', {'orders': orders})

@user_passes_test(is_staff, login_url='login')
def change_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    order.status = new_status
    order.save()
    # بعد از تغییر وضعیت، برمی‌گرده به داشبورد اصلی
    return redirect('staff_dashboard')