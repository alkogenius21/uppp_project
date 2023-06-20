from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LibraryUser, EmailVerificationToken, Book, Book_Category, Favorite_Book, Library_Card, News_paper

class LibraryModelsTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

    def test_library_user_creation(self):
        user = LibraryUser.objects.create(
            username='libraryuser',
            password='testpassword',
            email='library@example.com',
            first_name='John',
            last_name='Doe',
            phone='1234567890'
        )
        self.assertEqual(user.username, 'libraryuser')
        self.assertEqual(user.email, 'library@example.com')

    def test_email_verification_token_creation(self):
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token='randomtoken'
        )
        self.assertEqual(token.user, self.user)
        self.assertEqual(token.token, 'randomtoken')

    def test_book_creation(self):
        category = Book_Category.objects.create(genre='Fiction')
        book = Book.objects.create(
            book_title='Book Title',
            book_author='Book Author',
            book_description='Book Description',
            book_yearOfPublishing=2023,
            book_isbn=1234567890,
            book_genre=category
        )
        self.assertEqual(book.book_title, 'Book Title')
        self.assertEqual(book.book_genre, category)

    def test_favorite_book_creation(self):
        favorite_book = Favorite_Book.objects.create(
            user_id=self.user,
            book_id=Book.objects.create(book_title='Favorite Book'),
            is_favorite=True
        )
        self.assertEqual(favorite_book.user_id, self.user)
        self.assertEqual(favorite_book.is_favorite, True)

    def test_library_card_creation(self):
        library_card = Library_Card.objects.create(
            user_id=self.user,
            book_id=Book.objects.create(book_title='Library Card Book'),
            status='issued'
        )
        self.assertEqual(library_card.user_id, self.user)
        self.assertEqual(library_card.status, 'issued')

    def test_news_paper_creation(self):
        news_paper = News_paper.objects.create(
            News_Article='News Article',
            News_TitleOfArticle='News Title',
            News_ArticleAuthor='News Author'
        )
        self.assertEqual(news_paper.News_Article, 'News Article')
        self.assertEqual(news_paper.News_TitleOfArticle, 'News Title')

    # Add more test methods as needed

