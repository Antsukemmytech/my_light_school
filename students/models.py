from django.db import models

class Student (models.Model):
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    session = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    # profile_picture = models.ImageField()
    guardian_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    created_at = models.DateField()

    def __str__(self):
        return f"{self.surname} {self.first_name}"
        
