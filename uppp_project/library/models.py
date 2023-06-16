# -*- coding: cp1251 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta
import random

def generate_random_number():
    return str(random.randint(1000000000, 9999999999))

class LibraryUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    card_number = models.CharField(max_length=10, default=generate_random_number, unique=True)
    is_activate = models.BooleanField(default=False)
    is_verificate = models.BooleanField(default=False)
    is_stuff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    groups = models.ManyToManyField('auth.Group', related_name='library_users', related_query_name='library_user')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='library_users', related_query_name='library_user')

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):

    book_title = models.CharField(max_length=200) 
    book_author = models.CharField(max_length=200)  
    book_description = models.TextField(max_length=650) 
    book_yearOfPublishing = models.IntegerField() 
    book_isbn = models.IntegerField()
    book_udk = models.CharField(max_length=200, null=True)
    book_bbk = models.CharField(max_length=200, null=True)
    book_aviability = models.BooleanField(default=True)
    book_quanity = models.IntegerField(null=True)
    book_photo = models.ImageField(upload_to='media/books', default='media/book_default.jpg')
    book_genre = models.ForeignKey('Book_Category', on_delete=models.CASCADE, null=True)
    book_dateOfAdd = models.DateField(auto_now_add=True, null = True)
    book_popular = models.BooleanField(null=True)

    def update_book(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def __str__(self):
        return self.book_title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['book_genre', 'book_title']

class Book_Category(models.Model):

    genre = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

class Favorite_Book(models.Model):
    user_id = models.ForeignKey('LibraryUser', on_delete=models.PROTECT, null=True)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    is_favorite = models.BooleanField(default=True)

class Library_Card(models.Model):

    BOOK_STATUS_CHOICES = (
        ('reserved', 'Забронировано'),
        ('issued', 'Выдано'),
        ('returned', 'Возвращено'),
        ('canceled','Отменено')
    )

    user_id = models.ForeignKey('LibraryUser', on_delete=models.PROTECT, null=True)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    date_Reserve = models.DateField(auto_now_add=True)
    date_taken = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=BOOK_STATUS_CHOICES, default='reserved')

    def __str__(self):
        return f'{self.book_id.book_title} - {self.user_id.username} ({self.status})'

    def save(self, *args, **kwargs):
        if self.status == 'reserved':
            if self.date_Reserve is not None:
                days_passed = (timezone.now().date() - self.date_Reserve).days
                if days_passed > 7:
                    self.status = 'canceled'
        super().save(*args, **kwargs)

    @classmethod
    def get_overdue_records(cls):
        today = date.today()
        threshold_date = today - timedelta(days=21)
        return cls.objects.filter(status='issued', date_taken__lte=threshold_date)

    def issue_book(self):
        if self.status == 'reserved':
            self.status = 'issued'
            self.date_taken = timezone.now().date()
            self.save()

    def return_book(self):
        if self.status == 'issued':
            self.status = 'returned'
            self.date_returned = timezone.now().date()
            self.book_id.book_quanity += 1
            self.book_id.save()
            self.save()

    def cancel_book(self):
        if self.status == 'reserved':
            self.status = 'canceled'
            self.book_id.book_quanity += 1
            self.book_id.save()
            self.save()

class News_paper(models.Model):

    News_DateOfPub = models.DateField(auto_now_add=True, null=True) 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80)
    News_Photo = models.ImageField(upload_to='media/posts/', default='media/default_post.jpg')

    def __str__(self):
        return self.News_Article

    def update_news(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
