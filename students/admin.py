from django.contrib import admin
from .models import Student, StudentClass, Subject, SessionChoices

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentClass)
admin.site.register(Subject)
# admin.site.register(SessionChoices)

