# Generated by Django 4.2.1 on 2023-06-16 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_libraryuser_is_stuff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library_card',
            name='status',
            field=models.CharField(choices=[('reserved', 'Забронировано'), ('issued', 'Выдано'), ('returned', 'Возвращено'), ('canceled', 'Отменено')], default='reserved', max_length=10),
        ),
        migrations.CreateModel(
            name='Favorite_Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorite', models.BooleanField(default=True)),
                ('book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.book')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]