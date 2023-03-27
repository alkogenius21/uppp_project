from django.db import models

# Create your models here.


class Book(models.Model):
    """
    ������� � ��������� ��������� �����

    """
    Book_Title = models.CharField(max_length=200) #�������� �����
    Book_Author = models.CharField(max_length=200) #����� �����
    Book_Genre = models.CharField(max_length=200) #���� �����
    Book_Description = models.TextField() #�������� �����
    Book_YearOfPublishing = models.IntegerField(max_length=4) #��� ����������(� �������� �������)
    Book_ISBN = models.IntegerField(max_length=20) #��� ISBN
    Book_Condition = models.BooleanField() #��������� �����
    Book_Image = models.ImageField() #���������� �����

class User(models.Model):
    """

    ������� � ��������� ��������� ������������

    """

    User_Surname = models.CharField(max_length=15) #������� ������������
    User_Name = models.CharField(max_length=15) #��� ������������
    User_Patronymic = models.CharField(max_length=15) #�������� ������������
    User_DateOfBirth = models.DateField() #���� �������� ������������
    User_PhoneNumber = models.CharField(max_length=12) #����� �������� ������������
    User_Address = models.CharField(max_length=200) #����� ������������

