from django.contrib import admin
from.models import User, Blog,Comment

class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'created_at', 'updated_at', 'published')
    list_filter = ('status',)
    # ordering = ('created_at',)
    search_fields = ('title','content')

admin.site.register(User)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)


# Register your models here.
