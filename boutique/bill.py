from .models import Billing

def billing(request, total):
    bal=Billing.objects.get(user=request.user.username)
    if bal.amount >= total:
        bal.amount=(bal.amount - total)
        bal.save()
        return True
    else:
        return False