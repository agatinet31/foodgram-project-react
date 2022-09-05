from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year')
    search_fields = ('name', 'description')
    list_filter = ('year',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'score')
    search_fields = ('title',)
    list_filter = ('score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text')
    search_fields = ('text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
