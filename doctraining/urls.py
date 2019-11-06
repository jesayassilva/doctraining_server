"""doctraining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='change-password.html')),
    path('contas/alterar_senha/', auth_views.PasswordChangeView.as_view(template_name='registration/alterar_senha.html'), name='password_change'),
    path('contas/alterar_senha/completo/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/alterar_senha_completo.html'), name='password_change_done'),
    path('contas/recuperar_senha/', auth_views.PasswordResetView.as_view(template_name='registration/recuperar_senha.html'), name='password_reset'),
    path('contas/recuperar_senha/completo/', auth_views.PasswordResetDoneView.as_view(template_name='registration/recuperar_senha_completo.html'), name='password_reset_done'),
    path('contas/resetar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/confirmar_recuperacao.html'), name='password_reset_confirm'),
    path('contas/resetar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/confirmar_recuperacao_completo.html'), name='password_reset_complete'),

    path('', include('doctrainingapp.urls',namespace='doctrainingapp'))
]

# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']


#
