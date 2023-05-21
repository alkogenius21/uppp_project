# -*- coding: cp1251 -*-
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class LibraryUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    groups = models.ManyToManyField('auth.Group', related_name='library_users', related_query_name='library_user')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='library_users', related_query_name='library_user')

class Book(models.Model):

    Book_Title = models.CharField(max_length=200) 
    Book_Author = models.CharField(max_length=200)  
    Book_Description = models.TextField(max_length=650) 
    Book_YearOfPublishing = models.IntegerField() 
    Book_ISBN = models.IntegerField()
    Book_UDK = models.CharField(max_length=200, null=True)
    Book_BBK = models.CharField(max_length=200, null=True)
    Book_Aviability = models.BooleanField(default=True)
    Book_Quanity = models.IntegerField(max_length=35, null=True)
    Book_Photo = models.ImageField(upload_to='media/books', default='media/book_default.jpg')
    Book_Genre = models.ForeignKey('Book_Category', on_delete=models.CASCADE, null=True)
    Book_DateOfAdd = models.DateField(auto_now_add=True, null = True)
    Book_Popular = models.BooleanField(null=True)

    def __str__(self):
        return self.Book_Title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['Book_Genre', 'Book_Title']

class Book_Category(models.Model):

    Genre = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.Genre

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})



class Library_Card(models.Model):
    #User_id = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    Book_id = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    Date_taken = models.DateField()
    Dste_given = models.DateField()

class News_paper(models.Model):

    News_DateOfPub = models.DateField(auto_now_add=True, null=True) 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80)
    News_Photo = models.ImageField(upload_to='media/posts/', default='media/default_post.jpg')

    def __str__(self):
        return self.News_Article

