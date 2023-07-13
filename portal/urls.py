from django.urls import path
from .views import *

urlpatterns = [
    path('employer_registration/',EmployerRegistrationView.as_view(),name='employer_registration'),
    path('seeker_registration/',SeekerRegistrationView.as_view(),name='seeker_registration'),
    path('employer_home/',EmployerIndexView.as_view(),name='employer_home'),
    path('seeker_home/',SeekerIndexView.as_view(),name='seeker_home'),
    path('job/create/',JobCreateView.as_view(),name='job-create'),
    path('job/<int:pk>/delete/',JobDeleteView.as_view(),name='job-delete'),
    path('job/<int:pk>/update/',JobUpdateView.as_view(),name='job-update'),
    path('apply/<int:pk>/',ApplicationView.as_view(),name='apply'),
    path('applied/',ApplicationsListView.as_view(),name='applied_list'),
    path('employer_applied/',EmployerApplicationsListView.as_view(),name='employer_applied_list'),
    path('changestatus/<int:pk>/',ChangeStatusView.as_view(),name='change_status'),
    path('resumedownload/<int:pk>/',DownloadResume.as_view(),name='download'),
]