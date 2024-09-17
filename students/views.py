from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Student
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentsForm

def home(request):
    return render(request, 'home.html' )

def students_list(request):
    students = Student.objects.all()
    return render(request, 'students/students_list.html', {'students': students})

def students_detail(request, pk):
    student_instance = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student_instance})

def add_student(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('students_list')
    else:
        form = StudentsForm()
    return render(request, 'students/add_students.html', {'form': form})

def students_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentsForm(request.POST, student=student)
        if form.is_valid():
            form.save()
            return redirect('students:students_list')
    else:
        form = StudentsForm(instance=student)
    return render(request, 'students/students_form.html', {'form': form})

def students_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('students:students_list')
    return render(request, 'students/students_confirm_delete.html', {'students': student})
