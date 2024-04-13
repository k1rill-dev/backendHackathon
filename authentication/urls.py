from django.urls import path
from .views import TestView, LoginView, LogoutView, RotateTokensView, RegisterUserView, UserView

urlpatterns = [
    path('', TestView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('refresh', RotateTokensView.as_view()),
    path('register', RegisterUserView.as_view()),
    path('my-profile', UserView.as_view())
]
