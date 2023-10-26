from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from .bill import billing
from .cart import cart, get_client_ip
from django.core.paginator import Paginator, EmptyPage
from .form import DeliveryLocationForm
import random

def randomitem(itemq, qty):
    items=list(itemq)
    try:
        return random.sample(items,qty)
    except:
        return random.sample(items,len(items))
    

def index(request):
    category=Category.objects.filter()[:10]
    try:
        c=Category.objects.first().title
    except:
        c='women'

    itemq=Item.objects.filter(trending='True', outofstalk='False')
    item=randomitem(itemq, 24)
    context={
        'category':category,
        'item':item,
        'c':c,
    }
    return render(request, 'index.html', context)

def trending(request):
    itemq=Item.objects.filter(trending='True', outofstalk='False')
    item=randomitem(itemq, 20)
    context={
        'item':item,
    }
    return render(request, 'products.html', context)

def offer(request):
    itemq=Item.objects.filter(offer='True', outofstalk='False')
    item=randomitem(itemq, 20)
    context={
        'item':item,
    }
    return render(request, 'products.html', context)

def products(request,name):
    category=Category.objects.get(title=name)
    id=category.id
    itemq=Item.objects.filter(category__exact=id, outofstalk='False')
    item=randomitem(itemq, 30)
    context={
        'item':item
    }
    return render(request, 'products.html',context)

def more(request, id):
    item=Item.objects.get(id=id, outofstalk='False')
    ip=get_client_ip(request)
    relatedq=Item.objects.filter(category=item.category.first(), outofstalk='False')
    related=randomitem(relatedq, 12)
    if CartIp.objects.filter(ip=ip).exists():
        ipid=CartIp.objects.get(ip=ip).id
        if Cart.objects.filter(ip=ipid, item=Item(id=id)).exists():
            cart=Cart.objects.get(ip=ipid,item=Item(id=id))
            context={"item":item, "cart":cart,"related":related}
            return render(request,'more.html',context)
        else:
            context={"item":item,"related":related}
            return render(request,'more.html',context)
    else:
        context={"item":item,"related":related}
        return render(request,'more.html',context)
   


def login(request):
    if request.method=='POST':
        username=request.POST['email']
        username=username
        password=request.POST['pwd']
        nxt=request.GET.get('next')
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            url='/updateprofile'
            if nxt is not None:
                url+='?next='+nxt
            return redirect(url)
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            messages.info(request, 'Log in')
            return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

        
