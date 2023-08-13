from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_user),
    path('process_registration', views.process_registration),
    path('process_login', views.process_login),
    path('dashboard', views.welcome_page),
    path('jobs/new', views.create_job),
    path('process_new_job', views.process_new_job),
    path('logout', views.logout),
    path('jobs/<int:job_id>', views.view_job),
    path('jobs/edit/<int:job_id>', views.edit_job),
    path('update_job_process', views.update_job_process),
    path('jobs/delete/<int:job_id>', views.delete),
]