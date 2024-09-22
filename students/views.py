from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Student, Subject, StudentClass, Result, Session
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentsForm, SubjectForm, StudentClassForm, ResultForm, SessionForm


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
            return redirect('students:students_list')
    else:
        form = StudentsForm()
    return render(request, 'students/add_students.html', {'form': form})

def students_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
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

def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sessions_list')
    else:
        form = SessionForm()
    return render(request, 'add_session.html', {'form': form})

def add_results(request):
    classes = StudentClass.objects.all()
    subjects = Subject.objects.all()
    session = Session.objects.all()
    if request.method == 'POST':
        class_id = request.POST.get('class')
        subject_id = request.POST.get('subject')
        # session_id = request.Post.get('session')

        student_class = StudentClass.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)
        students = Student.objects.filter(student_class=student_class)
        # session = Session.objects.get(id=session_id)

        for student in students:
            ca1 = request.POST.get(f'ca1_{student.id}')
            ca2 = request.POST.get(f'ca2_{student.id}')
            exam = request.POST.get(f'exam_{student.id}')

            # Verify that values are not None
            if ca1 and ca2 and exam:
                Result.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'ca1': ca1,
                        'ca2': ca2,
                        'exam': exam
                    }
                )
            else:
                # Handle missing values
                print(f"Missing values for student {student.id}")

        return redirect('students:add_results')

    return render(request, 'students/add_results.html', {
        'classes': classes,
        'subjects': subjects,
        'sessions': session
    })


def report_card(request, pk):
    """
    Generate a report card for a student.

    Args:
        request (HttpRequest): The incoming request.
        pk (int): The student's primary key.

    Returns:
        HttpResponse: The rendered report card template.
    """
    student = Student.objects.get(pk=pk)
    results = Result.objects.filter(student=student)
    cumulative_total = results.aggregate(Sum('total'))['total__sum']
    return render(request, 'students/report_card.html', {'results': results, 'cumulative_total': cumulative_total})

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




