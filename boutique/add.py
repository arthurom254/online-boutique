from django.shortcuts import render, redirect
from django.contrib import messages
from .form import AddItems, AddCategory,LocationsForm
from django.http import HttpResponse
from .models import Order
def add_item(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method=='POST':
                form1=AddItems(request.POST, request.FILES)
                if form1.is_valid():
                    form1.save()
                    messages.success(request,"Saved Successfuly")
                    context={"form":AddItems(), "name_form":"Product", "show":"show", "success":"success"}
                    return render(request, 'additem.html',context)
                else:
                    messages.success(request,"Not saved - an error Occured")
                    context={"form":AddItems(), "name_form":"Products", "show":"show", "danger":"danger"}
                    return render(request, 'additem.html',context)
            else:
                context={"form":AddItems(), "name_form":"Product"}
                return render(request, 'additem.html',context)
        else:
            return redirect("/")
    else:
        return redirect("/login?next=/add-item")
    
def add_category(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method=='POST':
                form1=AddCategory(request.POST, request.FILES)
                if form1.is_valid():
                    form1.save()
                    messages.success(request,"Saved Successfuly")
                    context={"form":AddCategory(), "name_form":"Category", "show":"show", "success":"success"}
                    return render(request, 'additem.html',context)
                else:
                    messages.success(request,f"Category {request.POST['title']} already exist")
                    context={"form":AddCategory(), "name_form":"Category", "show":"show", "danger":"danger"}
                    return render(request, 'additem.html',context)
            else:
                context={"form":AddCategory(), "name_form":"Category"}
                return render(request, 'additem.html',context)
        else:
            return redirect("/")
    else:
        return redirect("/login?next=/add-category")

def add_location(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method=='POST':
                form1=LocationsForm(request.POST, request.FILES)
                if form1.is_valid():
                    form1.save()
                    messages.success(request,"Saved Successfuly")
                    context={"form":LocationsForm(), "name_form":"Location", "show":"show", "success":"success"}
                    return render(request, 'additem.html',context)
                else:
                    messages.success(request,"An error occured")
                    context={"form":LocationsForm(), "name_form":"Location", "show":"show", "danger":"danger"}
                    return render(request, 'additem.html',context)
            else:
                context={"form":LocationsForm(), "name_form":"Location"}
                return render(request, 'additem.html',context)
        else:
            return redirect("/")
    else:
        return redirect("/login?next=/add-category")

def delivered(request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                order=Order.objects.get(id=id)
                order.status='True'
                order.save()
                return HttpResponse("Success")
            else:
                return redirect('/')
        else:
            return redirect("/login")