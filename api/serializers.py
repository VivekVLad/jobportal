from rest_framework import serializers
from portal.models import Job,Employer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['id','employer_name','address','about','industry','website']


class JobSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    class Meta:
        model = Job
        fields = ['id','employer','title','description','requirements','experience_min',
                  'experience_max','location','salary','posted_date','expiry_date'
        ]


