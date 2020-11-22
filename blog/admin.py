from django.contrib import admin
from django.contrib import messages 
from .models import Post
from django.urls import path
from django.http import HttpResponseRedirect
from .github_code import update_posts_from_github

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    change_list_template = "admin/base_file.html"

    def active(self, obj): 
        return obj.status == 1
  
    active.boolean = True

    def publish(modeladmin, request, queryset): 
        queryset.update(status = 1) 
        messages.success(request, "Selected Record(s) Marked as published Successfully !!") 
  
    def unpublish(modeladmin, request, queryset): 
        queryset.update(status = 0) 
        messages.success(request, "Selected Record(s) Marked as unpublished Successfully !!") 
  
    admin.site.add_action(publish, "Publish") 
    admin.site.add_action(unpublish, "Unpublish")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update/', self.update_projects),
        ]
        return my_urls + urls

    def update_projects(self, request):
        update_posts_from_github("cyrilhokage")
        self.message_user(request, "Projects successfully updated")
        return HttpResponseRedirect("../")
  
admin.site.register(Post, PostAdmin)

