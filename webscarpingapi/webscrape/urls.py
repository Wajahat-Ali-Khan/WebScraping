from .views import scrap
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('', view_name, name="view_name"),
    path('scrap', scrap, name="scrap"),
]
