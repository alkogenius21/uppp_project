# -*- coding: cp1251 -*-
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta,date
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, ForgotPasswordForm, BookForm, NewsForm, EditProfileForm, ProblemReportForm
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.core.mail import EmailMessage

from django.contrib.auth import logout
from django.db.models import Q

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

    if request.user.is_authenticated:
        favorite_book_ids = Favorite_Book.objects.filter(user_id=request.user).values_list('book_id', flat=True)
    else:
        favorite_book_ids = []

    items_per_page = 8
    paginator = Paginator(books_list, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    settings = {'menu': Nav_Tables, 
                'title': 'Каталог книг', 
                'books': page_obj,
                'favorite_book_ids': favorite_book_ids,
                'cats': cats,
                }

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    return render(request, 'catalog.html', context=settings)

@csrf_exempt
def add_favorite(request, book_id, user_id):

    user = LibraryUser.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)

    try:
        favorite_book = Favorite_Book.objects.get(book_id=book, user_id=user)
        return JsonResponse({'message': 'removed'})
    except Favorite_Book.DoesNotExist:
        favorite_book = Favorite_Book.objects.create(book_id=book, user_id=user)
        return JsonResponse({'message': 'added'})
    except LibraryUser.DoesNotExist:
        return JsonResponse({'message': 'user_not_found'})


@csrf_exempt
def remove_favorite(request, book_id, user_id):
    try:
        favorite_book = Favorite_Book.objects.get(book_id=book_id, user_id=user_id)
        favorite_book.delete()
        return JsonResponse({'message': 'removed'})
    except Favorite_Book.DoesNotExist:
        return JsonResponse({'message': 'not_found'})

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            
            if LibraryUser.objects.filter(email=email).exists() or LibraryUser.objects.filter(phone=phone).exists():
                messages.error(request, 'Пользователь с таким email или номером телефона уже существует.')
                return redirect('register')
            user = form.save(commit=False)
            user.is_verificate = False
            user.save()
            send_verification_email(request, user)
            return redirect('verify_pls')
            
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
        'login': 'Логин',
        'password': 'Пароль',
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
            if user.is_verificate and user.is_activate:
                login(request, user)
                return redirect('profile')
            elif not user.is_verificate:
                send_verification_email(request, user)
                messages.error(request, f'Ваша почта не подтверждена. Пожалуйста, проверьте почту.')
            elif not user.is_activate:
                messages.error(request, 'Ваш аккаунт не активирован. Обратитесь к администратору сайта')
        else:
            messages.error(request, 'Ошибка при входе. Неверный логин или пароль.')

    return render(request, 'login.html', context=settings)

@login_required
def personal_area(request):

    user = request.user
    books = Book.objects.select_related('book_genre').order_by('book_title')
    issued_books_ids = Library_Card.objects.filter(user_id=user, status='issued').values_list('book_id', flat=True)
    reserved_books_ids = Library_Card.objects.filter(user_id=user, status='reserved').values_list('book_id', flat=True)
    favorite_book_ids = Favorite_Book.objects.filter(user_id=user).values_list('book_id', flat=True)
    library_card = Library_Card.objects.filter(user_id=request.user)
    form = ProblemReportForm()

    settings = {'menu': Nav_Tables,
                'title': 'Личный Кабинет',
                'issued_books_ids': issued_books_ids,
                'reserved_books_ids': reserved_books_ids,
                'user': user,
                'books': books,
                'favorite_book_ids': favorite_book_ids,
                'library_card': library_card,
                'form': form
                }

    active_item = 'Личный Кабинет'

    for item in Nav_Tables:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False


    return render(request, 'personal_area.html', context=settings)

def report(request):
    if request.method == 'POST':
        problem_title = request.POST.get('problem_title')
        problem_description = request.POST.get('problem_description')
        problem_photo = request.FILES.get('problem_photo')

        email = EmailMessage(
            'Новый отчет о проблеме',
            f'Название проблемы: {problem_title}\nОписание проблемы: {problem_description}',
            'report@2kegostrovskaya.ru',
            ['admin@2kegostrovskaya.ru'],
        )

        if problem_photo:
            email.attach(problem_photo.name, problem_photo.read(), problem_photo.content_type)

        email.send()
        return HttpResponse(status=200)

@login_required
def edit_user(request, user_id):

    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.is_verificate = False
            user.save()
            send_verification_email(request, user)
            logout(request)
            return redirect('second_verify')
    else:
        form = EditProfileForm(instance=user)

    context = {
        'menu': Nav_Tables,
        'form': form,
        }
    return render(request, 'edit_profile.html', context=context)

def second_verify(request):
    return render(request, 'email/second_verify.html')

def reserve_book(request, book_id):

    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, pk=book_id)
    try:
        library_card = Library_Card.objects.get(book_id=book, user_id=request.user)
    
        if library_card.status == 'reserved':
            return JsonResponse({'message': f'Книга "{book.book_title}" уже забронирована вами!'})
        elif library_card.status == 'issued':
            return JsonResponse({'message': f'Книга "{book.book_title}" уже выдана вам!'})
    
    except Library_Card.DoesNotExist:
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


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    verification_url = f"{current_site}/verify/{uid}/{token}/"
    
    subject = 'Подтвердите свой e-mail'
    text_message = f"Здравствуйте, {user.username}, пожалуйста подвердите регистрацию на сайте: {verification_url}. '/n' если вы не регистрировались, то не переходите по ссылке!"
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
                subject = 'Восстановить пароль'
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
                form.add_error('email', 'Аккаунта с таким email не существует')  # Добавляем ошибку в форму

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

