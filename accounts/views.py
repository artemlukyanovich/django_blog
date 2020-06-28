# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from accounts.forms import CustomUserCreationForm


class RegisterFormView(FormView):
    form_class = CustomUserCreationForm
    success_url = "/accounts/login/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)