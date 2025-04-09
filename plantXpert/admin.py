from django.contrib import admin

# Register your models here.
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # Display fields in the admin panel
    search_fields = ('name', 'email', 'subject')  # Enable search functionality
    list_filter = ('created_at',)  # Add filters for better management
