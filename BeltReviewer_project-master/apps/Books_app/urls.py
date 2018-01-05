from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.books),
    url(r'^add$', views.addForm),
    url(r'^addReview$', views.addReview),
    url(r'^(?P<bookID>\d+)$', views.getBook),
    url(r'^(?P<bookID>\d+)/addReview$', views.addAditionalReview),
    url(r'^(?P<bookID>\d+)/delete/(?P<reviewID>\d+)$', views.deleteReview),
]
