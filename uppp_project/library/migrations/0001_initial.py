# Generated by Django 4.1.7 on 2023-04-10 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Book_Title', models.CharField(max_length=200)),
                ('Book_Author', models.CharField(max_length=200)),
                ('Book_Genre', models.CharField(max_length=200)),
                ('Book_Description', models.TextField()),
                ('Book_YearOfPublishing', models.IntegerField()),
                ('Book_ISBN', models.IntegerField(max_length=20)),
                ('Book_Condition', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='News_paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_DateOfPub', models.DateTimeField()),
                ('News_Article', models.TextField()),
                ('News_TitleOfArticle', models.CharField(max_length=40)),
                ('News_ArticleAuthor', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Surname', models.CharField(max_length=15)),
                ('User_Name', models.CharField(max_length=15)),
                ('User_Patronymic', models.CharField(max_length=15)),
                ('User_DateOfBirth', models.DateField()),
                ('User_PhoneNumber', models.CharField(max_length=12)),
                ('User_Address', models.CharField(max_length=200)),
            ],
        ),
    ]
