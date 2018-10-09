from django.contrib import admin
from .models import Comment, Post
# Register your models here.
class CommentInline(admin.TabularInline):
	# readonly_fields = ("date",)
	model = Comment
	extra = 0

class PostAdmin(admin.ModelAdmin):
	# readonly_fields = ("date",)
	fieldsets = [
	    (None, {'fields': ['post_title']}),
	    (None, {'fields': ['post_url']})
	    # ('Date information', {'fields': ['time_created']}),
	]
	inlines = [CommentInline]
	list_display = ('post_title', 'time_created')
	list_filter = ['time_created']
	search_fields = ['post_title']

admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
