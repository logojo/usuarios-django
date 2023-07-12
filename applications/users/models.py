from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.
#PermissionsMixin permite controlar la creacion de usuarios desde la consola
class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('O', 'Otro')
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    codregistro = models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    #esto especifica cual campo se usara para hacer el logueo
    USERNAME_FIELD = 'username'
    #campos que solicitara ademas del username y el password para crear el usuario
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def __str__(self):
        return  str(self.id) + ' - ' + self.username

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombre  + ' ' + self.apellidos