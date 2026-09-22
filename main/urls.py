from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('listing/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('listing/add/', views.create_listing_view, name='create_listing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
