from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Kategori(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    discount = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Diskon (%)",
        default=0,
    )
    category = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='products', verbose_name="Kategori")
    stock_produk = models.PositiveIntegerField(verbose_name="Stok")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    merek_produk = models.CharField(max_length=50, verbose_name="Merek Produk")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def final_price(self):
        """Hitung harga akhir setelah diskon."""
        return self.price * (1 - self.discount / 100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Pengguna"
    )
    shipping_address = models.CharField(
        max_length=255, 
        verbose_name="Alamat Pengiriman",
        help_text="Masukkan alamat lengkap untuk pengiriman barang."
    )
    phone_number = models.CharField(
        max_length=15, 
        verbose_name="Nomor Telepon",
        help_text="Masukkan nomor telepon yang valid."
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True, 
        verbose_name="Avatar",
        help_text="Unggah foto profil (opsional)."
    )
    jenis_kelamin = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        verbose_name="Jenis Kelamin",
        help_text="Pilih jenis kelamin Anda."
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    class Meta:
        verbose_name = "Profil Pengguna"
        verbose_name_plural = "Profil Pengguna"

    def __str__(self):
        return f"Profil {self.user.username}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Gantilah dengan settings.AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def price(self):
        return self.quantity * self.product.final_price()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for order {self.order.id}"

class Catalog(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nama Katalog")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    def __str__(self):
        return self.name

class Review(models.Model):
    uuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)  
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Review oleh {self.user.username} pada {self.product.name}"

    class Meta:
        ordering = ['-created_at']
	
class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title