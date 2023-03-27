from django.db import models

# Create your models here.


class Book(models.Model):
    """
    Таблица с описанием элементов книги

    """
    Book_Title = models.CharField(max_length=200) #Название книги
    Book_Author = models.CharField(max_length=200) #Автор книги
    Book_Genre = models.CharField(max_length=200) #Жанр книги
    Book_Description = models.TextField() #Описание книги
    Book_YearOfPublishing = models.IntegerField(max_length=4) #Год публикации(в числовом формате)
    Book_ISBN = models.IntegerField(max_length=20) #Код ISBN
    Book_Condition = models.BooleanField() #Состояние книги
    Book_Image = models.ImageField() #Фотография книги

class User(models.Model):
    """

    Таблица с описанием элементов пользователя

    """

    User_Surname = models.CharField(max_length=15) #Фамилия пользователя
    User_Name = models.CharField(max_length=15) #Имя пользователя
    User_Patronymic = models.CharField(max_length=15) #Отчество пользователя
    User_DateOfBirth = models.DateField() #Дата рождения пользователя
    User_PhoneNumber = models.CharField(max_length=12) #Номер телефона пользователя
    User_Address = models.CharField(max_length=200) #Адрес пользователя

