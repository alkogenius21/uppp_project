
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
    path('verify/', views.verify_page, name='verify_pls'),
    path('reserve-book/<int:book_id>/', views.reserve_book, name='reserve_book'),
    path('verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
