from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'real_estate', 'text', 'is_moderated', 'created_at', 'updated_at']
    list_filter = ['is_moderated', 'created_at']
    search_fields = ['author__username', 'real_estate__title']

admin.site.register(Review, ReviewAdmin)