from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def home_page(request):
    return render(request, 'homepage.html')

def show_about_us_page(request):
    return render(request, 'about_us.html')


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
