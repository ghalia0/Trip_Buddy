from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Travel

def index(request):
    return render(request, 'index.html')

def travel(request):
    
    if request.session['user_id']:
        context= {'user': User.objects.get(id= request.session['user_id']), 'travels' : Travel.objects.all(),  'others': Travel.objects.all().exclude(join__id=request.session['user_id']) }
        return render(request, 'travel.html', context)
    else:
        return redirect('/')

def add_travel(request):
    context= {'user': User.objects.get(id= request.session['user_id'])}
    return render(request, 'add_travel.html', context)

def submit_travel(request):
    if request.method == 'POST':
        response_from_models= Travel.objects.validator(request.POST)
        if len(response_from_models) > 0:
            for error in response_from_models:
                messages.error(request, error)
            return redirect("/add_trip")
        else:
            Travel.objects.create(destination=request.POST['destination'], description=request.POST['description'], creator=User.objects.get(id= request.session['user_id']), start=request.POST['start'], end=request.POST['end'])
            return redirect("/travel")

def edit_travel(request, travel_id):
    context= {'user': User.objects.get(id= request.session['user_id']), 'traveles':  Travel.objects.get(id= travel_id),}
    
    return render(request, 'edit_travel.html', context)


def edit_submit(request, travel_id):
    if request.method == 'POST':
        response_from_models= Travel.objects.validator(request.POST)
        if len(response_from_models) > 0:
            for error in response_from_models:
                messages.error(request, error)
            return redirect(f'/edit_travel/{travel_id}')
        else: 
            update = Travel.objects.get(id=travel_id)
            if request.POST['destination']:
                update.destination = request.POST['destination']
            if request.POST['description']:
                update.description = request.POST['description']
            
            if request.POST['start']:
                update.start = request.POST['start']
            
            if request.POST['end']:
                update.end = request.POST['end']
            update.save()
        return redirect('/travel')

def delete_travel(request, travel_id):
    d = Travel.objects.get(id= travel_id)
    d.delete()
    return redirect('/travel')

def view(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/travel')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['user_id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'view_trip.html', context)

def join(request, travel_id):
    if request.method == "GET":
        return redirect('/')
    joiner= Travel.objects.join(request.session["user_id"], travel_id)
    
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travel')



def registration(request):
    if request.method == 'POST':
        response_from_models= User.objects.basic_validator(request.POST)
        if len(response_from_models) > 0:
            for error in response_from_models:
                messages.error(request, error)
            return redirect("/")
        else:
            if request.POST['submit'] == 'register':
                fname= request.POST['first_name']
                lname= request.POST['last_name']
                email= request.POST['email']
                user_salt= bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(request.POST['password'].encode(), user_salt).decode()
                this_user=User.objects.create(first_name=fname, last_name= lname, email=email, password= hashed_password , salt=user_salt)
                request.session['user_id'] = this_user.id
                # return redirect(f'wishes/{user.id}')
                return redirect('/travel')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user =user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/travel')
            else:
                messages.error(request, 'Password is incorrect!')
                return redirect('/')
        if not user:
            errors= User.objects.validator(request.POST)
            if len(errors) > 0:
                for error in errors:
                    messages.error(request, error)
                    
                    return redirect("/")


def logout(request):
    
    # request.session.clear()
    del request.session['user_id']
    messages.success(request, "You have successfully logged out")
    return redirect('/')