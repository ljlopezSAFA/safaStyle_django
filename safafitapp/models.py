from django.db import models


# Create your models here.
class Size(models.Model):
    name = models.CharField(max_length=2)
    measures = models.CharField(max_length=600)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    image = models.CharField(max_length=2000, default="")
    price = models.FloatField(null=False)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=150)
    birth_date = models.DateField(null=False)
    dni = models.CharField(max_length=9)
    mail = models.CharField(max_length=500)
    image_url = models.CharField(max_length=900)

    def __str__(self):
        return str(self.id) + " - " + self.name + " , " + self.surname


class OrderLine(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(null=False)
    purchase_price = models.FloatField(null=False)

    def __str__(self):
        return str(self.item.name) + " - " + str(self.amount) + " - " + str(self.purchase_price)


class Order(models.Model):
    code = models.CharField(max_length=100, blank=False)
    date = models.DateField(null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_lines = models.ManyToManyField(OrderLine)

    def __str__(self):
        return str(self.code) + " - " + str(self.date) + " - " + str(self.customer.dni)


class Shop(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Employee(models.Model):
    fullname = models.CharField(max_length=500)
    birth_date = models.DateField(null=False)
    dni = models.CharField(max_length=9)
    mail = models.CharField(max_length=500)
    image_url = models.CharField(max_length=900)
    shops = models.ManyToManyField(Shop)

    def __str__(self):
        return str(self.id) + " - " + self.fullname


