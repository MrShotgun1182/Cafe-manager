from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', views.menu_view, name='menu'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/change/<int:order_id>/<str:new_status>/', views.change_status, name='change_status'),
    path('submit-order/', views.submit_order, name='submit_order'),
]

# این خط طلایی است! بدون این، عکس‌ها در مرورگر باز نمی‌شوند
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)