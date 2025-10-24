from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Packages
    path('packages/', views.package_list, name='package_list'),
    path('packages/add/', views.add_package, name='add_package'),
    path('packages/update/<int:pk>/', views.update_package, name='update_package'),
    path('packages/delete/<int:pk>/', views.delete_package, name='delete_package'),

    # Bookings
    path('packages/book/<int:pk>/', views.book_package, name='book_package'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Backup
    path('backup/', views.backup, name='backup'),

    # Travel system CRUD
    path('travel/', views.travel_list, name='travel_list'),
    path('travel/add/', views.add_travel, name='add_travel'),
    path('travel/update/<int:pk>/', views.update_travel, name='update_travel'),
    path('travel/delete/<int:pk>/', views.delete_travel, name='delete_travel'),

    # 🔍 Search
    path('search/', views.search, name='search'),
]
