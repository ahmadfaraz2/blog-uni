from django.urls import path
from .views import SignUpView, login_view

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup_view"),
    path("login/", login_view, name="login"),
]
