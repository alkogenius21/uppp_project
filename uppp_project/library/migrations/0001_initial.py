# Generated by Django 4.2.1 on 2023-05-23 21:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30)),
                ('second_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField(null=True)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
                ('card_number', models.CharField(default=library.models.generate_random_number, max_length=10, unique=True)),
                ('groups', models.ManyToManyField(related_name='library_users', related_query_name='library_user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='library_users', related_query_name='library_user', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=200)),
                ('book_author', models.CharField(max_length=200)),
                ('book_description', models.TextField(max_length=650)),
                ('book_yearOfPublishing', models.IntegerField()),
                ('book_isbn', models.IntegerField()),
                ('book_udk', models.CharField(max_length=200, null=True)),
                ('book_bbk', models.CharField(max_length=200, null=True)),
                ('book_aviability', models.BooleanField(default=True)),
                ('book_quanity', models.IntegerField(max_length=35, null=True)),
                ('book_photo', models.ImageField(default='media/book_default.jpg', upload_to='media/books')),
                ('book_dateOfAdd', models.DateField(auto_now_add=True, null=True)),
                ('book_popular', models.BooleanField(null=True)),
            ],
            options={
                'verbose_name': 'Книги',
                'verbose_name_plural': 'Книги',
                'ordering': ['book_genre', 'book_title'],
            },
        ),
        migrations.CreateModel(
            name='Book_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='News_paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_DateOfPub', models.DateField(auto_now_add=True, null=True)),
                ('News_Article', models.TextField()),
                ('News_TitleOfArticle', models.CharField(max_length=40)),
                ('News_ArticleAuthor', models.CharField(max_length=80)),
                ('News_Photo', models.ImageField(default='media/default_post.jpg', upload_to='media/posts/')),
            ],
        ),
        migrations.CreateModel(
            name='Library_Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_Reserve', models.DateField(auto_now_add=True)),
                ('date_taken', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('reserved', 'Забронировано'), ('issued', 'Выдано'), ('returned', 'Возвращено')], default='reserved', max_length=10)),
                ('book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.book')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library.book_category'),
        ),
    ]
