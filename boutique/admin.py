from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Billing)
admin.site.register(CartIp)
admin.site.register(Order)
admin.site.register(Locations)
admin.site.register(DeliveryLocation)