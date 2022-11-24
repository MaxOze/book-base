"""bookdatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from bookcrud import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start),
    path('shop/', views.index, name='shop'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('tocart/<int:id>', views.toCart, name='tocart'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
]