def signup(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['pwd']
        password2=request.POST['pwd2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=fname, last_name=lname,username=email, email=email, password=password)
                user.save()
                Billing.objects.create(user=email, accountnum=email, amount=1000)
                return redirect('login')
        else:
            
            messages.info(request,'Password not same')
            return render(request, 'signup.html')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            messages.info(request,'Create your account')
            return render(request, 'signup.html') 
        
"""Automatically create a row in UserProfile model"""

def updateprofile(request):
    if request.user.is_authenticated:
        id=request.user.id
        nxt=request.GET.get('next')
        if UserProfile.objects.filter(user=id).exists():
            if nxt is not None:
                return redirect(nxt)
            else:
                if request.user.is_superuser:
                    return redirect('/my')
                else:
                    return redirect('/')
        else:
            profile=UserProfile.objects.create(user=id)
            profile.save()
            if nxt is not None:
                return redirect(nxt)
            else:
                return redirect('/')
    else:
        return redirect('login')


def order(request, name):
    if request.user.is_authenticated:
        item=Item.objects.get(name=name)
        context={
            'item':item,
        }
        return render(request, 'order.html',context)
    else:
        messages.info(request, 'Login to proceed with your order')
        return redirect('login')


def dashboard(request):
    if request.user.is_authenticated:
        id=request.user.id
        if Billing.objects.filter(user=request.user.username).exists():
            bill=Billing.objects.get(user=request.user.username)
        else:
            bill=None
        if request.method == 'POST':
            fname=request.POST['fname']
            lname=request.POST['lname']
            phone=request.POST['phone']
            
            profile=UserProfile.objects.get(user=id)
            if 'photo' in request.FILES:
                image=request.FILES['photo']
                fss=FileSystemStorage()
                file=fss.save(image.name, image)                
                profile.profile=file
            profile.phone=phone
            profile.save()
            user=User.objects.get(id=id)
            user.first_name=fname
            user.last_name=lname
            user.save()
            details=UserProfile.objects.get(user=id)
            context={"details":details,"bill":bill}
            return render(request, 'my.html', context)

        elif UserProfile.objects.filter(user=id).exists():
            details=UserProfile.objects.get(user=id)
            context={"details":details,"bill":bill} 
            messages.info(request,"Welcome Back")
            return render(request, 'my.html', context)
        else:
            messages.info(request,"Welcome Back")
            return render(request, 'my.html')
    else:
        messages.info(request, 'Welcome back')
        url='/login'
        url+='?next=my'
        return redirect('/login?next=/my')



def carts(request, id):
    ipaddr=get_client_ip(request)
    item=Item.objects.get(id=id)
    max=item.available
    
    if request.method == 'GET':
        add=request.GET.get('add')
        if CartIp.objects.filter(ip=ipaddr).exists():
            cartip=CartIp.objects.get(ip=ipaddr).id
            if Cart.objects.filter(ip=CartIp(id=cartip)).exists():
                if Cart.objects.filter(ip=CartIp(id=cartip),item=Item(id=id)).exists():
                    cart=Cart.objects.get(ip=CartIp(id=cartip),item=Item(id=id))
                    if add is not None:
                        num=cart.qty+int(add)
                    
                    if num > 0 and num <= max :
                        cart.qty=num
                        cart.price=item.price*cart.qty
                        cart.save()
                        return HttpResponse(cart.qty)
                    
                    elif num==0:
                        cart=Cart.objects.get(ip=CartIp(id=cartip),item=Item(id=id)).delete()
                        return HttpResponse(0)
                    elif num >max:
                        return HttpResponse(cart.qty)
                else:
                    Cart.objects.create(ip=CartIp(id=cartip),item=Item(id=id),qty=1, price=item.price )
                    return HttpResponse(1)
            else:
                Cart.objects.create(ip=CartIp(id=cartip),item=Item(id=id),qty=1, price=item.price )
                return HttpResponse(1)
        else:
            if CartIp.objects.create(ip=ipaddr):
                Cart.objects.create(ip=CartIp(id=cartip),item=Item(id=id),qty=1, price=item.price )
                return HttpResponse(1)
    else:
        return HttpResponse()
    
    


def mycart(request):
    if CartIp.objects.filter(ip=get_client_ip(request)).exists():
        cartip=CartIp.objects.get(ip=get_client_ip(request))
        cart=Cart.objects.filter(ip=cartip.id)
        item=Item.objects.all()
        total=cart.aggregate(Sum('price'))
        context={"cart":cart,"item":item, "total":total}
        return render(request, 'cart.html', context)
    else:
        return HttpResponse("Nothing to display")
   

def orders(request):
    if request.user.is_authenticated:
        name=request.user.username
        
        if request.user.is_superuser:
            data=Order.objects.all()
        else:
            data=Order.objects.filter(user=name)
        page_n=request.GET.get('page',1)
        p=Paginator(data,15)
        try:
            page=p.page(page_n)
        except EmptyPage:
            page=p.page(1)

        context={
            "order":page,
            "page":page_n,
            "orderby":order
        }
        return render(request, 'myorders.html',context)
    else:
        messages.info(request, 'Login to view your order')
        return redirect('/login?next=/orders')
    
def users(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user=User.objects.all().order_by('first_name')
            userprofile=UserProfile.objects.all()
            context={'user1':user, 'userprofile':userprofile}
            return render(request, 'user.html',context)
        else:
            return redirect('/')
    else:
        return redirect('/login?next=/users')
    
def checkout(request):
    
    if CartIp.objects.filter(ip=get_client_ip(request)).exists():
        
        if request.user.is_authenticated:
            if request.user.is_superuser:
                messages.info(request,"You are redirected to this page because admins are not allowed to checkout")
                return redirect('/my')
            else:
                cartip=CartIp.objects.get(ip=get_client_ip(request))
                cart=Cart.objects.filter(ip=cartip.id)
                item=Item.objects.all()
                form=DeliveryLocationForm()
                bal=Billing.objects.get(user=request.user.username).amount
                total=cart.aggregate(Sum('price'))
                if request.method == 'POST':
                    if buy(request) == True:
                        return redirect('/orders')
                    else:
                        context={"cart":cart,"item":item, "total":total,"bal":bal,"show":"show","form":form}
                        return render(request, 'checkout.html', context)
                else:
                    context={"cart":cart,"item":item, "total":total,"bal":bal,"form":form}
                    return render(request, 'checkout.html', context)
        else:
            return redirect('/login?next=checkout')
    else:
        return HttpResponse("Nothing to display")
    
def buy(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            if CartIp.objects.filter(ip=get_client_ip(request)).exists():
                cartid=CartIp.objects.get(ip=get_client_ip(request)).id
                if Cart.objects.filter(ip=cartid).exists():
                    cart=Cart.objects.filter(ip=cartid)
                    total=cart.aggregate(Sum('price'))['price__sum']
                    total=int(total)

                    location=request.POST['Delivery_Location']
                    if billing(request, total) == True:
                        for vals in cart:
                            Order.objects.create(user=request.user.username,location=Locations(id=location), item=vals.item, qty=vals.qty, price=vals.price)
                            i=Item.objects.get(id=vals.item.id)
                            i.available=i.available - vals.qty
                            if i.available > 0:
                                pass
                            else:
                                i.outofstalk='True'
                            i.save()
                            vals.delete()
                        return True
                    else:                        
                        messages.info(request,"You dont have enough money to buy these products")
                        return HttpResponse("No funds")
                else:
                    messages.info(request,"Your cart seems to be empty")
                    return HttpResponse("Empty cart")
            else:
                return False
        else:
            return False
    else:
        return redirect('/login?next=checkout')
    

def search(request):
    search=request.GET['q']
    result=Item.objects.filter(title__icontains=search, outofstalk='False')
    page_n=request.GET.get('page',1)
    p=Paginator(result, 10)
    try:
        page=p.page(page_n)
    except EmptyPage:
        page=p.page(1)

    context={
        "searchresult":page,
        "q":search
    }
    return render(request,'search.html',context)

def ck(request):
    a=cart(request)['atom']
    if a is not None:
        return HttpResponse(a)
    else:
        return HttpResponse(0)