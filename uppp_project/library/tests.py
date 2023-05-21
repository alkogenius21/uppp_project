from django.test import TestCase
from .models import Book, Book_Category
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import index, about, adress, catalog, register, user_login, personal_area

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых данных для всех тестов в классе
        genre = Book_Category.objects.create(name='Test Genre')
        Book.objects.create(
            Book_Title='Test Book',
            Book_Author='Test Author',
            Book_Description='This is a test book.',
            Book_YearOfPublishing=2022,
            Book_ISBN=1234567890,
            Book_Genre=genre,
        )

    def test_book_title_field(self):
        book = Book.objects.get(id=1)
        title = book._meta.get_field('Book_Title')
        max_length = title.max_length
        self.assertEquals(max_length, 200)  # Проверка максимальной длины поля Book_Title

    def test_book_author_field(self):
        book = Book.objects.get(id=1)
        author = book._meta.get_field('Book_Author')
        max_length = author.max_length
        self.assertEquals(max_length, 200)  # Проверка максимальной длины поля Book_Author

    def test_book_description_field(self):
        book = Book.objects.get(id=1)
        description = book._meta.get_field('Book_Description')
        max_length = description.max_length
        self.assertEquals(max_length, 650)  # Проверка максимальной длины поля Book_Description

    def test_book_year_of_publishing_field(self):
        book = Book.objects.get(id=1)
        year_of_publishing = book._meta.get_field('Book_YearOfPublishing')
        self.assertIsInstance(year_of_publishing, models.IntegerField)  # Проверка типа поля Book_YearOfPublishing

    def test_book_genre_field(self):
        book = Book.objects.get(id=1)
        genre = book.Book_Genre
        self.assertEquals(genre.name, 'Test Genre')  # Проверка значения поля Book_Genre

    def test_object_creation(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.Book_Title, 'Test Book')  # Проверка значения поля Book_Title
        self.assertEquals(book.Book_Author, 'Test Author')  # Проверка значения поля Book_Author

    def test_verbose_name_plural(self):
        self.assertEquals(str(Book._meta.verbose_name_plural), 'Êíèãè')  # Проверка множественного числа verbose_name

    def test_ordering(self):
        ordering = Book._meta.ordering
        self.assertEquals(ordering, ['Book_Genre', 'Book_Title'])  # Проверка порядка сортировки

class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        request = self.factory.get('/')
        request.user = self.user

        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about_view(self):
        request = self.factory.get('/about/')
        request.user = self.user

        response = about(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_adress_view(self):
        request = self.factory.get('/adress/')
        request.user = self.user

        response = adress(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adress.html')

    def test_catalog_view(self):
        request = self.factory.get('/catalog/')
        request.user = self.user

        response = catalog(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog.html')

    def test_register_view(self):
        request = self.factory.get('/register/')
        request.user = self.user

        response = register(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_user_login_view(self):
        request = self.factory.get('/login/')
        request.user = self.user

        response = user_login(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_personal_area_view(self):
        request = self.factory.get('/personal_area/')
        request.user = self.user

        response = personal_area(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_area.html')