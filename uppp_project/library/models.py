"""
File with description of all database tables for MTV template
"""

from django.db import models

class Book(models.Model):
    """

    Òable with info about book

    """
    Book_Title = models.CharField(max_length=200) #name of book
    Book_Author = models.CharField(max_length=200) #book author
    Book_Genre = models.CharField(max_length=200) #book genre
    Book_Description = models.TextField() #book about
    Book_YearOfPublishing = models.IntegerField(max_length=4) #Public Date(integer ver)
    Book_ISBN = models.IntegerField(max_length=20) #ISBN code
    Book_Condition = models.BooleanField() #condition of book
    Book_Image = models.ImageField() #book photo

class User(models.Model):
    """

    Table with user information

    """

    User_Surname = models.CharField(max_length=15) #user firstname
    User_Name = models.CharField(max_length=15) #user second name
    User_Patronymic = models.CharField(max_length=15) #user patrinymic
    User_DateOfBirth = models.DateField() #date of birth
    User_PhoneNumber = models.CharField(max_length=12) #phone number
    User_Address = models.CharField(max_length=200) #user adress

class News_paper(models.Model):
    """

    News information table

    """
    News_DateOfPub = models.DateTimeField() # date of publishing of article
    News_Photo = models.ImageField() # photo for article
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) # article title
    News_ArticleAuthor = models.CharField(max_length=80) # article author

