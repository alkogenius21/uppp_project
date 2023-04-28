from django.shortcuts import render
from library.models import *
# Create your views here.
def index1(request):
    books_list = Book.objects.all()
    return render(request, 'index1.html', {'books': books_list})