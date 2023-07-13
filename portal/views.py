from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.db.models import F
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import *
from .forms import JobForm
# Create your views here.

class EmployerRegistrationView(View):
    def get(self,request):
        return render(request,'portal/employer_registration.html')
    
    def post(self,request):
        User = get_user_model()
        user = User()
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_employer = True
        pwd = request.POST['password']
        user.set_password(raw_password=pwd)
        user.save()

        employer = Employer()
        employer.user = user
        employer.employer_name = request.POST['name']
        employer.address = request.POST['address']
        employer.about = request.POST['about']
        employer.industry = request.POST['industry']
        employer.website = request.POST['website']
        employer.save()
        messages.success(request, 'Registration Successful,Now you can Login')
        return redirect('login')


class SeekerRegistrationView(View):
    def get(self,request):
        return render(request,'portal/seeker_registration.html')
    
    def post(self,request):
        User = get_user_model()
        user = User()
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_employer = False
        pwd = request.POST['password']
        user.set_password(raw_password=pwd)

        seeker = Seeker()
        seeker.user = user
        seeker.gender = request.POST['gender']
        seeker.address = request.POST['address']
        seeker.about = request.POST['about']
        seeker.dob = request.POST['dob']
        seeker.resume = request.FILES['resume']
        user.save()
        seeker.save()
        messages.success(request, 'Registration Successful,Now you can Login')
        return redirect('login')
    

class EmployerIndexView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request):
        context = {}
        employer = Employer.objects.get(user_id=request.user.id)
        context['employer'] = employer
        context['jobs'] = Job.objects.filter(employer_id = employer.id)
        return render(request,'portal/employer_home.html',context)
    

class JobCreateView(LoginRequiredMixin,CreateView):
    login_url = "/login/"
    model = Job
    form_class = JobForm
    template_name = 'portal/job_create.html'
    success_url = reverse_lazy('employer_home')
    
    def form_valid(self, form):
        form.instance.employer_id = Employer.objects.get(user_id=self.request.user.id).id
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin,DeleteView):
    login_url = "/login/"
    model = Job
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employer_home')


class JobUpdateView(LoginRequiredMixin,UpdateView):
    login_url = "/login/"
    model = Job
    form_class = JobForm
    pk_url_kwarg = 'pk'
    template_name = 'portal/job_update_form.html'
    success_url = reverse_lazy('employer_home')


class SeekerIndexView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        context = {}
        context['jobs'] = Job.objects.all()
        # context['status'] = JobApplication.objects.get(applicant_email=request.user.email).status
        return render(request,'portal/seeker_home.html',context)
    

class ApplicationView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,pk):
        context = {}
        try:
            job = get_object_or_404(Job,pk=pk)
        except:
            messages.error(request,"Job not available!")
            return redirect('seeker_home')
        context['job'] = job
        context['employer'] = Employer.objects.get(pk=job.employer_id).employer_name
        context['website'] = Employer.objects.get(pk=job.employer_id).website
        try:
            context['status'] = JobApplication.objects.get(job_id=pk, applicant_id=request.user.id).status
        except:
            pass
        return render(request,'portal/application.html',context)
    
    def post(self,request,pk):
        application = JobApplication()
        try:
            job = get_object_or_404(Job,pk=pk)
        except:
            messages.error(request,"Job not available!")
            return redirect('seeker_home')
        application.applicant_id = request.user.id
        application.employer_id = job.employer_id
        application.job_id = pk
        application.status = 'Applied'
        application.save()
        messages.success(request,"Applied Successfully...!")
        return redirect('seeker_home')


class ApplicationsListView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        context = {}
        applications = JobApplication.objects.filter(applicant_id = request.user.id).prefetch_related('job')
        context['applications'] = applications
        return render(request,'portal/applied_jobs.html',context)


class EmployerApplicationsListView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        context = {}
        employer_id = Employer.objects.get(user_id=request.user.id).id
        applications = JobApplication.objects.filter(employer_id=employer_id).prefetch_related('applicant')
        context['applications'] = applications
        return render(request,'portal/employer_applied_jobs.html',context)


class ChangeStatusView(LoginRequiredMixin,View):
    def post(self,request,pk):
        application = JobApplication.objects.get(pk=pk)
        status = request.POST.get('status')
        application.status = status
        application.save()
        return redirect('employer_applied_list')
    

class DownloadResume(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,request,pk):
        print(pk)
        applicant = Seeker.objects.get(pk=pk)
        resume_file = applicant.resume.path
        return FileResponse(open(resume_file, 'rb'), as_attachment=True)