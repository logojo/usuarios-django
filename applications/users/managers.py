from django.db import models

#BaseUserManager me permite realizar la creacion de usuarios a partir del modelo de usuarios personalizado
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    #funcion privada
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
                username = username,
                email = email,
                is_staff = is_staff, 
                is_superuser = is_superuser,
                is_active = is_active,
                **extra_fields,
            )

        #encripta el password
        user.set_password(password)
        user.save(using=self.db)

        return user


    #sobreescribiendo la funcion create_user para la creacion de usuarios
    def create_user(self, username, email, password = None,  **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)
    

    def code_validation(self, id_user, code):
        #esto hace una consulta a la bd y verifica si el id y el codigo correcponden a un registro en la bd
        if self.filter(id=id_user, codregistro=code).exists():
            return True
        else:
            return False