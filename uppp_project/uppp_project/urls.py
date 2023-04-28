
from uppp_project import settings

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from library import views
import library_manager
from django.conf.urls.static import static
urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('adress/', views.adress, name='adress'),
    path('profile/', views.personal_area, name='profile'),
    path('manage/', include('library_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
