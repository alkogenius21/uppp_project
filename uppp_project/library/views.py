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
    settings ={'menu': Nav_Tables, 
               'title': 'История Библиотеки'
               }
    return render(request, 'about.html', context=settings)

def adress(request):
    settings ={'menu': Nav_Tables, 
               'title': 'Адрес',}
    return render(request, 'adress.html', context=settings)

def catalog(request):
    cats = Book_Category.objects.all()
    books_list = Book.objects.all()
    settings = {'menu': Nav_Tables, 
                'title': 'Каталог книг', 
                'books': books_list,
                'cats': cats,
                'cat_selected': 0}

    return render(request, 'catalog.html', context=settings)

def personal_area(request):
    settings = {'menu': Nav_Tables,
                'title': 'Личный Кабинет'}
    return render(request, 'personal_area.html', context=settings)
