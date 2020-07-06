from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    # path('', RedirectView.as_view(url='/blog/', permanent=True)),
    path('register/', views.RegisterFormView.as_view(), name="register"),

]

