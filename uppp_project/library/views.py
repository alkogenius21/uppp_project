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

Nav_Tables = [{'title': "�������", 'url_name': 'home'},
             {'title': "�������", 'url_name': 'catalog'},
             {'title': "�����", 'url_name': 'adress'},
             {'title': "������� ����������", 'url_name': 'about'},
             {'title': "������ �������", 'url_name': 'profile'}]

def index(request):

    current_date = datetime.now().date()
    week_ago = current_date - timedelta(days=7)

    active_item = '�������'
    news_list = News_paper.objects.order_by('-News_DateOfPub')
    book = Book.objects.all()
    latest_books = []

    for obj in book:
        if obj.book_dateOfAdd > week_ago:
            latest_books.append(obj)

        

    settings = {'menu': Nav_Tables,
               'title': '������ ������������� ����������',
               'news': news_list,
               'popular': '���������� �����',
               'latest': '��������� �����������',
               'news_name': '�������',
               'book': book,
               'latest_list': latest_books,
               'videos': '�������� �����'
               }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    return render(request, 'index.html', context=settings)

def about(request):

    active_item = '������� ����������'

    settings ={'menu': Nav_Tables, 
            'title': '������� ����������',
            'text1': '������ �����',
            'text2': '������ �����'}

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'about.html', context=settings)

def adress(request):

    active_item = '�����'

    settings ={'menu': Nav_Tables, 
                'title': '�����',
                'adress': '�� ��������� �����:'
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'adress.html', context=settings)

def catalog(request):

    
    active_item = '�������'

    cats = Book_Category.objects.all()
    books_list = Book.objects.select_related('book_genre').order_by('book_title')
    settings = {'menu': Nav_Tables, 
                'title': '������� ����', 
                'books': books_list,
                'cats': cats,
                'cat_selected': 0,
                'bron': '�������������',
                'about': '���������',
                'no_result': '�� ������ ������� ������ �� �������',
                'placeholder': '�������� ��� ����� �����...',
                'srch_btn': '�����'
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

    active_item = '������ �������'

    settings = {'menu': Nav_Tables,
                'title': '������ �������',
                'form': form,
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'register.html', context=settings)

def user_login(request):
    active_item = '������ �������'

    settings = {
        'menu': Nav_Tables,
        'title': '������ �������',
        'accept': '�����',
        'login': '�����:',
        'password': '������:',
        'register': '�����������',
        'forgot': '������ ������?',
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
            messages.error(request, '������ ��� �����. �������� ����� ��� ������.')

    return render(request, 'login.html', context=settings)

@login_required
def personal_area(request):

    active_item = '������ �������'

    settings = {'menu': Nav_Tables,
                'title': '������ �������'
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
        
        return JsonResponse({'message': f'����� "{book.book_title}" ������� �������������.'})
    else:
        return JsonResponse({'message': f'����� "{book.book_title}" ���������� ��� ������������.'}, status=400)