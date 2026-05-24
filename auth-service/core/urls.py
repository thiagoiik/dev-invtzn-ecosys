"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView 
from django.http import HttpResponseRedirect


# Funcion para Password reset confirm
def password_reset_redirect(request, uidb64, token):
    frontend_url = f"https://app.sandbox.invytazyon.online/password-reset-confirm/{uidb64}/{token}/"
    return HttpResponseRedirect(frontend_url)

# Personalización del Admin de Django (Header y Títulos)
admin.site.site_header = "Invitazyon Auth Administration"
admin.site.site_title = "Invitazyon Auth Admin"
admin.site.index_title = "Auth Control Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(
        r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        TemplateView.as_view(template_name='dummy.html'), # Opcional si sobrescribes el correo
        name='account_confirm_email',
    ),
    re_path(
        r'^password-reset/confirm/(?P<uidb64>[-:\w]+)/(?P<token>[-:\w]+)/$',
        password_reset_redirect,
        name='password_reset_confirm',
    ),
]
