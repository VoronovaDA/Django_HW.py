"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, register_converter

from books.converters import DateConverter
from books.views import books_view, index_view, books_date_view

register_converter(DateConverter, 'dt')

urlpatterns = [
    path('books/', books_view, name='books'),
    path('books/<dt:date>/', books_date_view, name='bdate'),
    path('', index_view),
    path('admin/', admin.site.urls),
]
