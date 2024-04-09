from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home_page, name='home_page'),
    path('about_us', show_about_us_page, name='about_us'),
    path('items/', list_items, name='items'),
    path('item/new/', new_item, name='new_item'),
    path('shop/', show_shops, name='shops'),
    path('shop/new', new_shop, name='shop_new'),
    path('shop/edit/<int:id>/', edit_shop, name='shop_edit'),
    path('shop/delete/<int:id>/', delete_shop, name='shop_delete'),
    path('employees/', list_employees, name='list_employees'),
    path('employees/new',new_employee , name='new_employee'),
    path('employees/delete/<int:id>/', delete_employee , name='delete_employee'),
    path('employees/edit/<int:id>/', edit_employee, name='edit_employee'),
    path('register/', register_user, name='register'),
    path('login/', do_login, name='login'),
    path('logout/', do_logout, name='logout'),
    path('employees/user/<int:id>/', create_employee_user, name='add_user'),

]

