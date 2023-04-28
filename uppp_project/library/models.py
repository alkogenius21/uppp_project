"""
File with description of all database tables for MTV template
"""

from django.db import models

class Book(models.Model):

    Book_Title = models.CharField(max_length=200) 
    Book_Author = models.CharField(max_length=200) 
    Book_Genre = models.CharField(max_length=200) 
    Book_Description = models.TextField() 
    Book_YearOfPublishing = models.IntegerField() 
    Book_ISBN = models.IntegerField()
    Book_Photo = models.ImageField(upload_to='media/photos/&Genre/&Author', default='media/book_default.jpg')

    def __str__(self):
        return self.Book_Title

class User(models.Model):

    User_Surname = models.CharField(max_length=15) 
    User_Name = models.CharField(max_length=15) 
    User_Patronymic = models.CharField(max_length=15) 
    User_DateOfBirth = models.DateField()
    User_PhoneNumber = models.CharField(max_length=12)
    User_Mail = models.CharField()

    def __str__(self):
        return self.User_Mail

class News_paper(models.Model):

    News_DateOfPub = models.DateTimeField() 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80) 

    def __str__(self):
        return self.News_Article

