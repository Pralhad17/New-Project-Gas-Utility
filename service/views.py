# consumer_services/views.py
from django.shortcuts import render, redirect
from .forms import ServiceRequestForm
from .models import ServiceRequest
from .forms import ServiceRequestForm, UserRegistrationForm, LoginForm
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

#  Home Page

def home(request):
    return render(request,'service/home.html')

# Customer and Admin Login

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('admin_home')  # Redirect to admin's home page
            else:
                login(request, user)
                return redirect('user_home')  # Redirect to user's home page
    else:
        form = LoginForm()
    return render(request, 'service/login.html', {'form': form})

# List Of User

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'service/user_list.html', {'users': users})



# Admin and Customer Registration

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'service/register.html', {'form': form})

#  Customer Home Page

def user_home(request):
    return render(request, 'service/userhome.html')

# Service List

@login_required
def service_request_list(request):
    user = request.user  # Get the logged-in user
    service_requests = ServiceRequest.objects.filter(customer=user)
    
    context = {'service_requests': service_requests}
    return render(request, 'service/service_request_list.html', context)

# Create Service Request Form

# def create_service_request(request):
#     if request.method == 'POST':
#         form = ServiceRequestForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('service_request_list')
#     else:
#         form = ServiceRequestForm()
#     return render(request, 'service/create_service_request.html', {'form': form})


#  Delete User 

def delete_service_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        service_request.delete()
        return redirect('service_request_list')
    return render(request, 'service/delete_service_request.html', {'service_request': service_request})

#  Submit The Request

def submit_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('user_home')  # Redirect to user's home page after submission
    else:
        form = ServiceRequestForm()
    return render(request, 'service/submit_service_request.html', {'form': form})


# Admin Request View all User

def admin_service_requests(request):
     # Get the logged-in user
    service_requests = ServiceRequest.objects.all()
    
    context = {'service_requests': service_requests}
    return render(request, 'service/user_service_request.html', context)


# Admin Home Page

@login_required
def admin_home(request):
    # Calculate counts of service requests based on status
    pending_requests = ServiceRequest.objects.filter(status='Pending').count()
    in_progress_requests = ServiceRequest.objects.filter(status='In Progress').count()
    resolved_requests = ServiceRequest.objects.filter(status='Resolved').count()

    return render(request, 'service/adminhome.html', {
        'pending_requests': pending_requests,
        'in_progress_requests': in_progress_requests,
        'resolved_requests': resolved_requests,
    })

# User submit Request

@login_required
def user_submit_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('user_home')
    else:
        form = ServiceRequestForm()
    return render(request, 'service/submit_service_request.html', {'form': form})



# Delete User Request

@login_required
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('user_list')


def user_logout(request):
    logout(request)
    return redirect('home') 


# @login_required
# @user_passes_test(lambda user: user.is_staff, login_url='home')
# def user_service_request_view(request):
#     user_service = ServiceRequest.objects.filter(customer=request.user)
#     return render(request, 'service/user_service_requests.html', {'user_service': user_service})

# @login_required
# @user_passes_test(lambda user: user.is_staff, login_url='home')
# def admin_service_request_view(request, request_id, new_status):
#     service_request = ServiceRequest.objects.get(id=request_id)

#     if new_status == 'in_progress':
#         service_request.status = 'In Progress'
#     elif new_status == 'resolved':
#         service_request.status = 'Resolved'

#     service_request.save()

#     return redirect('admin_service_requests')





