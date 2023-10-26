from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import add

urlpatterns=[
    path('',views.index,name='index'),
    path('trending',views.trending, name='trending'),
    path('login',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('logout',views.logout, name='logout'),
    path('my',views.dashboard, name='my'),
    path('category/<str:name>',views.products,name='producs'),
    path('view/<str:id>',views.more,name='more'),
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('users', views.users, name='test'),
    path('orders', views.orders, name='orders'),
    path('cart/<str:id>', views.carts, name='cart'),
    path('mycart', views.mycart, name='mycart'),
    path('search', views.search, name='search'),
    path('checkout', views.checkout, name='checkout'),
    path('buy', views.buy, name='buy'),
    path('ck', views.ck, name='ck'),
    path('offer', views.offer, name='offer'),
    path('add-category', add.add_category, name='add_category'),
    path('add-item', add.add_item, name='add_item'),
    path('add-location', add.add_location, name='add_location'),
    path('delivered/<str:id>', add.delivered, name='Delivered'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)