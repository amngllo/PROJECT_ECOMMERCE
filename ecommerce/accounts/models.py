from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_staff = models.BooleanField('Is staff', default=False)
    is_pelanggan = models.BooleanField('Is pelanggan', default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

