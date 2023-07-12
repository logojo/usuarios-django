from typing import Any, Dict
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import FormView

#PARA ENVIASR MENSAJES A PANTALLA
from django.contrib import messages

#authenticate funcion propia de django para verificar si el usuario y password enviados coinciden en la bd
#login funcion propia de django que se ejecutara una vez que el usuario sea autenticado
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm, UpdatePasswordForm, VerifyForm
from .models import User    
from .functions import code_generator
# Create your views here.

class Register(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        #Se genera el codigo de validación
        codigo = code_generator()

        user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                nombre = form.cleaned_data['nombre'],
                apellidos = form.cleaned_data['apellidos'],
                genero = form.cleaned_data['genero'],
                codregistro = codigo,
            )
        
        #enviar el codigo por email al user
        asunto = 'Confirmacion de email'
        mensaje = ' Codigo de verificación: ' + codigo
        email_remitente = 'joelf.06.88@gmail.com'
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])

        #enviado mesaje a pantalla o templete
        messages.success(self.request, 'Se ha enviado un correo a su email')


        #redirigir a pantalla de validación
        return HttpResponseRedirect( 
            reverse(
                'users_app:verify',
                #enviando parametros por url
                kwargs={'pk': user.id}
            ) 
            )
    

class CodeVerify(FormView):
    template_name = "users/verify.html"
    form_class = VerifyForm
    success_url = reverse_lazy('users_app:login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerify, self).get_form_kwargs()
        #Con esta funcion enviamos el parametro de la url al formulario
        kwargs.update({
            #self.kwargs['pk'] recupera el parametros de url
            'pk': self.kwargs['pk']
        })

        return kwargs

    def form_valid(self, form):
        #actualizando el estatus del usuario una vez validado el codigo
        User.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super(CodeVerify, self).form_valid(form)
    


class Login(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )

        #esta funcion crea en todo el sistema la sesion del usuario autenticado
        login(self.request, user)

        return super(Login, self).form_valid(form)
    
class Logout(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect( reverse('users_app:login') )
    

    
class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        #recuperando usuario logueado
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password']
        )

        if user:
            nueva = form.cleaned_data['nueva']
            usuario.set_password(nueva)
            usuario.save()
            logout(self.request)


        return super(UpdatePassword, self).form_valid(form)
    