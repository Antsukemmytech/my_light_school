from django import forms
from .models import Student, StudentClass, Subject, Result

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('surname', 'other_names', 'first_name', 'session', 'student_class', 'profile_picture', 'guardian_name', 'date_of_birth')
        labels = {
            'surname': 'Surname',
            'other_names': 'Other Names',
            'first_name': 'First Name',
            'session': 'Session',
            'student_class': 'Class',
            'profile_picture': 'Profile Picture',
            'guardian_name': 'Guardian Name',
            'date_of_birth': 'Date of Birth',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'description')

class StudentClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ('name', 'description')

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'subject', 'ca1', 'ca2', 'exam', 'total')
        widgets = {
            'ca1': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'ca2': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'exam': forms.NumberInput(attrs={'min': 0, 'max': 60}),
            'total': forms.NumberInput(attrs={'readonly': True}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total'].required = False


    def clean(self):
        cleaned_data = super().clean()
        ca1 = cleaned_data.get('ca1')
        ca2 = cleaned_data.get('ca2')
        exam = cleaned_data.get('exam')
        total = ca1 + ca2 + exam
        cleaned_data['total'] = total
        return cleaned_data
