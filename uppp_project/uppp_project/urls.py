
from uppp_project import settings

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from library import views
from django.conf.urls.static import static
urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', views.index),
    path('about/', views.about),
    path('catalog/', views.catalog),
    path('adress/', views.adress),
    path('profile/', views.personal_area),
    path('manager/', views.managment)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
