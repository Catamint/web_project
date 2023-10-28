"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from productApp import views
app_name='productApp'

urlpatterns = [
    path('products/<str:submenu_id>/', views.product, name='product'),
    path('movie/<str:movieid>/', views.movie_view, name='movie_url'),
    # path('order/<str:movieid>/', views.order_view, name='order_url'),
    path('ordering/<str:sessionid>/', views.ordering_view, name='ordering_url'),
    path('ticket/<str:ticketid>/', views.ticket_view, name='ticket_url'),
    path('search/', views.search_view, name='search_url'),
    path('add_fav/<str:movieid>/<str:action>/',views.add_fav_view, name='add_fav_url'),
    path('del_fav/<str:movieid>/',views.del_fav_view, name='del_fav_url'),
]
