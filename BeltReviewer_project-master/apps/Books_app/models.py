# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from ..Users_app.models import User

NAME_REGEX = re.compile(r"(^[a-zA-Z /-]+$)")
# re.sub(' +',' ','The     quick brown    fox')
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Author, related_name='books')

class ReviewManager(models.Manager):
    def validateReview(self, postData):
        results ={'status': True, 'errors': []}
        #### Title validation
        if len(postData['title']) < 1:
            results['status'] = False
            results['errors'].append('Please enter a title')

        #### Author Validation
        if not postData['author'] and not postData['new_author']:
            results['status'] = False
            results['errors'].append('Please select or enter a new author')
        if not postData['author'] and re.match(NAME_REGEX, postData['new_author']) == None:
            results['status'] = False
            results['errors'].append('Invalid name for a new author')

        #### Review Validation
        if len(postData['review']) < 20:
            results['status'] = False
            results['errors'].append('Reviews must be at least 20 characters long')
       
        #### Rating Validation
        if int(postData['rating']) == 0:
            results['status'] = False
            results['errors'].append('Please enter a rating')

        return results

    def createReview(self, postData, userID):

        if not postData['author'] and postData['new_author']:##### creates a new author
            curAuthor = Author.objects.create(name = postData['new_author'])
        else:
            curAuthor = Author.objects.get(name = postData['author'])

        if len(Book.objects.filter(title = postData['title'])) < 1:##### creates a new book
            curBook = Book.objects.create(title = postData['title'], author=curAuthor)
        else:
            curBook = Book.objects.filter(title = postData['title'])[0]

        newReview = self.create(
            rating = postData['rating'],
            thisReview = postData['review'],
            book = curBook,
            reviewer = User.objects.get(id=userID),
        )

        return newReview

    def getReviewLists(self):
        #### returns a dictionary with two sets of reviews
        reviewLists = {
            'most_recent': self.all().order_by('-created_at')[:3],
            'all_others': self.all().order_by('-created_at')[3:],
        }
        return reviewLists

class Review(models.Model):
    rating = models.IntegerField()
    thisReview = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, related_name='reviews')
    reviewer = models.ForeignKey('Users_app.User', related_name='reviews')
    objects = ReviewManager()