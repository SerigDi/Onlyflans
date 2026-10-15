"""
URL configuration for onlyflans project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from web.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('web.urls')),
]
