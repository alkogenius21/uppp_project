# Generated by Django 4.2 on 2023-05-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_type_of_account_remove_book_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['Book_Genre', 'Book_Title'], 'verbose_name': 'Книги', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AlterField(
            model_name='book',
            name='Book_Photo',
            field=models.ImageField(default='media/book_default.jpg', upload_to='media/books'),
        ),
    ]
