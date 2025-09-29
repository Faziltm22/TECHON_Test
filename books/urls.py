from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),  # Changed to match Django's default
    path('logout/', views.logout_view, name='logout'),
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/add/', views.book_create, name='book_add'),
    path('book/<int:pk>/edit/', views.book_update, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path("request-password-reset/", views.request_password_reset, name="request_password_reset"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    

]
