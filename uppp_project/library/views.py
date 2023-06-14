# -*- coding: cp1251 -*-
from django.shortcuts import render, redirect
from datetime import datetime, timedelta,date
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, ForgotPasswordForm, BookForm, NewsForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

from django.contrib.auth.forms import SetPasswordForm

from django.utils.html import strip_tags

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
            user = form.save(commit=False)
            user.is_verificate = False
            user.save()
            send_verification_email(request, user)
            return redirect('verify_pls')
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
        'login': '�����',
        'password': '������',
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
            if user.is_verificate and user.is_activate:
                login(request, user)
                return redirect('profile')
            elif not user.is_verificate:
                send_verification_email(request, user)
                messages.error(request, f'��� ������� �� �������������. ����������, ��������� �����.')
            elif not user.is_activate:
                messages.error(request, '��� ������� �� �����������. ���������� � �������������� �����')
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


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    verification_url = f"{current_site}/verify/{uid}/{token}/"
    
    subject = '����������� ���� e-mail'
    text_message = f"������������, {user.username}, ���������� ���������� ����������� �� �����: {verification_url}. '/n' ���� �� �� ����������������, �� �� ���������� �� ������!"
    html_message = render_to_string('email/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    
    email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verificate = True
        user.save()
        return render(request, 'email/email_verified.html')
    else:
        return render(request, 'email/email_verification_failed.html')

def verify_page(request):
    return render(request, 'email/verify_page.html')

def forgot_password_good(request):
    return render(request, 'email/forgot_password_good.html')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = LibraryUser.objects.get(email=email)
            except LibraryUser.DoesNotExist:
                user = None

            if user is not None:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                reset_url = reverse('reset_password', args=[uid, token])
                reset_url = f"{request.scheme}://{current_site}{reset_url}"
                subject = '������������ ������'
                from_email = 'noreply@example.com'
                to_email = user.email

                html_content = render_to_string('email/reset_password_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })

                msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                print(f"Forgot password email sent to {user.email}. Reset URL: {reset_url}")
                return redirect('password_reset_done')
            else:
                form.add_error('email', '�������� � ����� email �� ����������')  # ��������� ������ � �����

    else:
        form = ForgotPasswordForm()

    return render(request, 'email/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = LibraryUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, LibraryUser.DoesNotExist):
        user = None
    print(user)
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)

        return render(request, 'email/reset_password.html', {'form': form})
    else:
        return render(request, 'email/invalid_reset_link.html')

def password_reset_complete(request):
    return render(request, 'email/password_reset_complete.html')

menu = [{'title': "�������", 'url_name': 'manager_control'},
             {'title': "���� ����", 'url_name': 'fond'},
             {'title': "�������", 'url_name': 'news'},
             {'title': "������ ���������", 'url_name': 'debtors'},
             {'title': "������/������� �����", 'url_name': 'return-add'},
             {'title': "�����", 'url_name': 'logout'}]

def manager_login(request):

    title = [{'title':'������ ������������� ����������', 'url_name': 'home'}]

    active_item = '������ ������������� ����������'

    for item in title:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_stuff:
                login(request, user)
                return redirect('manager_control')
            else:
                messages.error(request, f'� ��� ��� ������� � ���� ��������')
        else:
            messages.error(request, f'�������� ����� ��� ������.')

    return render(request, 'manager/login.html', {'menu': title})

def permission_denied(request):
    return render(request, 'manager/permission_denied.html')

@login_required(login_url='manager_login')
def manager_control(request):

    active_item = '�������'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    today = date.today()
    overdue_date = today - timedelta(days=21)
    overdue_library_cards = Library_Card.objects.filter(status='issued', date_taken__lt=overdue_date)
    library_cards = Library_Card.objects.filter(status='reserved')

    context = {
        'menu': menu,
        'reserved_library_cards': library_cards,
        'overdue_library_cards': overdue_library_cards
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')
    return render(request, 'manager/profile.html', context=context)

@login_required(login_url='manager_login')
def user_details(request):
    card_number = request.GET.get('card_number')

    try:
        user = LibraryUser.objects.get(card_number=card_number)
    except LibraryUser.DoesNotExist:
        error_message = '������������ � ����� ������� ������������� ������ �� ������.'
        return render(request, 'manager/profile.html', {'error_message': error_message})

    reserved_books = Library_Card.objects.filter(user_id=user, status='reserved')
    issued_books = Library_Card.objects.filter(user_id=user, status='issued')

    return render(request, 'manager/user_details.html', {'user': user, 'reserved_books': reserved_books, 'issued_books': issued_books})

def book_tools(request):
    
    book_isbn = request.GET.get('book_isbn')
    
    try:
        book = Book.objects.get(book_isbn=book_isbn)
        reservations = Library_Card.objects.filter(book_id=book.id, status='reserved')
        issued_users = Library_Card.objects.filter(book_id=book.id, status='issued')

        context = {
                'book': book,
                'reservations': reservations,
                'issued_users': issued_users
            }
        return render(request, 'manager/book_tools.html', context=context)

    except Book.DoesNotExist:
        return redirect('book_tools')

@login_required(login_url='manager_login')
def manager_catalog(request):
    active_item = '���� ����'

    cats = Book_Category.objects.all()
    books_list = Book.objects.select_related('book_genre').order_by('book_title')
    settings = {'menu': menu, 
                'title': '���� ����', 
                'books': books_list,
                'cats': cats,
                'about': '���������',
                'no_result': '�� ������ ������� ������ �� �������',
                'placeholder': '�������� ��� ����� �����...',
                'srch_btn': '�����'
                }

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/catalog.html', context=settings)

@login_required(login_url='manager_login')
def manager_news(request):

    active_item = '�������'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    date_param = request.GET.get('date')
    
    if date_param:
        selected_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        filtered_news = News_paper.objects.filter(News_DateOfPub=selected_date)
    else:
        filtered_news = News_paper.objects.all()

    news = News_paper.objects.order_by('-News_DateOfPub')

    if request.method == 'POST' and 'delete_news' in request.POST:
        news_id = request.POST.get('delete_news')
        news_to_delete = News_paper.objects.get(id=news_id)
        news_to_delete.delete()
        return redirect('news')

    context={
        'menu': menu,
        'news': news,
        'filtered_news': filtered_news,
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/news.html', context=context)

@login_required(login_url='manager_login')
def add_news(request):

    active_item = '�������'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    form = NewsForm()

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')

    context={
        'menu': menu,
        'form': form
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/add_news.html', context=context)

@login_required(login_url='manager_login')
def edit_news(request, news_id):

    active_item = '�������'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    news = get_object_or_404(News_paper, id=news_id)

    form = NewsForm()

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm(instance=news)

    context={
        'menu': menu,
        'form': form
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/edit_news.html', context=context)

@login_required(login_url='manager_login')
def manager_debtors(request):

    active_item = '������ ���������'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    today = date.today()
    threshold_date = today - timedelta(days=21)
    users = LibraryUser.objects.all()
    user_books = {}

    for user in users:
        books = Library_Card.objects.filter(user_id=user, status='issued', date_taken__lte=threshold_date)
        user_books[user] = books

    context = {
        'menu': menu,
        'user_books': user_books,
        }
    if not request.user.is_stuff:
        return redirect('permission_denied')
    return render(request, 'manager/debtors.html', context=context)

@login_required(login_url='manager_login')
def manager_return(request):

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/tools.html')

@login_required(login_url='manager_login')
def add_book(request):

    active_item = '���� ����'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            existing_book = Book.objects.filter(book_isbn=new_book.book_isbn).first()

            if existing_book:
                existing_book.book_quanity += new_book.book_quanity
                existing_book.save()
            else:
                new_book.save()

            return redirect('fond')
    else:
        form = BookForm()

    context = {
        'menu': menu,
        'form': form,
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/add_book.html', context=context)

@login_required(login_url='manager_login')
def change_book(request, book_id):

    active_item = '���� ����'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False


    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('fond')
    else:
        form = BookForm(instance=book)

    context = {
        'menu': menu,
        'form': form,
        'book_id': book_id,
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/change_book.html', context=context)

@login_required(login_url='manager_login')
def book_details(request, book_id):

    active_item = '���� ����'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST' and 'delete_book' in request.POST:
        book_id = request.POST.get('delete_book')
        book_to_delete = Book.objects.get(id=book_id)
        book_to_delete.delete()
        return redirect('fond')

    context = {
        'menu': menu,
        'book': book
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/book_details.html', context=context)

@login_required(login_url='manager_login')
def send_email(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        books_string = request.POST.get('books')
        books = [book.strip() for book in books_string.split(',') if book.strip()]
        print(books)
        book_list = []
        for book in books:
            book_parts = book.split(' - ')
            if len(book_parts) == 2:
                book_title = book_parts[0]
                book_author = book_parts[1]
                book_dict = {'book_title': book_title, 'book_author': book_author}
                book_list.append(book_dict)
        print(book_list)
        # �������� ������
        subject = '����������� � ������������ ������'
        from_email = 'your_email@example.com'
        to_email = recipient

        # �������� ������� HTML-������
        html_message = render_to_string('email/email_debtor.html', {'books': book_list})

        # �������� ������
        try:
            msg = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, [to_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            success_message = 'Email ������� ���������.'
        except Exception as e:
            error_message = '��������� ������ ��� �������� email.'

    return redirect('debtors')

@login_required(login_url='manager_login')
def extend_book(request, book_id):
    book = get_object_or_404(Library_Card, id=book_id, status='issued')
    
    if request.method == 'POST':
        book.date_taken = timezone.now().date()
        book.save()
        return redirect('debtors')

def issue_book(request, book_id, user_id):
    library_card = Library_Card.objects.get(book_id=book_id, user_id=user_id, status='reserved')
    library_card.issue_book()
    return redirect('return-add')

def return_book(request, book_id, user_id):
    library_card = Library_Card.objects.get(book_id=book_id, user_id=user_id, status='issued')
    library_card.return_book()
    return redirect('return-add')

def cancel_book(request, book_id, user_id):
    library_card = Library_Card.objects.get(book_id=book_id, user_id=user_id, status='reserved')
    library_card.cancel_book()
    return redirect('return-add')