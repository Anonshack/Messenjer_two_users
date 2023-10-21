from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserDetailView,
    UsersListView
)

urlpatterns = [
    path('signup', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view()),
    path('user', UserDetailView.as_view()),
    path('list', UsersListView.as_view()),
]