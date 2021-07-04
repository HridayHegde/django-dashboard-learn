from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    datetime_created = models.DateTimeField(verbose_name='time created', auto_now_add=True)
    completed = models.BooleanField(default=False)
    duedate = models.DateTimeField(verbose_name='due date')
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=900)
    customer_name = models.CharField(max_length=200)
    customer_email = models.CharField(max_length=200)
    completed_by = models.CharField(max_length=100,default="")
    temp = models.CharField(max_length=300)
    def __str__(self):
        return self.ticket_id

    
    

