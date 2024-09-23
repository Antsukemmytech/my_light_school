from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Student, Subject, StudentClass, Result, Session
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.db.models import Sum
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

@require_http_methods(["GET", "POST"])
def add_results(request):
    if request.method == 'POST' and 'view_students' in request.POST:
        session_id = request.POST['session']
        class_id = request.POST['class']
        subject_id = request.POST['subject']
        
        session = Session.objects.get(id=session_id)
        student_class = StudentClass.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)
        students = Student.objects.filter(student_class=student_class)
        
        return render(request, 'students/score_sheet.html', {
            'session': session,
            'student_class': student_class,
            'subject': subject,
            'students': students
        })
    
    return render(request, 'students/add_results.html', {
        'sessions': Session.objects.all(),
        'classes': StudentClass.objects.all(),
        'subjects': Subject.objects.all()
    })

@require_http_methods(["GET", "POST"])
def score_sheet(request, class_id, subject_id, session_id):
    try:
        student_class = StudentClass.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)
        session = Session.objects.get(id=session_id)
        students = Student.objects.filter(student_class=student_class)
        
        # Fetch results from database
        student_results = []
        for student in students:
            result = student.result_set.filter(subject=subject).first()
            student_results.append({
                'student': student,
                'result': result
            })

        if request.method == 'POST':
            for student in students:
                result = student.result_set.filter(subject=subject).first()
                if not result:
                    result = Result(
                        student=student,
                        subject=subject,
                        student_class=student_class,
                        ca1=request.POST.get(f'ca1_{student.id}'),
                        ca2=request.POST.get(f'ca2_{student.id}'),
                        exam=request.POST.get(f'exam_{student.id}'),
                        total=int(request.POST.get(f'ca1_{student.id}')) + 
                              int(request.POST.get(f'ca2_{student.id}')) + 
                              int(request.POST.get(f'exam_{student.id}'))
                    )
                    result.save()
                else:
                    result.ca1 = request.POST.get(f'ca1_{student.id}')
                    result.ca2 = request.POST.get(f'ca2_{student.id}')
                    result.exam = request.POST.get(f'exam_{student.id}')
                    result.total = int(result.ca1) + int(result.ca2) + int(result.exam)
                    result.save()
            return redirect(reverse('score_sheet', args=[class_id, subject_id, session_id]))
        
        context = {
            'student_class': student_class,
            'subject': subject,
            'session': session,
            'students': student_results,
            'has_any_result': any(student_dict['result'] for student_dict in student_results)
        }
        return render(request, 'score_sheet.html', context)
    except Exception as e:
        # Error handling
        print(f"Error: {e}")
        return render(request, 'error.html', {'error': str(e)})
    

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




