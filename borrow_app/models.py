from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length = 250)

class Book(models.Model):
    title = models.CharField(max_length = 250)
    publish_date = models.DateField()
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    available = models.BooleanField(default=True)

class Borrower(models.Model):
    name = models.CharField(max_length = 250)
    phone = models.IntegerField()
    address = models.CharField(max_length = 450)

class BorrowRecord(models.Model):
    borrower = models.ForeignKey(Borrower,on_delete=models.CASCADE) 
    book = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    actual_return_date = models.DateField(blank=True,null=True)
    returned = models.BooleanField(default=False)

