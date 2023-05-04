from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Book)
admin.site.register(News_paper)
admin.site.register(Book_Category)
admin.site.register(Library_Card)
