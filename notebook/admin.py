from django.contrib import admin
from .models import Profile, Program, ViewProgram

# Register your models here.
admin.site.register(Profile)
admin.site.register(Program)
admin.site.register(ViewProgram)
