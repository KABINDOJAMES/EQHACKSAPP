from django.contrib import admin
from django.urls import path
from EQHACKSAPP import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.loginPage, name='login-user'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout-user'),

    path('create-ticket/', views.new_ticket, name='new-ticket'),
    path('tickets/', views.tickets_list, name='tickets-list'),
    path('tickets/<str:ticket_id>/', views.ticket_detail, name='ticket-detail'),
    path('my-donations/', views.donate, name='donate'),
    path('contact/', views.contact, name='contact-us'),
    path("search/", views.search, name='search'),
]