from django.shortcuts import render, redirect

from .forms import CreateUserForms, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from . models import Record
from django.contrib import messages

# Create your views here.
def home(request):
    # return HttpResponse('Hello, World')

    return render(request, 'webapp/index.html')

def register(request):

    form = CreateUserForms()

    if request.method == "POST":

        form = CreateUserForms(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully")

            return redirect('my_login')

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)

#Login a User

def  my_login(request):
    
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')

            password = request.POST.get('password')

            user =  authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)


# Dashboard
@login_required(login_url='my_login')

def dashboard(request):

    my_records  = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)


# Create a record
@login_required(login_url='my_login')

def create_record(request):
    
    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")

            return redirect('dashboard')
        
    context = {'form': form}

    return render(request, 'webapp/create-record.html', context=context)


# Update a record
@login_required(login_url='my_login')

def update_record(request, pk):
    
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)
     
    if request.method == "POST":

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect('dashboard')
        
    context = {'form': form}
        
    return render(request, 'webapp/update-record.html', context=context)


# Read / view a singular record
@login_required(login_url='my_login')

def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record': all_records}

    return render(request, 'webapp/view-record.html', context=context)


# Delete A Record
@login_required(login_url='my_login')

def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect('dashboard')


# User logout
def user_logout(request):
    auth.logout(request)
    
    messages.success(request, "You've been logged out of your account")

    return redirect("my_login")


