from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView, profile_view, ChangePasswordView,
    RegisterUserView, UserListView, UserDetailView, 
    UserUpdateView, UserDeleteView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='password_change_view'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    # ✅ Rrugët për resetimin e fjalëkalimit
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
]
