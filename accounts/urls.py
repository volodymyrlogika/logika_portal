from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
app_name = "accounts"

urlpatterns = [
    # 🔐 Аутентифікація
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='main:home'), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),

    # 👤 Профіль
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("set_theme/", views.set_theme, name="set_theme"),
    # 🔑 Зміна пароля
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html"
        ),
        name="change_password",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/change_password_done.html"
        ),
        name="password_change_done",
    ),
]
