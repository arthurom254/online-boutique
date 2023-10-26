from .models import Cart, CartIp
from django.db.models import Sum
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def cart(request):
    ip=get_client_ip(request)
    if CartIp.objects.filter(ip=ip).exists():
        cartip=CartIp.objects.get(ip=ip).id
        cart=Cart.objects.filter(ip=cartip, checked="False").aggregate(Sum('qty'))['qty__sum']
        return {'atom':cart}
    else:
        cart=0
        return {'atom':cart}
    