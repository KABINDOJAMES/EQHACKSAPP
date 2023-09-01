from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from EQHACKSAPP import settings
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.
def blog_index(request):

    posts = Post.objects.filter(status=Post.PUBLISHED).order_by('?')[:6]
    newsarticles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED).order_by('?')[:4]

    context = {
        'newsarticles':newsarticles,
        'posts':posts,
    }

    return render(request, 'blog/index.html', context)

def news_detail(request, slug):
    newsarticle = get_object_or_404(NewsArticle, slug=slug, status=NewsArticle.PUBLISHED)
    comments = newsarticle.newscomments.filter(status=NewsComment.PUBLISHED)
    newsarticle.views += 1
    newsarticle.save()
    new_newscomment = None

    #retrieve related articles
    query = newsarticle.title + newsarticle.content
    related_articles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED).filter(Q(title__icontains=query) | Q(content__icontains=query)).exclude(slug=slug).order_by('?')[:4]


    if related_articles.count() < 1:
        related_articles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED).exclude(slug=slug).order_by('?')[:4]
    # Comment posted
    if request.method == 'POST':
        newscomment_form = NewsCommentForm(data=request.POST)

        if newscomment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_newscomment = newscomment_form.save(commit=False)
            # Assign the current news article to the comment
            new_newscomment.newsarticle = newsarticle
            # Save the comment to the database
            new_newscomment.save()
            messages.info(request, 'Comment is awaiting admin approval')
            return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        newscomment_form = NewsCommentForm()

    context = {
        'newsarticle':newsarticle,
        'related_articles':related_articles,
        'comments':comments,
        'newscomment_form':newscomment_form,

    }
    return render(request, 'blog/news-detail.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.PUBLISHED)
    comments = post.postcomments.filter(status=PostComment.PUBLISHED)
    post.views += 1
    post.save()
    new_postcomment = None

    #retrieve related posts
    query = post.title + post.content
    related_posts = Post.objects.filter(status=Post.PUBLISHED).filter(Q(title__icontains=query) | Q(content__icontains=query)).exclude(slug=slug)

    if related_posts.count() < 1:
        related_posts = Post.objects.filter(status=Post.PUBLISHED).exclude(slug=slug).order_by('?')[:4]

    newsarticles = NewsArticle.objects.filter(status=NewsArticle.PUBLISHED).order_by('?')[:4]

    # Comment posted
    if request.method == 'POST':
        postcomment_form = PostCommentForm(data=request.POST)

        if postcomment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_postcomment = postcomment_form.save(commit=False)
            # Assign the current post to the comment
            new_postcomment.post = post
            # Save the comment to the database
            new_postcomment.save()
            messages.info(request, 'Comment is awaiting admin approval')
            return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        postcomment_form = PostCommentForm()

    context = {
        'post':post,
        'related_posts':related_posts,
        'newsarticles':newsarticles,
        'comments':comments,
        'postcomment_form':postcomment_form,
    }
    return render(request, 'blog/post-detail.html', context)

def subscribe(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        email = email.lower()
        name = post_data.get("name", None)
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email.lower()
        subscribedUsers.name = name

        if SubscribedUsers.objects.filter(email=email).exists():
            messages.error(request, 'Error!!! Email already exists')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            subscribedUsers.save()
            messages.success(request, 'Thanks for subscribing.')
            # send a confirmation mail
            subject = 'NewsLetter Subscription'
            message = 'Hello ' + name + ', You have successfully subscribed to our newsletter. We are happy to see you join our community. Keep checking your email for weekly updates. . . Please do not reply on this email.'
            #email_from = settings.EMAIL_HOST_USER
            """ send_mail(
                  subject,
                  message, 
                  email_from, 
                  [email, ],
                  fail_silently = False,
            ) """
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'An error occured')

    return render(request, 'blog/index.html')
 

