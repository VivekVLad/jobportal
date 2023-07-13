from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=200,null=False)
    address = models.CharField(max_length=400,blank=True,default='Not Provided')
    about = models.TextField(blank=True,default='Not Provided')
    industry = models.CharField(max_length=60,blank=True,default='Not Provided')
    website = models.URLField(blank=True,default='Not Provided')

    def __str__(self) -> str:
        return self.employer_name


class Seeker(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE,'Male'),
        (FEMALE,'Female')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=None)
    address = models.CharField(max_length=400,blank=True,default='Not Provided')
    about = models.TextField(blank=True,default='Not Provided')
    dob = models.DateField(null=False)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self) -> str:
        return self.user.username
    

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    experience_min = models.IntegerField()
    experience_max = models.IntegerField()
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    posted_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()

    def __str__(self):
        return self.title
    

class JobApplication(models.Model):
    applicant = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Applied')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant.user.first_name} {self.applicant.user.last_name}'