# -*- coding: cp1251 -*-
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import *
 
Nav_Tables = [{'title': "Главная", 'url_name': 'home'},
             {'title': "Каталог", 'url_name': 'catalog'},
             {'title': "Адрес", 'url_name': 'adress'},
             {'title': "История библиотеки", 'url_name': 'about'},
             {'title': "Личный Кабинет", 'url_name': 'profile'}]

def index(request):

    current_date = datetime.now().date()
    week_ago = current_date - timedelta(days=7)

    active_item = 'Главная'
    news_list = News_paper.objects.all()
    book = Book.objects.all()
    popular_books = []
    for obj in book:
        if obj.Book_DateOfAdd > week_ago:
            popular_books.append(obj)

        

    settings = {'menu': Nav_Tables,
               'title': 'Вторая Кегостровская библиотека',
               'news': news_list,
               'popular': 'Популярные книги',
               'latest': 'Последние поступления',
               'news_name': 'Новости',
               'book': book,
               'popular_list': popular_books
               }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    return render(request, 'index.html', context=settings)

def about(request):

    active_item = 'История библиотеки'

    settings ={'menu': Nav_Tables, 
            'title': 'История Библиотеки'
            }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'about.html', context=settings)

def adress(request):

    active_item = 'Адрес'

    settings ={'menu': Nav_Tables, 
                'title': 'Адрес',
                'adress': 'Мы находимся здесь:'
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'adress.html', context=settings)

def catalog(request):

    
    active_item = 'Каталог'

    cats = Book_Category.objects.all()
    books_list = Book.objects.all()
    settings = {'menu': Nav_Tables, 
                'title': 'Каталог книг', 
                'books': books_list,
                'cats': cats,
                'cat_selected': 0
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False



    return render(request, 'catalog.html', context=settings)

def personal_area(request):

    active_item = 'Личный Кабинет'

    settings = {'menu': Nav_Tables,
                'title': 'Личный Кабинет'
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False


    return render(request, 'personal_area.html', context=settings)
