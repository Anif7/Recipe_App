from django.shortcuts import render
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

class RegisterView(FormView):
    template_name='register.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('recipe:home_page')
    
    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)

