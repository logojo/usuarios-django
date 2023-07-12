import datetime
from django.shortcuts import render

#LoginRequiredMixin es un mixin de protejer una vista y no permitir el ingreso a menos que este logueado
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
# Create your views here.

#mixin personalizado
class FechaMixin(object):

    #funcion que se utiliza cuando se quiere enviar datos al templete
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

class Home(LoginRequiredMixin, FechaMixin, TemplateView):
    template_name = "home/index.html"
    #redireccion al no estar loguado
    login_url = reverse_lazy('users_app:login')
    
class PrueabaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"

    