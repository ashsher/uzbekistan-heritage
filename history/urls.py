from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.home, name='home'),
    path('periods/', views.period_list, name='period_list'),
    path('periods/<int:pk>/', views.period_detail, name='period_detail'),
    path('figures/', views.figure_list, name='figure_list'),
    path('figures/<int:pk>/', views.figure_detail, name='figure_detail'),
    path('figures/create/', views.figure_create, name='figure_create'),
    path('figures/<int:pk>/edit/', views.figure_edit, name='figure_edit'),
    path('figures/<int:pk>/delete/', views.figure_delete, name='figure_delete'),
    path('sites/', views.site_list, name='site_list'),
    path('sites/<int:pk>/', views.site_detail, name='site_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]