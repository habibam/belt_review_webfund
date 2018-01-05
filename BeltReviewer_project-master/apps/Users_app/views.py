# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import User, UserManager
from django.contrib import messages

# Create your views here.

############################################  Login/Registration  ############################
def index(request):
    return render(request, 'Users_app/index.html')

def register(request):
    results = User.objects.validateReg(request.POST)
    if results['status']:
        newUser = User.objects.createUser(request.POST)
        genSessions(request, newUser)
        return redirect('/books')
    else:
        genErrorMessages(request, results)
        return redirect('/')
        
def login(request):
    results = User.objects.validateLogin(request.POST)
    if  results['status']:
        # return genSessions(request, results['user'])
        genSessions(request, results['user'])
        return redirect('/books')
    else:
        genErrorMessages(request, results)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

############################################  Specific User Page  ############################
def getUser(request, getID):
    tempUser = User.objects.get(id = getID)
    context ={
        'alias': tempUser.alias,
        'name': tempUser.name,
        'email': tempUser.email,
        'reviews': User.objects.get(id=getID).reviews.all(),
        'count': len(User.objects.get(id=getID).reviews.all()),
    }
    return render(request, 'Users_app/users.html', context)

############################################  Helper Functions  ############################
def genSessions(request, user):
    request.session['name'] = user.name
    request.session['alias'] = user.alias
    request.session['email'] = user.email
    request.session['userID'] = user.id

def genErrorMessages(request, results):
    for error in results['errors']:
        messages.error(request, error)