menu = [{'title': "Главная", 'url_name': 'manager_control'},
             {'title': "Фонд книг", 'url_name': 'fond'},
             {'title': "Новости", 'url_name': 'news'},
             {'title': "Список должников", 'url_name': 'debtors'},
             {'title': "Отчёт", 'url_name': 'raport'},
             {'title': "Выдать/Забрать книгу", 'url_name': 'return-add'},
             {'title': "Выйти", 'url_name': 'logout'},]

def manager_login(request):

    title = [{'title':'Вторая Кегостровская библиотека', 'url_name': 'home'}]

    active_item = 'Вторая Кегостровская библиотека'

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
                messages.error(request, f'У вас нет доступа к этой странице')
        else:
            messages.error(request, f'Неверный логин или пароль.')

    return render(request, 'manager/login.html', {'menu': title})

def permission_denied(request):
    return render(request, 'manager/permission_denied.html')

@login_required(login_url='manager_login')
def manager_control(request):

    active_item = 'Главная'

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
        error_message = 'Пользователь с таким номером читательского билета не найден.'
        return render(request, 'manager/profile.html', {'error_message': error_message})

    reserved_books = Library_Card.objects.filter(user_id=user, status='reserved')
    issued_books = Library_Card.objects.filter(user_id=user, status='issued')

    return render(request, 'manager/user_details.html', {'user': user, 'reserved_books': reserved_books, 'issued_books': issued_books})

@login_required(login_url='manager_login')
def raport(request):

    card_number = request.GET.get('card_number')
    book_title = request.GET.get('book_title')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    
    library_card = Library_Card.objects.all()
    
    if card_number:
        library_card = library_card.filter(user_id__card_number=card_number)
    
    if book_title:
        library_card = library_card.filter(book_id__book_title__icontains=book_title)
    
    if start_date and end_date:
        library_card = library_card.filter(Q(date_Reserve__gte=start_date) & Q(date_Reserve__lte=end_date))
    
    if status:
        library_card = library_card.filter(status=status)

    active_item = 'Отчёт'

    settings = {'menu': menu,
                'library_card': library_card,
                }

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/raport.html', context=settings)


@login_required(login_url='manager_login')
def generate_raport_pdf(request):
     
    pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))

    records = Library_Card.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="library_records.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    
    data = [['Дата бронирования', 'Дата выдачи', 'Дата вовзрата', 'Читательский билет', 'Книга(ISBN)', 'Статус']]

    for record in records:
        data.append([str(record.date_Reserve), str(record.date_taken), str(record.date_returned), record.user_id.card_number, record.book_id.book_isbn, record.status])
    
    table = Table(data, colWidths=[110, 110, 110, 150, 150, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return response


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
    active_item = 'Фонд книг'

    cats = Book_Category.objects.all()
    books_list = Book.objects.select_related('book_genre').order_by('book_title')
    settings = {'menu': menu, 
                'title': 'Фонд книг', 
                'books': books_list,
                'cats': cats,
                'about': 'Подробнее',
                'no_result': 'По вашему запросу ничего не найдено',
                'placeholder': 'Название или Автор книги...',
                'srch_btn': 'Найти'
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

    active_item = 'Новости'

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

    active_item = 'Новости'

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

    active_item = 'Новости'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False
    
    news = get_object_or_404(News_paper, id=news_id)

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

    active_item = 'Список Должников'

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
    
    active_item = 'Выдать/забрать книгу'

    for item in menu:
        if item['title'].lower() == active_item.lower():
            item['active'] = True
        else:
            item['active'] = False

    context = {
        'menu': menu
        }

    if not request.user.is_stuff:
        return redirect('permission_denied')

    return render(request, 'manager/tools.html', context=context)

@login_required(login_url='manager_login')
def add_book(request):

    active_item = 'Фонд Книг'

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

    active_item = 'Фонд Книг'

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

    active_item = 'Фонд Книг'

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
        # Создание письма
        subject = 'Уведомление о просроченных книгах'
        from_email = 'your_email@example.com'
        to_email = recipient

        # Загрузка шаблона HTML-письма
        html_message = render_to_string('email/email_debtor.html', {'books': book_list})

        # Отправка письма
        try:
            msg = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, [to_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            success_message = 'Email успешно отправлен.'
        except Exception as e:
            error_message = 'Произошла ошибка при отправке email.'

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
    book = Book.objects.get(id=book_id)
    library_card.issue_book()
    return JsonResponse({'message': f'Книга "{book.book_title}" успешно выдана.'})

def return_book(request, book_id, user_id):
    library_card = Library_Card.objects.get(book_id=book_id, user_id=user_id, status='issued')
    book = Book.objects.get(id=book_id)
    library_card.return_book()
    return JsonResponse({'message': f'Книга "{book.book_title}" успешно возвращена.'})

def cancel_book(request, book_id, user_id):
    library_card = Library_Card.objects.get(book_id=book_id, user_id=user_id, status='reserved')
    book = Book.objects.get(id=book_id)
    library_card.cancel_book()
    return JsonResponse({'message': f'Бронь на книгу "{book.book_title}" была отменена!'})