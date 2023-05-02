from django.db import models
from django.urls import reverse

class Book(models.Model):

    Book_Title = models.CharField(max_length=200) 
    Book_Author = models.CharField(max_length=200)  
    Book_Description = models.TextField() 
    Book_YearOfPublishing = models.IntegerField() 
    Book_ISBN = models.IntegerField()
    Book_UDK = models.CharField(max_length=200, null=True)
    Book_BBK = models.CharField(max_length=200, null=True)
    Book_Aviability = models.BooleanField(default=True)
    Book_Photo = models.ImageField(upload_to='media/photos/%Genre/%Author', default='media/book_default.jpg')
    Book_Genre = models.ForeignKey('Book_Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Book_Title

class Book_Category(models.Model):

    Genre = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.Genre

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

class User(models.Model):

    User_Surname = models.CharField(max_length=15) 
    User_Name = models.CharField(max_length=15) 
    User_Patronymic = models.CharField(max_length=15) 
    User_DateOfBirth = models.DateField()
    User_PhoneNumber = models.CharField(max_length=12)
    User_Mail = models.CharField(max_length=250, null=True)
    Type_Of_Account = models.ForeignKey('Type_Of_Account', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.User_Mail

class Library_Card(models.Model):
    User_id = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    Book_id = models.ForeignKey('Book', on_delete=models.PROTECT, null=True)
    Date_taken = models.DateField()
    Dste_given = models.DateField()

class Type_Of_Account(models.Model):
    Type = models.CharField(max_length=5)
    Login = models.CharField(max_length=30)
    Password = models.CharField(max_length=50)

class News_paper(models.Model):

    News_DateOfPub = models.DateTimeField() 
    News_Article = models.TextField()
    News_TitleOfArticle = models.CharField(max_length=40) 
    News_ArticleAuthor = models.CharField(max_length=80)
    News_Photo = models.ImageField(upload_to='media/photos/%Genre/%Author', default='media/book_default.jpg')

    def __str__(self):
        return self.News_Article

