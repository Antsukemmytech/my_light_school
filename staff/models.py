from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True)
    surname = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1, null=True)
    qualification = models.CharField(max_length=50, null=True)  
    course_studied = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    date_of_birth = models.DateField()
    created_at = models.DateField(auto_now_add=True)  

    def __str__(self):
        return f"{self.surname} {self.first_name}"
    

