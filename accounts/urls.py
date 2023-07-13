from django.urls import include, path
from .views import *

urlpatterns = [
    path('',CustomLoginView.as_view(),name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]