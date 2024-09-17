from django.urls import path
from . import views


app_name = 'staff'
urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('<pk>/', views.staff_detail, name='staff_detail'),
    path('<pk>/staff_update/', views.staff_update, name='staff_update'),
    path('<pk>/staff_delete/', views.staff_delete, name='staff_delete'),
]