from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import uuid
from django.shortcuts import reverse

# Create your models here.

#Advisors or voluntias model
class Advisor(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS = (
      (ACTIVE, 'active'),
      (INACTIVE, 'inactive'),
    )

    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advisors')
    location = models.TextField()
    contact_number = models.CharField(max_length=30)
    approval_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS, default=INACTIVE)
    available = models.BooleanField(default=False)

    class Meta:
        ordering = ['-approval_date']

#Donor model
class Donor(models.Model):
    owner = models.CharField(max_length=50, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    date_donated = models.DateTimeField(auto_now_add=True)
    amount_donated = models.IntegerField()

    class Meta:
        ordering = ['-date_donated']

#Ticket model, Problem report and tracking
class Ticket(models.Model):
    OPEN = 'open'
    INPROGRESS = 'inprogress'
    CLOSED = 'closed'

    TICKET_STATUS = (
        (OPEN, 'open'),
        (INPROGRESS, 'inprogress'),
        (CLOSED, 'closed'),
    )

    owner = models.CharField(max_length=50, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    advisor_assigned = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=100)
    affected_person_contact = models.CharField(max_length=100, null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=TICKET_STATUS, default=OPEN)
    title = models.CharField(max_length=150, null=True, blank=True)
    ticket_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-open_date']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ticket-detail', args = [self.ticket_id])

#User feedback model
class Feedback(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='feedbacks')
    submitted_by = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(null=True, blank=True)
    reply_created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

class Notifications(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'notifications'

#General Enquiry model 
class GeneralEnquiry(models.Model):

    RECEIVED = 'received'
    RESPONDED = 'responded'
    CLOSED = 'closed'

    MESSAGE = (
       (RECEIVED, 'received'),
       (RESPONDED, 'responded'),
       (CLOSED, 'closed'),
    )

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    conatct_number = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MESSAGE, default=RECEIVED)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'General Enquiries'

