from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="add"),
    path("<int:id>", views.detail, name="detail"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    
]
