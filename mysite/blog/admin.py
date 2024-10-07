from django.contrib import admin
from .models import Comment, Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']    

# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ['title', 'slug', 'author', 'publish', 'status']
#     list_filter = ['status', 'created', 'publish', 'author']
#     search_fields = ['title', 'ingredients', 'instructions']
#     prepopulated_fields = {'slug': ('title',)}
#     raw_id_fields = ['author']
#     date_hierarchy = 'publish'
#     ordering = ['status', 'publish']

# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ['recipe', 'user', 'score', 'created']
#     list_filter = ['score', 'created']
#     search_fields = ['user__username', 'recipe__title', 'comment']
#     raw_id_fields = ['user', 'recipe']
#     ordering = ['-created']
