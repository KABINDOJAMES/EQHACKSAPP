from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.sites.models import Site
from .models import *

# Register your models here.

admin.site.unregister(Site)
admin.site.index_title  =  "EQUITY PLATFORM BLOGSITE MANAGEMENT"
admin.site.site_header = "SITE MANAGEMENT"

class SiteAdmin(admin.ModelAdmin): 
    list_display = ('id', 'domain', 'name')


class PostCommentItemInline(admin.TabularInline):
    model = PostComment
    raw_id_fields = ['post']
    extra = 0

class NewscommentItemInline(admin.TabularInline):
    model = NewsComment
    raw_id_fields = ['newsarticle']
    extra = 0


class PostAdmin(SummernoteModelAdmin):
    search_fields = ['title', 'content', 'created_on', 'updated_on']
    list_display = ['title', 'created_on', 'updated_on', 'status']
    list_filter = ['created_on', 'updated_on', 'status']
    inlines = [PostCommentItemInline]
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    actions = ['make_published']

    @admin.action(description='Mark selected posts as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status=Post.PUBLISHED)
        self.message_user(request, ngettext(
            '%d Post was successfully marked as published.',
            '%d Posts were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)

class PostCommentAdmin(admin.ModelAdmin):
    search_fields = ['owner', 'post__title', 'created_on', 'approved_on']
    list_display = ['owner', 'post', 'created_on', 'approved_on']
    list_filter = ['owner', 'post', 'created_on', 'approved_on']
   
    actions = ['make_published']

    @admin.action(description='Mark selected post comments as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status=PostComment.PUBLISHED)
        self.message_user(request, ngettext(
            '%d Post comment was successfully marked as published.',
            '%d Post comments were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)

class NewsArticleAdmin(SummernoteModelAdmin):
    search_fields = ['title', 'content', 'created_on', 'updated_on',]
    list_display = ['title', 'created_on', 'updated_on', 'status',]
    list_filter = ['created_on', 'updated_on', 'status']
    inlines = [NewscommentItemInline]
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    actions = ['make_published']

    @admin.action(description='Mark selected news articles as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status=NewsArticle.PUBLISHED)
        self.message_user(request, ngettext(
            '%d News article was successfully marked as published.',
            '%d News articles were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)


class NewsCommentAdmin(admin.ModelAdmin):
    search_fields = ['owner', 'newsarticle__title', 'created_on', 'approved_on']
    list_display = ['owner', 'newsarticle', 'created_on', 'approved_on']
    list_filter = ['owner', 'newsarticle', 'created_on', 'approved_on']
    
    actions = ['make_published']

    @admin.action(description='Mark selected news comments as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status=NewsComment.PUBLISHED)
        self.message_user(request, ngettext(
            '%d News comment was successfully marked as published.',
            '%d News comments were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)

class SubscribedUsersAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email', 'subscribe_date']
    list_display = ['name', 'email', 'subscribe_date']
    list_filter = ['name', 'email', 'subscribe_date']

admin.site.register(Site, SiteAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(NewsComment, NewsCommentAdmin)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)

