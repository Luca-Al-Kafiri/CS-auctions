from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('listing/<int:id>', views.listing, name='listing'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('cats', views.cats, name='cats'),
    path('cat/<str:category>', views.cat, name='cat'),
    path('bid/<int:id>', views.bid, name='bid'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('watch/<int:id>', views.watch, name='watch'),
    path('remove/<int:id>', views.remove, name='remove'),
    path('watchlist', views.watchlist, name='watchlist')
]
