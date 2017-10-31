from django.contrib import admin

# Register your models here.
from .models import Skill, Tag, Event, Location, User, Project

admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Project)

class ProjectInline(admin.TabularInline):
    model = Project
# Define the admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'relevant_skills', 'projects_owned')
    fields = ['name', 'id', 'email', 'relevant_skills', 'projects_owned']
    inlines = [ProjectInline]
