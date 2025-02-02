from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    # Página de cadastro
    path('register/', views.register, name='register'),

    # Página de login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Página de logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Página de alteração de senha
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('accounts:password_change_done')  # Corrigir aqui
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    # Página de recuperação de senha
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            success_url=reverse_lazy('accounts:password_reset_done')
            # Aqui usamos reverse_lazy para o redirecionamento correto
        ),
        name='password_reset',
    ),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',  # Template que será usado
            success_url=reverse_lazy('accounts:password_reset_complete')
            # Corrigido com reverse_lazy e namespace accounts
        ),
        name='password_reset_confirm',
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',  # Página final de sucesso
        ),
        name='password_reset_complete',
    ),


]

