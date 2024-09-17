from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone



def generate_student_id(sender, instance, *args, **kwargs):
    if not instance.student_id:
        year = timezone.now().year
        class_admitted = instance.class_admitted
        student_count = Student.objects.filter(class_admitted=class_admitted, created_at__year=year).count() + 1
        instance.student_id = f"{year}/{class_admitted}/{student_count:03d}"

class Student(models.Model):
    
    # Choices for session
    SESSION_CHOICES = [
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026'),
       
    ]

    student_id = models.CharField(max_length=20, unique=True, blank=True)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    class_admitted = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    guardian_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.surname} {self.first_name}"
    
pre_save.connect(generate_student_id, sender=Student)

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca1 = models.DecimalField(max_digits=5, decimal_places=2)
    ca2 = models.DecimalField(max_digits=5, decimal_places=2)
    exam = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total = self.ca1 + self.ca2 + self.exam
        super().save()

    def __str__(self):
        return f"{self.student.name} {self.subject.name} {self.total}"
    
class StudentClass(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
