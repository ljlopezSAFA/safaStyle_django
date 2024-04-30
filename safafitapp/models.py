from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    CUSTOMER = 'CUSTOMER', 'Customer'
    EMPLOYEE = 'EMPLOYEE', 'Employee'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, )
    rol = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.username




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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default= None)

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
    user = models.OneToOneField(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id) + " - " + self.fullname


