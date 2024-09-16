from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from .models import Student
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'home.html' )

def students_list(request):
    students = Student.objects.all()
    return render (request, 'students/students_list.html', {'students': students})
