from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import *

# Register your models here.

class AdvisorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'location', 'contact_number', 'approval_date', 'status', 'available']
    list_display = ['name', 'location', 'contact_number', 'status', 'available']
    list_filter = ['name', 'location', 'contact_number', 'status', 'available']
    actions = ['advisor_active', 'advisor_inactive']
    
    @admin.action(description='Mark selected advisors as active.')
    def advisor_active(self, request, queryset):
        updated = queryset.update(status=Advisor.ACTIVE)
        self.message_user(request, ngettext(
            '%d Advisor was successfully marked as active.',
            '%d Advisors were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected advisors as inactive')
    def advisor_inactive(self, request, queryset):
        updated = queryset.update(status=Advisor.INACTIVE)
        self.message_user(request, ngettext(
            '%d Advisor was successfully marked as inactive.',
            '%d Advisors were successfully marked as inactive.',
            updated,
        ) % updated, messages.SUCCESS)

class DonorAdmin(admin.ModelAdmin):
    search_fields = ['owner', 'location', 'date_donated', 'contact_number', 'amount_donated']
    list_display = ['owner', 'location', 'date_donated', 'contact_number', 'amount_donated']
    list_filter = ['owner', 'location', 'date_donated', 'contact_number', 'amount_donated']

class FeedbackItemInline(admin.TabularInline):
    model = Feedback
    raw_id_fields = ['ticket']
    extra = 0

class TicketAdmin(admin.ModelAdmin):
    search_fields = ['owner', 'location', 'advisor_assigned', 'contact_number', 'affected_person_contact', 'ticket_id', 'title', 'description']
    list_display = ['owner', 'advisor_assigned', 'title', 'open_date', 'status']
    list_filter = ['owner', 'location', 'advisor_assigned', 'open_date', 'status']
    inlines = [FeedbackItemInline]
    actions = ['ticket_inprogress', 'ticket_closed']
    
    @admin.action(description='Mark selected tickets in progress.')
    def ticket_inprogress(self, request, queryset):
        updated = queryset.update(status=Ticket.INPROGRESS)
        self.message_user(request, ngettext(
            '%d Ticket was successfully marked as responded.',
            '%d Tickets were successfully marked as responded.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected tickets as closed')
    def ticket_closed(self, request, queryset):
        updated = queryset.update(status=Ticket.CLOSED)
        self.message_user(request, ngettext(
            '%d Ticket was successfully marked as closed.',
            '%d Tickets were successfully marked as closed.',
            updated,
        ) % updated, messages.SUCCESS)

class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['ticket', 'submitted_by', 'date_created', 'content']
    list_display = ['ticket', 'submitted_by', 'date_created']
    list_filter = ['ticket', 'submitted_by', 'date_created']

class GeneralEnquiryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'subject', 'message', 'status', 'email']
    list_display = ['name', 'subject', 'email', 'status', 'date']
    list_filter = ['name', 'subject', 'email', 'status', 'date']
    actions = ['enquiry_respond', 'enquiry_closed']


    @admin.action(description='Mark selected enquiries as responded')
    def enquiry_respond(self, request, queryset):
        updated = queryset.update(status=GeneralEnquiry.RESPONDED)
        self.message_user(request, ngettext(
            '%d Enquiry was successfully marked as responded.',
            '%d Enquiries were successfully marked as responded.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected enquiries as closed')
    def enquiry_closed(self, request, queryset):
        updated = queryset.update(status=GeneralEnquiry.CLOSED)
        self.message_user(request, ngettext(
            '%d Enquiry was successfully marked as closed.',
            '%d Enquiries were successfully marked as closed.',
            updated,
        ) % updated, messages.SUCCESS)



class NotificationsAdmin(admin.ModelAdmin):
    search_fields = ['created_by', 'content', 'date_created']
    list_display = ['created_by', 'content', 'date_created']
    list_filter = ['created_by', 'content', 'date_created']


admin.site.register(Donor, DonorAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(GeneralEnquiry, GeneralEnquiryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Advisor, AdvisorAdmin)
