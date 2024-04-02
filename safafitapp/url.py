from django.urls import path
from .views import *

urlpatterns = [
    path('home/',  home_page, name='home_page'),
    path('about_us', show_about_us_page, name='about_us'),
    path('items/',  list_items, name='items'),
    path('item/new/',  new_item, name='new_item'),
]
