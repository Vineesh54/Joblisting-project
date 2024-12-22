from django.urls import path
from .views import JobListAPIView, JobCreateAPIView

urlpatterns = [
    path('', JobListAPIView.as_view(), name='job-list'),
    path('add/', JobCreateAPIView.as_view(), name='job-create'),
]
