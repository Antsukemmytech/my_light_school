from django import forms
from .models import Staff
from django.forms import DateInput

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('email', 'phone', 'surname', 'first_name', 'other_names', 'department', 'qualification', 'course_studied', 'profile_picture', 'date_of_birth')

        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }