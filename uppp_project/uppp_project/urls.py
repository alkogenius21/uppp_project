
from uppp_project import settings

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from library import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('adress/', views.adress, name='adress'),
    path('profile/', views.personal_area, name='profile'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
