

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from library import views
urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', views.index)
]
