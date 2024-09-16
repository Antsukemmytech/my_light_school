from django.urls import path
from . import views


app_name = 'staff'
urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('<pk>/', views.staff_detail, name='detail'),
    path('<pk>/update/', views.staff_update, name='update'),
    path('<pk>/delete/', views.staff_delete, name='delete'),
]