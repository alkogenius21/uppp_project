# -*- coding: cp1251 -*-
from django.shortcuts import render

from django.http import HttpResponse

from .models import *
 
Nav_Tables = [{'title': "Главная", 'url_name': 'home'},
             {'title': "Каталог", 'url_name': 'catalog'},
             {'title': "Адрес", 'url_name': 'adress'},
             {'title': "История библиотеки", 'url_name': 'about'},
             {'title': "Личный Кабинет", 'url_name': 'profile'}]

def index(request):
    return render(request, 'index.html', {'menu': Nav_Tables, 'title': 'Вторая Кегостровская библиотека'})

def about(request):
    books_list = Book.objects.all()
    return render(request, 'about.html', {'menu': Nav_Tables, 'title': 'Каталог книг', 'books': books_list})

def adress(request):
    return render(request, 'adress.html', {'menu': Nav_Tables, 'menu': Nav_Tables})

def catalog(request):
    books_list = Book.objects.all()
    return render(request, 'catalog.html', {'menu': Nav_Tables, 'title': 'Каталог книг', 'books': books_list})

def personal_area(request):
    return render(request, 'personal_area.html', {'menu': Nav_Tables})

def managment(request):
    return render(request, 'managment.html')
