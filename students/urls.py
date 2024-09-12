from django.urls import path
from .import views

urlpatterns = [
    path('students/', views.StudentView.as_view(), name='create-list'),
    path('students<int:pk>/', views.StudentDetailView.as_view(), name='students-details'),
]