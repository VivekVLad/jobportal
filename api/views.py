from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from portal.models import Job
from .serializers import JobSerializer


class JobViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Job.objects.all()
    serializer_class = JobSerializer
