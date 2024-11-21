from django.contrib import admin
from .models import Kategori, Product, Catalog, Review, Order,OrderItem

admin.site.register(Kategori)
admin.site.register(Product)
admin.site.register(Catalog)  
admin.site.register(Review)
admin.site.register(OrderItem)
admin.site.register(Order)