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
    path('employees/new', new_employee, name='new_employee'),
    path('employees/delete/<int:id>/', delete_employee, name='delete_employee'),
    path('employees/edit/<int:id>/', edit_employee, name='edit_employee'),
    path('register/', register_user, name='register'),
    path('login/', do_login, name='login'),
    path('logout/', do_logout, name='logout'),
    path('employees/user/<int:id>/', create_employee_user, name='add_user'),
    path('permision/error', permision_error_page, name='permision_error'),
    path('cart/add/<int:id>', add_to_cart, name='add_to_cart'),
    path('show/cart', show_cart, name='show_cart'),
    path('customer/profile', customer_profile, name='customer_profile'),
    path('buy/', buy, name='buy'),
    path('game/', start_game, name='game'),
    path('no_user_logged_error/', no_user_logged, name="no_user_logged_error"),
    path('my_orders/', my_orders, name='my_order'),
    path('order_detail/<int:id>', order_detail, name='order_detail'),
    path('statistics/', stadistics, name='statistics'),
    path('statistic_customer_order/', orders_by_customer, name='statistic_customer_order'),
    path('statistic_customer_spent/', spent_by_customer, name='statistic_customer_spent'),
    path('statistic_product_bought/', top_bought_items, name='statistic_item_bought'),
    path('chat_bot/', chat_gpt_request, name='chat_bot')

]
