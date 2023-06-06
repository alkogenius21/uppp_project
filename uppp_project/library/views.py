# -*- coding: cp1251 -*-
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

Nav_Tables = [{'title': "Главная", 'url_name': 'home'},
             {'title': "Каталог", 'url_name': 'catalog'},
             {'title': "Адрес", 'url_name': 'adress'},
             {'title': "История библиотеки", 'url_name': 'about'},
             {'title': "Личный Кабинет", 'url_name': 'profile'}]

def index(request):

    current_date = datetime.now().date()
    week_ago = current_date - timedelta(days=7)

    active_item = 'Главная'
    news_list = News_paper.objects.order_by('-News_DateOfPub')
    book = Book.objects.all()
    latest_books = []

    for obj in book:
        if obj.book_dateOfAdd > week_ago:
            latest_books.append(obj)

        

    settings = {'menu': Nav_Tables,
               'title': 'Вторая Кегостровская библиотека',
               'news': news_list,
               'popular': 'Популярные книги',
               'latest': 'Последние поступления',
               'news_name': 'Новости',
               'book': book,
               'latest_list': latest_books,
               'videos': 'Полезные видео'
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
            'title': 'История Библиотеки',
            'text1': 'Первый абзац',
            'text2': 'Второй абзац'}

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
    books_list = Book.objects.select_related('book_genre').order_by('book_title')
    settings = {'menu': Nav_Tables, 
                'title': 'Каталог книг', 
                'books': books_list,
                'cats': cats,
                'cat_selected': 0,
                'bron': 'Заброинровать',
                'about': 'Подробнее',
                'no_result': 'По вашему запросу ничего не найдено',
                'placeholder': 'Название или Автор книги...',
                'srch_btn': 'Найти'
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False



    return render(request, 'catalog.html', context=settings)


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    active_item = 'Личный Кабинет'

    settings = {'menu': Nav_Tables,
                'title': 'Личный Кабинет',
                'form': form,
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'register.html', context=settings)

def user_login(request):
    active_item = 'Личный Кабинет'

    settings = {
        'menu': Nav_Tables,
        'title': 'Личный Кабинет',
        'accept': 'Войти',
        'login': 'Логин:',
        'password': 'Пароль:',
        'register': 'Регистрация',
        'forgot': 'Забыли пароль?',
    }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка при входе. Неверный логин или пароль.')

    return render(request, 'login.html', context=settings)

@login_required
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

def reserve_book(request, book_id):

    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, pk=book_id)
    
    if book.book_quanity > 0:
        library_card = Library_Card.objects.create(
            user_id=request.user, 
            book_id=book,
            status='reserved'
        )
        
        book.book_quanity = book.book_quanity - 1
        book.save()
        
        return JsonResponse({'message': f'Книга "{book.book_title}" успешно забронирована.'})
    else:
        return JsonResponse({'message': f'Книга "{book.book_title}" недоступна для бронирования.'}, status=400)