# Generated by Django 4.2 on 2023-04-29 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_book_category_user_user_mail_alter_book_book_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='Category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_book', to='library.book_category'),
        ),
    ]