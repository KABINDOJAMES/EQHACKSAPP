from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from blog.models import *
from datetime import date, timedelta

# Create your views here.

def index(request):
    posts = Post.objects.filter(status=Post.PUBLISHED).order_by('?')[:4]
    newsarticles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED)[:2]
    notifications = Notifications.objects.filter(date_created=date.today())

    context = {
        'posts':posts,
        'newsarticles':newsarticles,
        'notifications':notifications,
    }

    return render(request, 'core/index.html', context)

def loginPage(request):
    if request.user.is_authenticated:
            return redirect('index')
            
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')
            return redirect('login-user')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully')

            return redirect('index')
        
        else:
            messages.error(request, 'Wrong password entered')
            return redirect('login-user')
    
    return render(request, 'core/login.html', {})


def registerPage(request):
    if request.user.is_authenticated:
            return redirect('index')

    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully registered')

            return redirect('index')
        else:
            messages.error(request, 'An error occured, try another username')
    
    return render(request, 'core/register.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('index')

def new_ticket(request):
    new_ticket = None
    notifications = Notifications.objects.filter(date_created=date.today())
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        location = post_data.get("location", None)

        new_ticket_form = NewTicketForm(data=request.POST)

        if new_ticket_form.is_valid():

            new_ticket = new_ticket_form.save(commit=False)

            if request.user.is_authenticated:
               owner = request.user.username
            else:
               owner = 'anonymous'

            new_ticket.owner = owner
            advisor_assigned = Advisor.objects.filter(available=True).filter(status=Advisor.ACTIVE).filter(Q(location__icontains=location))[:1]

            if advisor_assigned.count() < 1:
                new_ticket.status = Ticket.OPEN
                new_ticket.save()
                messages.info(request, 'Ticket submitted, wait for admin to assign you an advisor.')
                return redirect('tickets-list')
            else:
                user = User.objects.get(advisors=advisor_assigned)
                advisor_assigned_name = user.username
                new_ticket.advisor_assigned = advisor_assigned_name
                new_ticket.status = Ticket.INPROGRESS
                new_ticket.save()
                messages.success(request, 'Ticket successfully submitted and advisor automatically allocated.')
                return redirect('tickets-list')
 
    else:
        new_ticket_form = NewTicketForm()

    return render(request, 'core/new-ticket.html', {'new_ticket_form':new_ticket_form, 'notifications':notifications})

def tickets_list(request):

    notifications = Notifications.objects.filter(date_created=date.today())

    if request.user.is_authenticated:
        owner = request.user.username
        tickets = Ticket.objects.filter(owner=owner)
    else:
        messages.error(request, 'You are required to login to view your tickets. However you can create a ticket as an anonymous user.')
        return redirect('new-ticket')
    
    context = {
        'tickets':tickets,
        'notifications':notifications,
    }

    return render(request, 'core/tickets-list.html', context)

@login_required(login_url="login-user")
def ticket_detail(request, ticket_id):
    owner = request.user.username

    ticket = get_object_or_404(Ticket, ticket_id=ticket_id, owner=owner)
    previous_feedbacks = Feedback.objects.filter(submitted_by=ticket.owner).filter(ticket=ticket)#.order_by('-date_created')

    if request.method == 'POST':
        post_data = request.POST.copy()
        content = post_data.get("content", None)

        feedback = Feedback()
        feedback.content = content
        feedback.submitted_by = request.user.username
        feedback.ticket = ticket
        feedback.save()
        messages.success(request, 'Feedback successfully submitted.')
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'ticket':ticket,
        'previous_feedbacks':previous_feedbacks,
    }

    return render(request, 'core/ticket-detail.html', context)

def contact(request):

    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        contact_number = post_data.get("contact_number", None)
        name = post_data.get("name", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)
        enquiry = GeneralEnquiry()
        enquiry.email = email
        enquiry.conatct_number = contact_number
        enquiry.name = name
        enquiry.subject = subject
        enquiry.message = message
        
        # save in model
        enquiry.save()
        messages.success(request, 'Your request has been received. We will get back to you shortly')
        return redirect(request.META.get('HTTP_REFERER'))
       
    return render(request, 'core/index.html')

def donate(request):

    owner = None
    new_donation = None
    donate_profiles = None

    if request.user.is_authenticated:
        owner = request.user.username
        donate_profiles = Donor.objects.filter(owner=owner)

    if request.method == "POST":
        donation_form = DonateForm(data=request.POST)

        if donation_form.is_valid():

            new_donation = donation_form.save(commit=False)

            if request.user.is_authenticated:
               owner = request.user.username
               new_donation.owner = owner
               new_donation.save()
               messages.success(request, 'Thank you for your donation.')

            else:
               owner = "Anonymous"
               new_donation.owner = owner
               new_donation.save()
               messages.success(request, 'Thank you for your donation. Consider signing up to be able to track your donations.')          
        else:
            messages.error(request, "An error occurred. Try again.")
    else:
        donation_form = DonateForm()

    context = {
        'donate_profiles':donate_profiles,
        'donation_form':donation_form,
    }
    return render(request, 'core/donate.html', context)
     
def search(request):
    query = request.GET.get('q', '')

    posts = Post.objects.filter(status=Post.PUBLISHED).filter(Q(title__icontains=query) | Q(content__icontains=query))[:10]
    news_articles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED).filter(Q(title__icontains=query) | Q(content__icontains=query))[:10]

    posts_count = posts.count()
    newsarticles_count = news_articles.count()

    # declare search object not empty
    Empty = False
    recommendedposts = None

    # else declare search object empty and return recommended articles
    if posts.count() < 1:
        if news_articles.count() < 1:
            Empty = True
            recommendedposts = Post.objects.filter(status=Post.PUBLISHED).order_by('-updated_on')[:4]

    context = {
       'newsarticles':news_articles,
        'query':query,
        'posts_count':posts_count,
        'newsarticles_count':newsarticles_count,
        'posts':posts,
        'Empty':Empty,
        'recommendedposts':recommendedposts
                                               
    }

    return render(request, 'blog/search.html', context)
  
def robots_txt(request):
    text = [
        "User-Agent : *",
        "Disallow : /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")


def page_not_found(request, exception):
   
    return render(request, 'core/null.html', status=404)
