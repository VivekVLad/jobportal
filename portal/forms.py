from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','requirements','location','salary','expiry_date','experience_min','experience_max']
