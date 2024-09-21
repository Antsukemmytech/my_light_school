from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from .enums import SessionChoices, SubjectTypes
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentClass(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

def generate_student_id(sender, instance, *args, **kwargs):
    if not instance.student_id:
        year = timezone.now().year
        student_class = instance.student_class
        student_count = Student.objects.filter(student_class=student_class, created_at__year=year).count() + 1
        instance.student_id = f"{year}/{student_class}/{student_count:03d}"

class Student(models.Model):
    
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    session = models.CharField(max_length=20, choices=[(c.value, c.name) for c in SessionChoices])
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE,)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    guardian_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.surname
    
pre_save.connect(generate_student_id, sender=Student)

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=[(c.value, c.value) for c in SubjectTypes])
    description = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    ca1 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    ca2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    exam = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(60)])
    total = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total = self.ca1 + self.ca2 + self.exam
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} {self.subject.name} {self.total}"  
