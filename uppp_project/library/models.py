"""
File with description of all database tables for MTV template
"""

from django.db import models

class Book(models.Model):

    Book_id = models.BigAutoField(primary_key=True)
    Book_Title = models.CharField(max_length=200) 
    Book_Author = models.CharField(max_length=200) 
    Book_Genre = models.CharField(max_length=200) 
    Book_Description = models.TextField() 
    Book_YearOfPublishing = models.IntegerField() 
    Book_ISBN = models.IntegerField() 
    Book_Condition = models.BooleanField() 

class User(models.Model):

    User_id = models.BigAutoField(primary_key=True)
    User_Surname = models.CharField(max_length=15) 
    User_Name = models.CharField(max_length=15) 
    User_Patronymic = models.CharField(max_length=15) 
    User_DateOfBirth = models.DateField() 
    User_PhoneNumber = models.CharField(max_length=12) 
    User_Address = models.CharField(max_length=200) 

class News_paper(models.Model):
    News_id = models.BigAutoField(primary_key=True)
    News_DateOfPub = models.DateTimeField() 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80) 

