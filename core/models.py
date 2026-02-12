from django.db import models

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    cost = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True, verbose_name="توضیح کوتاه")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('seen', 'Seen'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
    ]
    
    table_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='seen')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name}"