from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def home_page(request):
    return render(request, 'homepage.html')


def show_about_us_page(request):
    return render(request, 'about_us.html')


def show_shops(request):
    list_shops = Shop.objects.all()
    return render(request, 'list_shops.html', {'shops': list_shops})


def list_employees(request):
    list_employees = Employee.objects.all()
    return render(request, 'listEmployees.html', {'employees':list_employees })


def list_items(request):
    list_items = Item.objects.all()
    return render(request, 'listItem.html', {'items': list_items})


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





def delete_employee(request,id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('/safafit/employees')




def delete_shop(request,id):
    shop = Shop.objects.get(id=id)
    shop.delete()
    return redirect('/safafit/shop/')



def new_shop(request):
    if request.method == 'GET':
        return render(request, 'newShop.html')
    else:
        new_shop= Shop()
        new_shop.name = request.POST.get('name')
        new_shop.address = request.POST.get('address')
        new_shop.save()
        return redirect('/safafit/shop')


def edit_shop(request, id):
    shop = Shop.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'newShop.html', {'shop': shop})
    else:
        shop.name = request.POST.get('name')
        shop.address = request.POST.get('address')
        shop.save()
        return redirect('/safafit/shop')