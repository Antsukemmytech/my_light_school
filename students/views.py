from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Student, Grade, Subject
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentsForm, GradeForm, SubjectForm, StudentClassForm

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

def add_grade(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:report_card', pk=pk)
    else:
        form = GradeForm(initial={'student': student})
    return render(request, 'students/add_grade.html', {'form': form})


def report_card(request, pk):
    student = Student.objects.get(pk=pk)
    grades = Grade.objects.filter(student=student)
    return render(request, 'students/report_card.html', {'grades': grades})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects_list')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})

def add_student_class(request):
    if request.method == 'POST':
        form = StudentClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_classes_list')
    else:
        form = StudentClassForm()
    return render(request, 'add_student_class.html', {'form': form})




