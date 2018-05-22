from django.contrib import admin
from .models import Post, Worker, Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'body')

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'tag_list')
	def get_queryset(self,request):
		return super(PostAdmin, self).get_queryset(request).prefetch_related('tags')
	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Comment, CommentAdmin)

admin.site.register(Post, PostAdmin)

admin.site.register(Worker)

