from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('test/', views.TestTemplateView.as_view())
]
