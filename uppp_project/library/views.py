# -*- coding: cp1251 -*-
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import *
 
Nav_Tables = [{'title': "�������", 'url_name': 'home'},
             {'title': "�������", 'url_name': 'catalog'},
             {'title': "�����", 'url_name': 'adress'},
             {'title': "������� ����������", 'url_name': 'about'},
             {'title': "������ �������", 'url_name': 'profile'}]

def index(request):

    current_date = datetime.now().date()
    week_ago = current_date - timedelta(days=7)

    active_item = '�������'
    news_list = News_paper.objects.all()
    book = Book.objects.all()
    latest_books = []
    for obj in book:
        if obj.Book_DateOfAdd > week_ago:
            latest_books.append(obj)

        

    settings = {'menu': Nav_Tables,
               'title': '������ ������������� ����������',
               'news': news_list,
               'popular': '���������� �����',
               'latest': '��������� �����������',
               'news_name': '�������',
               'book': book,
               'latest_list': latest_books
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
            'text1': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vel risus ut lacus rhoncus ultricies. Sed ac leo sapien. Fusce sem odio, commodo a elit a, suscipit suscipit ligula. Mauris congue finibus rutrum. In sed tortor vitae nisi scelerisque rhoncus nec ac turpis. In eu malesuada tortor.',
            'text2': 'Suspendisse tristique felis nec massa placerat, at hendrerit arcu hendrerit. Mauris id urna eu purus aliquet tempus. Integer eu lorem id erat finibus semper. Curabitur mollis viverra augue ut pulvinar. Ut tempor auctor mauris. Integer ut dui sit amet sem mattis ultrices.'
            }

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
    books_list = Book.objects.all()
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
