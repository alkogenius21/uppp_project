
from uppp_project import settings
from django.contrib import admin
from django.urls import path
from library import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('reserve-book/<int:book_id>/', views.reserve_book, name='reserve_book'),
    path('add-favorite/<int:book_id>/<int:user_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:book_id>/<int:user_id>/', views.remove_favorite, name='remove_favorite'),
    path('adress/', views.adress, name='adress'),
    path('profile/', views.personal_area, name='profile'),
    path('profile/report/', views.report, name='report'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit-user'),
    path('verify-mail', views.second_verify, name='second_verify'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify/', views.verify_page, name='verify_pls'),
    path('verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/complete', views.forgot_password_good, name='password_reset_done'),
    path('password-reset/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('manager/login', views.manager_login, name='manager_login'),
    path('manager/', views.manager_control, name='manager_control'),
    path('manager/permission/', views.permission_denied, name='permission_denied'),
    path('manager/catalog/', views.manager_catalog, name='fond'),
    path('manager/news/', views.manager_news, name='news'),
    path('manager/news/add/', views.add_news, name='add_news'),
    path('edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('manager/debtors/', views.manager_debtors, name='debtors'),
    path('manager/raport/', views.raport, name='raport'),
    path('manager/raport/get-file/', views.generate_raport_pdf, name='generate'),
    path('extend_book/<int:book_id>/', views.extend_book, name='extend_book'),
    path('manager/return-add/', views.manager_return, name='return-add'),
    path('manager/return-add/book-detail', views.book_tools, name='book_tools'),
    path('manager/add_book/', views.add_book, name='add_book'),
    path('change_book/<int:book_id>/', views.change_book, name='change_book'),
    path('book_details/<int:book_id>/', views.book_details, name='book_details'),
    path('manager/user-details/', views.user_details, name='user_details'),
    path('send_email/', views.send_email, name='send_email'),
    path('book/<int:book_id>/<int:user_id>/issue/', views.issue_book, name='issue_book'),
    path('book/<int:book_id>/<int:user_id>/return/', views.return_book, name='return_book'),
    path('book/<int:book_id>/<int:user_id>/cancel/', views.cancel_book, name='cancel_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
