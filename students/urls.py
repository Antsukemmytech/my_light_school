from django.urls import path
from .import views

app_name='students'
urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.students_list, name='students_list'),
    path('<pk>/students_detail', views.students_detail, name='students_detail'),
    path('add_student/', views.add_student, name='add_student'),
    path('<pk>/students_update/', views.students_update, name='students_update'), 
    path('<pk>/students_delete/', views.students_delete, name='students_delete'), 
    path('report_card/<pk>/', views.report_card, name='report_card'),
    path('add_grade/<pk>/', views.add_grade, name='add_grade'), 
    
]