from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'is_pinned')
    list_filter = ('is_published', 'is_pinned', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    list_editable = ('is_published', 'is_pinned')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fields = ('title', 'excerpt', 'content', 'image', 'pdf', 'is_published', 'is_pinned')
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()