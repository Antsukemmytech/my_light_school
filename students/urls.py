from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.students_list, name='students_list'),
    path('students/<pk>/', views.students_detail, name='students_detail'),
    path('add_student/', views.add_student, name='add_student'),
    path('students/<pk>/update/', views.students_update, name='students_update'),
    path('students/<pk>/delete/', views.students_delete, name='students_delete'),
    path('report_card/<pk>/', views.report_card, name='report_card'),
    path('add_results/', views.add_results, name='add_results'),
    # path('add_session/', views.add_session, name='add_session'),
]