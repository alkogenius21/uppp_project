# Generated by Django 4.1.7 on 2023-04-10 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='Book_ISBN',
            field=models.IntegerField(),
        ),
    ]