from django.shortcuts import render
from django.contrib.auth.views import LoginView,LogoutView

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        if self.request.user.is_employer:
            success_url = 'portal/employer_home'
            return success_url
        else:
            success_url = 'portal/seeker_home'
            return success_url

class CustomLogoutView(LogoutView):
    template_name = "registration/login.html"
    
