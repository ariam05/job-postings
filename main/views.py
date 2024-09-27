from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job
import bcrypt

# Create your views here.
def register_user(request):
    if 'user_id' in request.session:
        return redirect('/dashboard') 
    context = {
        'all_users': User.objects.all()
    }
    return render(request, 'register.html', context)

def process_registration(request):
    # Check if the email already exists in the database
    if User.objects.filter(email=request.POST['email']).exists():
        messages.error(request, "The email you have provided is already associated with an account. Please login or reset your password")
        return redirect('/')
    
    # Validate other fields
    errs = User.objects.user_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    else:
        # Hash the password and create the user if no errors
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(password, "\n", hashed)
        user = User.objects.create(
            f_name=request.POST['f_name'],
            l_name=request.POST['l_name'],
            email=request.POST['email'],
            password=hashed,
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard')


def process_login(request):
    errs = User.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg) 
        return redirect('/')
    else:
        user_email = User.objects.filter(email=request.POST['email'])
        if user_email:
            logged_user = user_email[0]
            # Verifying password
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id 
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid Email or Password")  # Display password error
        else:
            messages.error(request, "Invalid Email or Password")  # Handle case when email is not found
        return redirect('/')




def welcome_page(request):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'all_jobs': Job.objects.all()
    }
    return render(request, 'welcome_dashboard.html', context)

def create_job(request):
    context = {
        'all_jobs': Job.objects.all(),
        'logged_in_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'create_new_job.html', context)

def process_new_job(request):
    errs = User.objects.create_job_validator(request.POST)
    print(errs)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/jobs/new')
    else:
        Job.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            submitted_by = User.objects.get(id=request.POST['user_id'])
            
        )
        return redirect('/dashboard')



def view_job(request, job_id):
    context = {
        'selected_job': Job.objects.get(id=job_id),
        'logged_in_user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'view_job_details.html', context)


def edit_job(request, job_id):
    context = {
        'edit_job':Job.objects.get(id=job_id),
        'logged_in_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_job.html', context)

def update_job_process(request):
    errs = User.objects.create_job_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect(f'/jobs/edit/{job.id}')
    else:
        job_to_update = Job.objects.get(id=request.POST['job_id'])
        job_to_update.title = request.POST['title']
        job_to_update.description = request.POST['description']
        job_to_update.location = request.POST['location']
        job_to_update.save() #updating each imput in edit page
        return redirect('/dashboard')


def delete(request, job_id):
    job_to_delete = Job.objects.get(id=job_id)
    job_to_delete.delete()
    return redirect('/dashboard')



def logout(request):
    request.session.clear()
    return redirect('/')