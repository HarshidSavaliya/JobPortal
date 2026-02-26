from django.urls import path
from . import views 

urlpatterns = [
    path('post_job/', views.post_job, name='post_job'),
]
