from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import authenticate
from django.forms.utils import ErrorList

from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña'
            }
        )
    )

    confirm = forms.CharField(
        label='Confirmar Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'confirmar contraseña'
            }
        )
    )
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombre',
            'apellidos',
            'genero',
        )
    
    def clean_confirm(self):
       if self.cleaned_data['password'] != self.cleaned_data['confirm']:
           self.add_error('confirm', 'la confirmacion de la contraseña no coincide')


class LoginForm(forms.Form):
     
      username = forms.CharField(
            label='Usuario',
            required=True,
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su usuario'
                }
            )
      )
      
      password = forms.CharField(
            label='Contraseña',
            required=True,
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su contraseña'
                }
            )
      )

      #cuando se requiere hacer la validacion de un campo en el formulario se sobreescribe la funcion clean_nombre_campo
      #cuando la validacion se va hacer sobre todo el form solo se sobreescribe la funcion clean
      def clean(self):
          #aqui le indicamos en donde se mostrara el error ya que el error no es epecifico de un campo
          cleaned_data = super(LoginForm, self).clean()

          username = self.cleaned_data['username']
          password = self.cleaned_data['password']

          if not authenticate(username = username, password = password):
              #raise corta el proceso de ejecución y manda un mensaje en pantalla
              raise forms.ValidationError('El usuario o contraseña no coinciden')
          
          return self.cleaned_data
      

class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
            label='Contraseña Actual',
            required=True,
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su contraseña'
                }
            )
      )
    
    nueva = forms.CharField(
            label='Nueva Contraseña',
            required=True,
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su nueva contraseña'
                }
            )
      )
    
    confirm = forms.CharField(
            label='Confirmar',
            required=True,
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'confirmar contraseña'
                }
            )
      )
    
    def clean_confirm(self):
       if self.cleaned_data['nueva'] != self.cleaned_data['confirm']:
           self.add_error('confirm', 'La confirmacion de la contraseña no coincide')


class VerifyForm(forms.Form):
    verify = forms.CharField(
            label='Codigo',
            required=True,
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su codigo de validación'
                }
            )
      )
    

    #se sobre escribe la funcion init para poder recibir la actualizacion de los kwargs que se realizo desde la vista
    #y poder obtener el parametro url
    #pk es el nombre del parametro url
    def __init__(self, pk, *args, **kwargs):
        #se crea una nueva variable dentro de todo el contexto del VerifyForm y poder utilizarla en cualquier funcion
        self.id_user = pk
        super(VerifyForm, self).__init__(*args, **kwargs)


    def clean_verify(self):
        print('ejecutando clean__verify')
        #recuperando codigo de formulario
        codigo = self.cleaned_data['verify']

        #len() sirve para medir el tamaño de una cadena
        if len(codigo) == 6:
            #verificando si el id de usuario y el codigo son validos
            activo = User.objects.code_validation(
                #se manda el parametro de url usando la variable creada en la funcion __init__
                self.id_user,
                codigo
            )

            if not activo:
                raise forms.ValidationError('Codigo de verificación no valido 1')
        else:
            raise forms.ValidationError('Codigo de verificación no valido 2')