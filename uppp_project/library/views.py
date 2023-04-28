# -*- coding: cp1251 -*-
from django.shortcuts import render

from django.http import HttpResponse

from .models import *
 
Nav_Tables = ["�������", "�������", "�����", "������� ����������"]

def index(request):
    return render(request, 'index.html', {'menu': Nav_Tables, 'title': '������ ������������� ����������'})

def about(request):
    books_list = Book.objects.all()
    return render(request, 'about.html', {'title': '������� ����', 'books': books_list})

def adress(request):
    return render(request, 'adress.html', {'menu': Nav_Tables})

def catalog(request):
    books_list = Book.objects.all()
    return render(request, 'catalog.html', {'title': '������� ����', 'books': books_list})

def personal_area(request):
    return render(request, 'personal_area.html', {'menu': Nav_Tables})

def managment(request):
    return render(request, 'managment.html', {'menu': Nav_Tables})
