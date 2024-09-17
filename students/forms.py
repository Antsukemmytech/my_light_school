from django import forms
from .models import Student, Grade

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('surname', 'other_names', 'first_name', 'session', 'class_admitted', 'profile_picture', 'guardian_name', 'date_of_birth')
        labels = {
            'surname': 'Surname',
            'other_names': 'Other Names',
            'first_name': 'First Name',
            'session': 'Session',
            'class_admitted': 'Class Admitted',
            'profile_picture': 'Profile Picture',
            'guardian_name': 'Guardian Name',
            'date_of_birth': 'Date of Birth',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('subject', 'ca1', 'ca2', 'exam')