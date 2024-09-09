from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users import views

from users.apps import UsersConfig

name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.CreateUser.as_view(), name='registration'),
    path('confirm-email/<str:token>/', views.email_verification, name='email_confirm'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user_delete/<int:pk>', views.DeleteUserView.as_view(), name='user_delete'),
    path('account_change/<int:pk>', views.ChangeUserView.as_view(), name='account_change'),
    path('user_active_button/<int:pk>', views.user_status, name='user_status_button'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.ResetComplete.as_view(), name='password-confirm'),
]
