# Generated by Django 4.2 on 2023-04-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_remove_book_book_condition_remove_user_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Book_Photo',
            field=models.ImageField(default='media/book_default.jpg', upload_to='media/photos/&Genre/&Author'),
        ),
    ]
