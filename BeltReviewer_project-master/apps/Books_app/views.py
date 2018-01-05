# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from models import Review, ReviewManager, Author, Book

############################################  Main page  ############################
def books(request):
    reviewLists = Review.objects.getReviewLists()
    context = {
        'alias': request.session['alias'],
        'first_3': reviewLists['most_recent'],
        'otherBooks': reviewLists['all_others'],
    }
    return render(request, 'Books_app/books.html', context)


############################################  Specific Book  ############################
def getBook(request, bookID):
    curBook = Book.objects.get(id=bookID)
    context ={
        'newReview':"", 
        'title': curBook.title,
        'author': curBook.author.name,
        'reviews': curBook.reviews.all().order_by('created_at'),
        'bookID': bookID,
    }
    return render(request, 'Books_app/bookDetails.html', context)


############################################  Reviews  ############################
def addForm(request):
    context = {
        'title': '',
        'new_author': '',
        'review': '',
        'authors': Author.objects.all().order_by('name'),
    }
    return render(request, 'Books_app/add.html', context)

##### create new review from ^
def addReview(request):
    results = Review.objects.validateReview(request.POST)

    if results['status']:
        Review.objects.createReview(request.POST, request.session['userID'])
        return redirect('/books')
    else:
        #### saves your text in case it errors out
        context = {
            'title': request.POST['title'],
            'new_author': request.POST['new_author'],
            'review': request.POST['review'],
            'authors': Author.objects.all().order_by('name'),
        }
        # for error in results['errors']:
        #     messages.error(request, error)
        genErrorMessages(request, results)
        return render(request, 'Books_app/add.html', context)

##### from specific book page
def addAditionalReview(request, bookID):  
    results = Review.objects.validateReview(request.POST)

    if results['status']:
        Review.objects.createReview(request.POST, request.session['userID'])
        return redirect('/books')
    else:
        # for error in results['errors']:
        #     messages.error(request, error)
        genErrorMessages(request, results)

        #### saves your text in case it errors out
        curBook = Book.objects.get(id=bookID)
        context = {
            'newReview': request.POST['review'],
            'title': curBook.title,
            'author': curBook.author.name,
            'reviews': curBook.reviews.all().order_by('-created_at'),
            'bookID': bookID,
        }
        return render(request, 'Books_app/bookDetails.html', context)

##### destroy
def deleteReview(request, bookID, reviewID):
    #### prevents tampering with urls to delete
    if request.session['userID'] != Review.objects.get(id=reviewID).reviewer.id or 'email' not in request.session:
        return redirect('/books/{}'.format(bookID))
    else:
        Review.objects.get(id=reviewID).delete()
        return redirect('/books/{}'.format(bookID))

############################################  Helper functions ############################
def genErrorMessages(request, results):
    for error in results['errors']:
        messages.error(request, error)