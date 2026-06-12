from django.contrib import admin

from events.models import Category, Event, Registration

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title","description", "date", "location", "capacity","category", "is_cancelled" ]
    list_filter = ["created_by", "category", "is_cancelled"]
    search_fields = ["title", "location"]

@admin.register(Registration)
class RegistrationAdin(admin.ModelAdmin):
    list_display = ["participant", "event", "status", "registered_at"]
    list_filter = ["status"]
    search_fields = ["participant__name", "event__title"]