from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', views.menu_view, name='menu'),
    
    # داشبورد اصلی کارمندان
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # آدرس طلایی برای آپدیت لحظه‌ای لیست سفارشات با HTMX
    path('dashboard/orders-ajax/', views.order_list_ajax, name='order_list_ajax'),
    
    # تغییر وضعیت سفارش
    path('dashboard/change/<int:order_id>/<str:new_status>/', views.change_status, name='change_status'),
    
    # ثبت سفارش مشتری
    path('submit-order/', views.submit_order, name='submit_order'),
    
    # احراز هویت
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# نمایش فایل‌های مدیا (عکس محصولات) در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)