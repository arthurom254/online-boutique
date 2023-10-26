from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
SIZE_CHOISE = (
    ("SM", "SM"),
    ("L", "L"),
    ("XL", "XL"),
    ("All","All"),
)

TRUE_FALSE=(
    ("True","True"),
    ("False","False"),
)

PREFERENCE=(
    ("Man","Man"),
    ("Boy","Boy"),
    ("Woman","Woman"),
    ("Girl", "Girl"),
    ("Baby", "Baby"),
)


class Category(models.Model):
    title=models.CharField(max_length=100, unique=True)
    img=models.ImageField(upload_to='category/')

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=2000)
    img=models.ImageField(upload_to='uploads/')
    price=models.IntegerField(default=0)
    category=models.ManyToManyField(Category)
    trending=models.CharField(max_length=5, choices=TRUE_FALSE, null=True)
    available=models.IntegerField()
    offer=models.CharField(max_length=5, choices=TRUE_FALSE, default='False')
    outofstalk=models.CharField(max_length=5, choices=TRUE_FALSE,default="False")
    agegroup=models.CharField(max_length=200, choices=PREFERENCE, null=True, blank=True)
    size = models.TextField(max_length=10, choices=SIZE_CHOISE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('more',args=[self.id])
    
    def __str__(self):
        return self.title
class CartIp(models.Model):
    id=models.AutoField(primary_key=True)
    ip=models.CharField(max_length=100)#user fname
    
    def __str__(self):
        return f"{self.ip}"

class Cart(models.Model):
    ip=models.ForeignKey(CartIp, on_delete=models.CASCADE , null=True)
    item=models.ForeignKey(Item, on_delete=models.CASCADE , null=True)
    qty=models.IntegerField(default=1)
    price=models.IntegerField(null=True)
    checked=models.CharField(max_length=10, choices=TRUE_FALSE, default='False')
    
    def __str__(self):
        return f"{self.id}"


class UserProfile(models.Model):
    user=models.IntegerField(null=True)
    profile=models.ImageField(upload_to='', default='profile.svg')
    phone=models.CharField(max_length=15, default='')
    
    def __str__(self):
        return f"{self.user}"




class Billing(models.Model):
    user=models.CharField(max_length=100)
    amount=models.IntegerField()
    accountnum=models.TextField(max_length=20)
    def __str__(self):
        return f"{self.user}"


class Locations(models.Model):
    id=models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    shop=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.city} - {self.area} - {self.shop}"
    class Meta:
        ordering=['city','area','shop']
        

class DeliveryLocation(models.Model):
    Delivery_Location=models.ForeignKey(Locations, on_delete=models.CASCADE)
    

class Order(models.Model):
    user=models.CharField(max_length=100)
    location=models.ForeignKey(Locations,on_delete=models.CASCADE, null=True)
    item=models.ForeignKey(Item, on_delete=models.CASCADE , null=True)
    qty=models.IntegerField(default=1)
    price=models.IntegerField(null=True)
    date=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=10, choices=TRUE_FALSE, default='False')
    def __str__(self):
        return f"{self.user} - {self.item}"