from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Employer)
admin.site.register(Seeker)
admin.site.register(Job)
admin.site.register(JobApplication)
