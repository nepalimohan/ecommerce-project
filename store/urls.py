from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    # url patttern for processOrder added
    path('process_order/', views.processOrder, name='process_order'),


    path('search/', views.search, name='search'),



    # to handle favicon exception as browsers may search for favicon
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/images/favicon.ico')),


]
