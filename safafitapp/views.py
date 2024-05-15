import datetime
import random
import time
import plotly.graph_objs as go
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import ExpressionWrapper, F, FloatField, Sum, Count
from django.shortcuts import render

from safafit import settings
from .decorators import *
from .models import *


# Create your views here.
def home_page(request):
    return render(request, 'homepage.html')


def show_about_us_page(request):
    return render(request, 'about_us.html')


@check_user_role('ADMIN')
def show_shops(request):
    list_shops = Shop.objects.all()
    return render(request, 'list_shops.html', {'shops': list_shops})


def list_employees(request):
    list_employees = Employee.objects.all()
    return render(request, 'listEmployees.html', {'employees': list_employees})


def list_items(request):
    list_items = Item.objects.all()
    return render(request, 'listItem.html', {'items': list_items})


@check_user_roles(['ADMIN', 'EMPLOYEE'])
def new_item(request):
    if request.method == 'GET':
        sizes = Size.objects.all()
        return render(request, 'newItem.html', {'sizes': sizes})
    else:
        newItem = Item()
        newItem.name = request.POST.get('name')
        newItem.description = request.POST.get('description')
        newItem.image = request.POST.get('image')
        newItem.price = float(request.POST.get('price'))
        newItem.size = Size.objects.get(id=int(request.POST.get('size')))
        Item.save(newItem)
        return redirect('/safafit/items')


@check_user_role('ADMIN')
def new_employee(request):
    if request.method == 'GET':
        shops = Shop.objects.all()
        return render(request, "newEmployee.html", {'shops': shops})
    else:
        new = Employee()
        new.fullname = request.POST.get('fullname')
        new.mail = request.POST.get('mail')
        new.dni = request.POST.get('dni')
        new.image_url = request.POST.get('image')
        new.birth_date = request.POST.get('birthdate')
        new.save()

        list_shops = request.POST.getlist('shop')

        for s in list_shops:
            shop = Shop.objects.get(id=s)
            new.shops.add(shop)

        return redirect('/safafit/employees')


@check_user_role('ADMIN')
def edit_employee(request, id):
    employee = Employee.objects.get(id=id)
    if request.method == "GET":
        shops = Shop.objects.all()
        id_tiendas = employee.shops.values_list('id', flat=True)
        return render(request, "newEmployee.html", {'employee': employee, 'shops': shops, 'id_tiendas': id_tiendas})
    else:
        employee.fullname = request.POST.get('fullname')
        employee.mail = request.POST.get('mail')
        employee.dni = request.POST.get('dni')
        employee.image_url = request.POST.get('image')
        employee.birth_date = request.POST.get('birthdate')
        employee.save()

        list_shops = request.POST.getlist('shop')

        employee.shops.clear()

        for s in list_shops:
            shop = Shop.objects.get(id=s)
            employee.shops.add(shop)

        return redirect('/safafit/employees')


@check_user_role('ADMIN')
def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('/safafit/employees')


@check_user_role('ADMIN')
def delete_shop(request, id):
    shop = Shop.objects.get(id=id)
    shop.delete()
    return redirect('/safafit/shop/')


@check_user_role('ADMIN')
def new_shop(request):
    if request.method == 'GET':
        return render(request, 'newShop.html')
    else:
        new_shop = Shop()
        new_shop.name = request.POST.get('name')
        new_shop.address = request.POST.get('address')
        new_shop.save()
        return redirect('/safafit/shop')


@check_user_role('ADMIN')
def edit_shop(request, id):
    shop = Shop.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'newShop.html', {'shop': shop})
    else:
        shop.name = request.POST.get('name')
        shop.address = request.POST.get('address')
        shop.save()
        return redirect('/safafit/shop')


def register_user(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get('username')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        passwaord2 = request.POST.get('repeatPassword')

        errors = []

        if password != passwaord2:
            errors.append("Las contraseñas no coinciden")
        existe_usuario = User.objects.filter(username=username).exists()
        if existe_usuario:
            errors.append("Ya existe un usuario con ese nombre")
        existe_mail = User.objects.filter(email=mail).exists()
        if existe_mail:
            errors.append("Ya existe un usuario con ese email")

        if len(errors) != 0:
            return render(request, "register.html", {"errores": errors, "username": username})
        else:
            user = User.objects.create(username=username, password=make_password(password), email=mail)
            user.save()

            return redirect('home_page')


def do_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección tras un login exitoso
            return redirect('home_page')
        else:
            # Mensaje de error si la autenticación falla
            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})

    # Mostrar formulario de login para método GET
    return render(request, 'login.html')


def do_logout(request):
    logout(request)
    return redirect('login')


@check_user_role('ADMIN')
def create_employee_user(request, id):
    employee = Employee.objects.get(id=id)
    if employee.user is None:
        user = User()
        user.username = employee.fullname.replace(" ", "")
        user.email = employee.mail
        user.password = make_password(employee.dni)
        user.rol = Role.EMPLOYEE
        user.save()

        employee.user = user
        employee.save()

        return redirect('login')
    else:
        return redirect('list_employees')


