from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Plan
from django.db.models import Count

def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, "index/index.html")
# Create your views here.
def register(request):
    #because its short :P
    req = request.POST
    PostData = {
        'name': req['name'],
        'email': req['email'],
        'password': req['password'],
        'conf_password': req['conf_password']
    }
    #if there is no error returned
    if not User.objects.register(PostData):
        #then store new_user into a session so we could use it on the success page
        new_user_id = User.objects.create_user(PostData)
        request.session['user_id'] = new_user_id
        #then send it to the success page
        return redirect('/success')
    #else if we got the errors as array, then display it and then redirect to the regi page
    for error in User.objects.register(PostData):
        messages.error(request, error)
    request.session['loginErr'] = False
    return redirect('/')
def login(request):
    req = request.POST
    PostData = {
        'email': req['email'],
        'password': req['password']
    }
    if not User.objects.login(PostData):
        user_id = User.objects.get(email=PostData['email']).id
        request.session['user_id'] = user_id
        return redirect('/success')
    for error in User.objects.login(PostData):
        messages.error(request, error)
    request.session['loginErr'] = True
    return redirect('/')
def success(request):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        plan = Plan.objects.all()
        context = {
            'user': user,
            'plans':plan,
        }
        return render(request, "index/success.html", context)
    return redirect('/')
def add(request):
    context = {
        'user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'index/add.html', context)
def add_plans(request):
    req = request.POST
    PostData = {
        'destination': req['destination'],
        'description': req['description'],
        'start_date': req['start_date'],
        'end_date': req['end_date'],
        'user': User.objects.get(id=request.session['user_id'])
    }
    plan = Plan.objects.add_plans(PostData)
    return redirect('/success')
def show_info(request, id):
    context = {
        'plan': Plan.objects.get(id=id)
    }
    return render(request, "index/info.html", context)
def join(request):
    PostData = {
        'user_id': request.session['user_id']
    }
    return redirect("/success")
def logout(request):
    request.session.clear()
    return redirect('/')
