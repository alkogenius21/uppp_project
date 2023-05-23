# -*- coding: cp1251 -*-
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.username

    groups = models.ManyToManyField('auth.Group', related_name='library_users', related_query_name='library_user')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='library_users', related_query_name='library_user')

class Book(models.Model):

    book_title = models.CharField(max_length=200) 
    book_author = models.CharField(max_length=200)  
    book_description = models.TextField(max_length=650) 
    book_yearOfPublishing = models.IntegerField() 
    book_isbn = models.IntegerField()
    book_udk = models.CharField(max_length=200, null=True)
    book_bbk = models.CharField(max_length=200, null=True)
    book_aviability = models.BooleanField(default=True)
    book_quanity = models.IntegerField(max_length=35, null=True)
    book_photo = models.ImageField(upload_to='media/books', default='media/book_default.jpg')
    book_genre = models.ForeignKey('Book_Category', on_delete=models.CASCADE, null=True)
    book_dateOfAdd = models.DateField(auto_now_add=True, null = True)
    book_popular = models.BooleanField(null=True)

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



class Library_Card(models.Model):

    BOOK_STATUS_CHOICES = (
        ('reserved', 'Забронировано'),
        ('issued', 'Выдано'),
        ('returned', 'Возвращено'),
    )

    user_id = models.ForeignKey('LibraryUser', on_delete=models.PROTECT, null=True)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    date_Reserve = models.DateField(auto_now_add=True)
    date_taken = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=BOOK_STATUS_CHOICES, default='reserved')

    def __str__(self):
        return f'{self.book_id.book_title} - {self.user_id.username} ({self.status})'


@receiver(post_save, sender=Library_Card)
def update_issue_date(sender, instance, created, **kwargs):
    if instance.status == 'issued' and not instance.date_taken:
        instance.Date_taken = instance.date_Reserve
        instance.save()

@receiver(pre_delete, sender=Library_Card)
def delete_reservation(sender, instance, **kwargs):
    if instance.status == 'returned':
        instance.delete()

class News_paper(models.Model):

    News_DateOfPub = models.DateField(auto_now_add=True, null=True) 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80)
    News_Photo = models.ImageField(upload_to='media/posts/', default='media/default_post.jpg')

    def __str__(self):
        return self.News_Article