def permision_error_page(request):
    return render(request, 'permision_error.html')


def no_user_logged(request):
    return render(request, 'no_user_logged_error.html')


def add_to_cart(request, id):
    cart = {}

    # Comprobar si hay ya un carrito en sesión
    if "cart" in request.session:
        cart = request.session.get("cart", {})

    # Comprobar que el producto está o no está en el carrito
    if str(id) in cart.keys():
        cart[str(id)] = cart[str(id)] + 1
    else:
        cart[str(id)] = 1

    request.session["cart"] = cart

    return redirect('items')


def show_cart(request):
    cart = {}
    session_cart = {}
    total = 0.0

    if 'cart' in request.session:
        session_cart = request.session.get('cart', {})

    for key in session_cart.keys():
        product = Item.objects.get(id=key)
        amount = session_cart[key]
        cart[product] = amount
        total += amount * product.price

    return render(request, 'cart.html', {'cart': cart, 'total': total})


def customer_profile(request):
    logged_user = User.objects.get(username=request.user.username)
    customer = None

    if logged_user is not None and logged_user.rol == Role.CUSTOMER:
        customers = Customer.objects.filter(user=logged_user)

        if len(customers) != 0:
            customer = customers[0]

        if request.method == "GET":
            if customer is not None:
                return render(request, 'customer_profile.html', {'edit': True, 'customer': customer})
            else:
                return render(request, 'customer_profile.html', {'edit': False})

        else:
            if "save_profile" in request.POST:
                customer = Customer()

            customer.name = request.POST.get('name')
            customer.surname = request.POST.get('surname')
            customer.dni = request.POST.get('dni')
            customer.mail = request.POST.get('mail')
            customer.birth_date = request.POST.get('birth_date')
            customer.image_url = request.POST.get('image')
            customer.user = logged_user
            customer.save()

            return render(request, 'customer_profile.html', {'edit': True, 'customer': customer, 'modified': True})


def buy(request):
    session_cart = {}

    if 'cart' in request.session:
        session_cart = request.session.get('cart', {})

    id_logged_user = request.user.id
    customers = Customer.objects.filter(user_id=id_logged_user)

    if len(customers) != 0:
        customer = customers[0]
        order = Order()
        order.code = "CO-" + str(int(round(time.time() * 1000)))
        order.date = datetime.date.today()
        order.customer = customer
        order.save()

        for k in session_cart.keys():
            order_line = OrderLine()
            order_line.item = Item.objects.get(id=k)
            order_line.amount = session_cart.get(k)
            order_line.purchase_price = order_line.item.price
            order_line.save()
            order.order_lines.add(order_line)

        # vaciamos el carrito
        request.session.pop('cart')

        return redirect('home_page')

    return redirect('show_cart')


@check_user_role('ADMIN')
def start_game(request):
    if request.method == "GET":
        lista_vasos = Vaso.objects.all()
        vaso_premiado = random.randint(1, 4)
        for vaso in lista_vasos:
            if vaso.id == vaso_premiado:
                vaso.premiado = True
            else:
                vaso.premiado = False
            vaso.save()
    else:
        value = request.POST["seleccion"]
        vaso_seleccionado = Vaso.objects.get(color=value)

        if vaso_seleccionado.premiado:
            return render(request, 'game.html', {"ganador": True})
        else:
            return render(request, 'game.html', {"ganador": False})

    return render(request, 'game.html', {'vasos': lista_vasos, 'inicio': True})


@check_user_role('CUSTOMER')
def my_orders(request):
    usuario_logueado = User.objects.get(id=request.user.id)
    cliente_usuario_logueado = Customer.objects.get(user=usuario_logueado)
    pedidos_cliente = Order.objects.filter(customer=cliente_usuario_logueado).annotate(
        cost=Sum(
            ExpressionWrapper(
                F('order_lines__amount') * F('order_lines__item__price'),
                output_field=FloatField()
            )
        ))

    return render(request, 'orders.html', {'orders': pedidos_cliente})


@check_user_role('CUSTOMER')
def order_detail(request, id):
    order = Order.objects.filter(id=id).annotate(
        cost=Sum(
            ExpressionWrapper(
                F('order_lines__amount') * F('order_lines__item__price'),
                output_field=FloatField()
            )
        ))

    return render(request, 'order_detail.html', {'order': order[0]})


def stadistics(request):
    return render(request, "statistics.html")




def orders_by_customer(request):
    customers_with_order_count = Customer.objects.annotate(orders_count=Count('order'))

    names = [f"{customer.name} {customer.surname}" for customer in customers_with_order_count]
    orders_count = [customer.orders_count for customer in customers_with_order_count]

    # Crear el gráfico
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=orders_count))

    # Configuraciones adicionales (títulos, ejes, etc.)
    fig.update_layout(title='Compras por cliente', xaxis_title='Clientes', yaxis_title='Número de compras')

    # Guardar el gráfico como un archivo HTML
    plotly_html_path = str(settings.TEMPLATES[0]['DIRS'][0]) + "/user_statistics.html"
    fig.write_html(plotly_html_path)

    return render(request, "customer_statistics.html")



